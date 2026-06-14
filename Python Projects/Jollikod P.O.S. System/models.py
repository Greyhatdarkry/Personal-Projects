"""
models.py — JolliKod Kanto Style Fastfood
Data models: MenuItem, Order, OrderStatus
"""

from enum import Enum
from datetime import datetime
import uuid


# ─── Status Enum ──────────────────────────────────────────────────────────────

class OrderStatus(Enum):
    QUEUED    = "Queued"
    PREPARING = "Preparing"
    READY     = "Ready"
    DELIVERED = "Delivered"


# ─── Menu Items ───────────────────────────────────────────────────────────────

class MenuItem:
    def __init__(self, name: str, cook_time: int, price: float, emoji: str = ""):
        """
        :param name:      Display name of the item
        :param cook_time: Cooking time in seconds (for real-time demo)
        :param price:     Price in pesos
        :param emoji:     Decorative label character
        """
        self.name      = name
        self.cook_time = cook_time   # seconds
        self.price     = price
        self.emoji     = emoji

    def __repr__(self):
        return f"MenuItem({self.name}, {self.cook_time}s, ₱{self.price})"


# ─── Order ────────────────────────────────────────────────────────────────────

class Order:
    def __init__(self, customer_name: str, items: list[MenuItem]):
        self.order_id      = str(uuid.uuid4())[:6].upper()
        self.customer_name = customer_name
        self.items         = items                     # list of MenuItem
        self.status        = OrderStatus.QUEUED
        self.created_at    = datetime.now()
        self.cook_end_time = None                      # set when PREPARING starts
        self.remaining_sec = 0                         # countdown seconds

    @property
    def total_price(self) -> float:
        return sum(item.price for item in self.items)

    @property
    def max_cook_time(self) -> int:
        """Longest cook time among all items in the order."""
        return max(item.cook_time for item in self.items) if self.items else 0

    @property
    def item_summary(self) -> str:
        counts: dict[str, int] = {}
        for item in self.items:
            counts[item.name] = counts.get(item.name, 0) + 1
        return ", ".join(
            f"{qty}x {name}" for name, qty in counts.items()
        )

    def __repr__(self):
        return (f"Order#{self.order_id} [{self.customer_name}] "
                f"{self.item_summary} — {self.status.value}")


# ─── Pre-defined Menu Catalogue ───────────────────────────────────────────────
# Cook times are in seconds so the demo is watchable in real time.
# (Fries=10s, Fried Chicken=20s — matching the user's spec)

MENU_CATALOGUE: list[MenuItem] = [
    MenuItem("Jollikod Fries",          cook_time=10,  price=59.00,  emoji="F"),
    MenuItem("Kanto Fried Chicken",     cook_time=20,  price=129.00, emoji="C"),
    MenuItem("Kanto Burger",            cook_time=15,  price=89.00,  emoji="B"),
    MenuItem("Streetside Rice Meal",    cook_time=12,  price=75.00,  emoji="R"),
    MenuItem("Kanto Spaghetti",         cook_time=18,  price=95.00,  emoji="S"),
]
