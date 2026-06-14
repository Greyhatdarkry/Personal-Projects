"""
queue_manager.py — JolliKod Kanto Style Fastfood
Real-time queue engine using threading.Timer.
Manages QUEUED → PREPARING → READY pipeline.

Algorithm: Insertion Sort is applied to the PREPARING queue so orders
are always displayed in ascending remaining-cook-time order — the order
closest to completion surfaces to the top, giving kitchen staff precise
priority visibility at a glance.
"""

import threading
import time
from typing import Callable
from models import Order, OrderStatus


class QueueManager:
    """
    Manages the order lifecycle:
      QUEUED → PREPARING (cook timer starts) → READY → (manual) DELIVERED
    """

    def __init__(self, on_status_change: Callable[[Order], None] | None = None):
        """
        :param on_status_change: callback fired every time an order's status changes
        """
        self._orders: list[Order]      = []
        self._lock                     = threading.Lock()
        self._timers: dict[str, threading.Timer] = {}
        self._tick_thread: threading.Thread | None = None
        self._running                  = False
        self.on_status_change          = on_status_change

    # ── Public API ──────────────────────────────────────────────────────────

    def start(self):
        """Start the background tick thread that counts down cook timers."""
        self._running = True
        self._tick_thread = threading.Thread(target=self._tick_loop, daemon=True)
        self._tick_thread.start()

    def stop(self):
        self._running = False
        for t in self._timers.values():
            t.cancel()
        self._timers.clear()

    def add_order(self, order: Order):
        """Add a new order and immediately start preparing it."""
        with self._lock:
            self._orders.append(order)
        self._begin_preparing(order)

    def deliver_order(self, order_id: str) -> bool:
        """Mark a READY order as DELIVERED. Returns True on success."""
        with self._lock:
            order = self._find(order_id)
            if order and order.status == OrderStatus.READY:
                order.status        = OrderStatus.DELIVERED
                order.remaining_sec = 0
                if self.on_status_change:
                    self.on_status_change(order)
                return True
        return False

    def get_orders_by_status(self, status: OrderStatus) -> list[Order]:
        """Return orders matching status.
        PREPARING orders are sorted by remaining_sec (ascending) via
        insertion sort — shortest cook time remaining appears first.
        """
        with self._lock:
            orders = [o for o in self._orders if o.status == status]
        if status == OrderStatus.PREPARING:
            orders = insertion_sort_by_remaining(orders)
        return orders

    def all_orders(self) -> list[Order]:
        with self._lock:
            return list(self._orders)

    # ── Internals ───────────────────────────────────────────────────────────

    def _find(self, order_id: str) -> Order | None:
        return next((o for o in self._orders if o.order_id == order_id), None)

    def _begin_preparing(self, order: Order):
        with self._lock:
            order.status        = OrderStatus.PREPARING
            order.remaining_sec = order.max_cook_time
        if self.on_status_change:
            self.on_status_change(order)

    def _mark_ready(self, order_id: str):
        with self._lock:
            order = self._find(order_id)
            if order and order.status == OrderStatus.PREPARING:
                order.status        = OrderStatus.READY
                order.remaining_sec = 0
        if order and self.on_status_change:
            self.on_status_change(order)

    def _tick_loop(self):
        """Counts down remaining_sec for each PREPARING order every second."""
        while self._running:
            time.sleep(1)
            with self._lock:
                preparing = [
                    o for o in self._orders
                    if o.status == OrderStatus.PREPARING and o.remaining_sec > 0
                ]
            for order in preparing:
                with self._lock:
                    order.remaining_sec -= 1
                    remaining = order.remaining_sec
                if remaining <= 0:
                    self._mark_ready(order.order_id)

    # ── Stats helpers ────────────────────────────────────────────────────────

    def stats(self) -> dict:
        with self._lock:
            all_o = list(self._orders)
        return {
            "total":     len(all_o),
            "queued":    sum(1 for o in all_o if o.status == OrderStatus.QUEUED),
            "preparing": sum(1 for o in all_o if o.status == OrderStatus.PREPARING),
            "ready":     sum(1 for o in all_o if o.status == OrderStatus.READY),
            "delivered": sum(1 for o in all_o if o.status == OrderStatus.DELIVERED),
        }


# ── Insertion Sort ────────────────────────────────────────────────────────────

def insertion_sort_by_remaining(orders: list) -> list:
    """
    Insertion Sort — O(n²) stable sort on remaining_sec (ascending).

    Why insertion sort here?
    • The PREPARING queue is typically small (≤ 10 concurrent orders).
    • Insertion sort is O(n) on nearly-sorted data, which is exactly the
      case after each 1-second tick (only one value changes per cycle).
    • It is stable, preserving the original arrival order for ties.
    • It is in-place and easy to reason about — ideal for a teaching context.

    Each pass takes the next unsorted order and slides it left until
    it finds its correct position by remaining_sec.
    """
    arr = list(orders)                        # work on a copy
    for i in range(1, len(arr)):
        key = arr[i]                          # element to be inserted
        j   = i - 1
        # Shift elements that are greater than key one position to the right
        while j >= 0 and arr[j].remaining_sec > key.remaining_sec:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key                      # drop key into its sorted slot
    return arr
