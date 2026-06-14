"""
main.py — JolliKod: Kanto Style Fastfood
Turtle Graphics UI with Jollibee-inspired red/yellow theme.
Real-time order queue: PREPARING → READY → DELIVERED
"""

import turtle
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

from models import MenuItem, Order, OrderStatus, MENU_CATALOGUE
from queue_manager import QueueManager

# ── Theme ─────────────────────────────────────────────────────────────────────
W, H      = 1300, 800
BG        = "#1A0000"
RED       = "#CC0000"
DKRED     = "#8B0000"
YELLOW    = "#FFD700"
AMBER     = "#E65100"
GREEN     = "#2E7D32"
LT_GREEN  = "#00C853"
GRAY      = "#757575"
WHITE     = "#FFFFFF"
PANEL_BG  = "#2D0505"
CARD_BG   = "#3D0F0F"
CARD_PREP = "#1A1200"
CARD_READY= "#001A05"
CARD_DONE = "#111111"

# ── Drawing Helpers ───────────────────────────────────────────────────────────

def rect(pen, x, y, w, h, fill, outline=None, lw=1):
    """Draw filled rectangle; (x,y) = bottom-left corner."""
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(outline or fill, fill)
    pen.width(lw)
    pen.begin_fill()
    for _ in range(2):
        pen.forward(w)
        pen.left(90)
        pen.forward(h)
        pen.left(90)
    pen.end_fill()
    pen.penup()


def text(pen, x, y, msg, color=WHITE, size=11, style="normal", align="center"):
    pen.penup()
    pen.goto(x, y)
    pen.color(color)
    pen.write(msg, align=align, font=("Arial", size, style))
    pen.penup()


def circle_fill(pen, cx, cy, r, fill, outline=None):
    pen.penup()
    pen.goto(cx, cy - r)
    pen.pendown()
    pen.color(outline or fill, fill)
    pen.begin_fill()
    pen.circle(r)
    pen.end_fill()
    pen.penup()


# ── Button ────────────────────────────────────────────────────────────────────

class Button:
    def __init__(self, cx, cy, w, h, label, cb, bg=YELLOW, fg="#1A0000", size=10):
        self.cx, self.cy = cx, cy
        self.w,  self.h  = w, h
        self.label = label
        self.cb    = cb
        self.bg    = bg
        self.fg    = fg
        self.size  = size

    def draw(self, pen):
        rx = self.cx - self.w / 2
        ry = self.cy - self.h / 2
        rect(pen, rx, ry, self.w, self.h, self.bg, self._border(), 2)
        # rounded feel: inner highlight
        rect(pen, rx + 2, ry + self.h - 5, self.w - 4, 4,
             self._lighten(), self._lighten())
        text(pen, self.cx, self.cy - self.size // 2 - 2,
             self.label, self.fg, self.size, "bold")

    def _border(self):
        if self.bg == YELLOW:   return "#B8860B"
        if self.bg == LT_GREEN: return "#1B5E20"
        if self.bg == RED:      return DKRED
        return DKRED

    def _lighten(self):
        if self.bg == YELLOW:   return "#FFE066"
        if self.bg == LT_GREEN: return "#66BB6A"
        if self.bg == RED:      return "#E57373"
        return "#666"

    def hit(self, mx, my):
        return (abs(mx - self.cx) <= self.w / 2 and
                abs(my - self.cy) <= self.h / 2)

    def click(self, mx, my):
        if self.hit(mx, my):
            self.cb()
            return True
        return False


# ── Main App ──────────────────────────────────────────────────────────────────

class JolliKodApp:

    # ──────────────────────────────────────────────────────────────────────────
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(W, H)
        self.screen.title("JolliKod — Kanto Style Fastfood")
        self.screen.bgcolor(BG)
        self.screen.tracer(0)

        self.bg_pen  = turtle.Turtle(); self.bg_pen.hideturtle();  self.bg_pen.speed(0)
        self.dyn_pen = turtle.Turtle(); self.dyn_pen.hideturtle(); self.dyn_pen.speed(0)

        self.cart: list[MenuItem] = []
        self.static_buttons: list[Button] = []
        self.deliver_buttons: list[tuple[Button, str]] = []

        self.qm = QueueManager(on_status_change=lambda o: None)
        self.qm.start()

        self._build_layout()
        self._draw_static()
        self._draw_cart()

        self.screen.onclick(self._click)
        self._refresh()

    # ── Layout constants ──────────────────────────────────────────────────────

    def _build_layout(self):
        # Header
        self.HDR_H   = 85
        self.HDR_Y   = H // 2 - self.HDR_H          # bottom of header = 315

        # Left panel  (menu + cart)
        self.LX      = -W // 2                       # -650
        self.LW      = 640
        self.PANEL_Y = -H // 2                       # -400
        self.PANEL_H = self.HDR_Y - self.PANEL_Y     # 715

        # Right panel (queue)
        self.RX      = self.LX + self.LW + 10        # 0
        self.RW      = W - self.LW - 10              # 650

        # Menu items
        self.MENU_TOP    = self.HDR_Y - 55           # 260
        self.ITEM_H      = 56
        self.ITEM_X      = self.LX + 15
        self.ITEM_W      = self.LW - 30

        # Cart box
        items_end        = self.MENU_TOP - len(MENU_CATALOGUE) * self.ITEM_H
        self.CART_TOP    = items_end - 10            # ~-22
        self.CART_H      = 115
        self.CART_BOT    = self.CART_TOP - self.CART_H

        # Buttons row
        self.BTN_Y       = self.CART_BOT - 22

        # Right sections
        self.PREP_TOP    = self.HDR_Y - 55           # 260  (below right header)
        self.READY_TOP   = 40
        self.DELIV_TOP   = -175

    # ── Static drawing ────────────────────────────────────────────────────────

    def _draw_static(self):
        p = self.bg_pen
        p.clear()

        # ── Header background
        rect(p, self.LX, self.HDR_Y, W, self.HDR_H, RED, DKRED, 3)
        rect(p, self.LX, self.HDR_Y, W, 6, YELLOW)             # gold stripe

        # ── Bee mascots
        self._bee(p, self.LX + 70, self.HDR_Y + 42, 26)
        self._bee(p, -self.LX - 70, self.HDR_Y + 42, 26)

        # ── Header text
        text(p, 0, self.HDR_Y + 42, "JolliKod", YELLOW, 34, "bold")
        text(p, 0, self.HDR_Y + 14, '"Kanto Style Fastfood"', WHITE, 13, "italic")

        # ── Left panel bg
        rect(p, self.LX, self.PANEL_Y, self.LW, self.PANEL_H, PANEL_BG, DKRED, 2)

        # ── Left panel title bar
        rect(p, self.LX, self.HDR_Y - 55, self.LW, 50, DKRED, RED, 2)
        text(p, self.LX + self.LW // 2, self.HDR_Y - 43, "🍟  ORDER MENU", YELLOW, 14, "bold")

        # ── Menu item cards
        self.static_buttons.clear()
        for i, item in enumerate(MENU_CATALOGUE):
            card_top = self.MENU_TOP - i * self.ITEM_H
            card_bot = card_top - self.ITEM_H
            cy = (card_top + card_bot) / 2
            ix = self.ITEM_X

            rect(p, ix, card_bot, self.ITEM_W, self.ITEM_H, CARD_BG, RED, 1)
            # emoji badge
            rect(p, ix, card_bot, 46, self.ITEM_H, RED)
            text(p, ix + 23, cy - 8, item.emoji, YELLOW, 17, "bold")
            # name + info
            text(p, ix + 56, cy + 6,  item.name,  WHITE,  11, "bold",   "left")
            text(p, ix + 56, cy - 10,
                 f"₱{item.price:.0f}  •  {item.cook_time}s cook time",
                 YELLOW, 8, "normal", "left")

            # ADD button
            btn = Button(ix + self.ITEM_W - 38, cy, 58, 28,
                         "+ ADD", lambda m=item: self._add(m),
                         YELLOW, "#1A0000", 9)
            btn.draw(p)
            self.static_buttons.append(btn)

        # ── Cart box
        rect(p, self.ITEM_X, self.CART_BOT, self.ITEM_W, self.CART_H,
             "#0D0000", YELLOW, 2)
        text(p, self.LX + self.LW // 2, self.CART_TOP - 18, "🛒  YOUR ORDER",
             YELLOW, 11, "bold")

        # ── Action buttons
        mid = self.LX + self.LW // 2
        clear_btn = Button(mid - 90, self.BTN_Y, 100, 34,
                           "CLEAR", self._clear, DKRED, WHITE, 10)
        clear_btn.draw(p)
        self.static_buttons.append(clear_btn)

        place_btn = Button(mid + 45, self.BTN_Y, 140, 34,
                           "PLACE ORDER", self._place_order, YELLOW, "#1A0000", 10)
        place_btn.draw(p)
        self.static_buttons.append(place_btn)

        # ── Right panel bg
        rect(p, self.RX, self.PANEL_Y, self.RW, self.PANEL_H, PANEL_BG, DKRED, 2)

        # ── Right panel title bar
        rect(p, self.RX, self.HDR_Y - 55, self.RW, 50, DKRED, RED, 2)
        text(p, self.RX + self.RW // 2, self.HDR_Y - 43,
             "⚡  LIVE ORDER QUEUE", YELLOW, 14, "bold")

        # ── Section headers (right)
        def sec_hdr(label, y_top, color):
            rect(p, self.RX + 5, y_top - 28, self.RW - 10, 28, color, color)
            text(p, self.RX + self.RW // 2, y_top - 22, label, WHITE, 10, "bold")

        sec_hdr("⏳  PREPARING",     self.PREP_TOP,  AMBER)
        sec_hdr("✅  READY TO SERVE", self.READY_TOP, GREEN)
        sec_hdr("🎉  DELIVERED",      self.DELIV_TOP, GRAY)

        self.screen.update()

    # ── Bee mascot ────────────────────────────────────────────────────────────

    def _bee(self, p, cx, cy, r):
        # body
        circle_fill(p, cx, cy - r, r, YELLOW, "#B8860B")
        # stripes
        for dy in [-r // 3, r // 4]:
            rect(p, cx - r + 3, cy + dy, (r - 3) * 2, r // 4, DKRED)
        # wing
        circle_fill(p, cx + r - 2, cy + r // 2, r // 2, "#CCEFFF", "#AADDFF")
        # eye
        circle_fill(p, cx + r // 3, cy + r // 3, 3, "#1A0000")

    # ── Cart ─────────────────────────────────────────────────────────────────

    def _add(self, item: MenuItem):
        self.cart.append(item)
        self._draw_cart()

    def _clear(self):
        self.cart.clear()
        self._draw_cart()

    def _draw_cart(self):
        p = self.dyn_pen
        # Erase old cart contents
        rect(p, self.ITEM_X + 2, self.CART_BOT + 2,
             self.ITEM_W - 4, self.CART_H - 22, "#0D0000")

        if not self.cart:
            text(p, self.LX + self.LW // 2, self.CART_TOP - 50,
                 "No items selected yet", GRAY, 9, "italic")
            self.screen.update()
            return

        counts: dict[str, tuple[int, float]] = {}
        for itm in self.cart:
            n, p2 = counts.get(itm.name, (0, 0.0))
            counts[itm.name] = (n + 1, p2 + itm.price)

        line_y = self.CART_TOP - 35
        for name, (qty, subtotal) in list(counts.items())[:4]:
            short = name[:22]
            text(self.dyn_pen, self.ITEM_X + 8, line_y,
                 f"• {qty}x {short}", WHITE, 9, "normal", "left")
            text(self.dyn_pen, self.ITEM_X + self.ITEM_W - 8, line_y,
                 f"₱{subtotal:.0f}", YELLOW, 9, "bold", "right")
            line_y -= 18

        total = sum(i.price for i in self.cart)
        rect(self.dyn_pen, self.ITEM_X + 2, self.CART_BOT + 2,
             self.ITEM_W - 4, 20, "#1A0000")
        text(self.dyn_pen, self.ITEM_X + self.ITEM_W // 2,
             self.CART_BOT + 5,
             f"TOTAL:  ₱{total:.2f}", YELLOW, 11, "bold")

        self.screen.update()

    # ── Place Order ──────────────────────────────────────────────────────────

    def _place_order(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add items before placing an order!")
            return
        root = self.screen.getcanvas().winfo_toplevel()
        name = simpledialog.askstring("Customer Name", "Enter customer name:", parent=root)
        if not name or not name.strip():
            return
        order = Order(name.strip(), list(self.cart))
        self.cart.clear()
        self._draw_cart()
        self.qm.add_order(order)

    # ── Dynamic queue panel ───────────────────────────────────────────────────

    def _refresh(self):
        self._draw_queue()
        self.screen.ontimer(self._refresh, 1000)

    def _draw_queue(self):
        p = self.dyn_pen
        self.deliver_buttons.clear()

        rx  = self.RX + 5
        rw  = self.RW - 10
        cw  = rw - 10           # card width
        ch  = 52                 # card height
        pad = 5

        # Erase entire right queue area
        rect(p, rx, self.PANEL_Y + 1, rw, self.PANEL_H - 2, PANEL_BG)

        # ── PREPARING ─────────────────────────────────────────────────────────
        rect(p, rx, self.PREP_TOP - 28, rw, 28, AMBER, AMBER)
        text(p, rx + rw // 2, self.PREP_TOP - 22, "⏳  PREPARING", WHITE, 10, "bold")

        orders = self.qm.get_orders_by_status(OrderStatus.PREPARING)
        y = self.PREP_TOP - 28 - pad
        if not orders:
            text(p, rx + rw // 2, y - 18, "No orders being prepared…", GRAY, 8, "italic")
        for o in orders[:4]:
            y -= ch + pad
            self._order_card(p, rx + 5, y, cw, ch, o, AMBER, CARD_PREP, "timer")

        # ── READY ─────────────────────────────────────────────────────────────
        rect(p, rx, self.READY_TOP - 28, rw, 28, GREEN, GREEN)
        text(p, rx + rw // 2, self.READY_TOP - 22, "✅  READY TO SERVE", WHITE, 10, "bold")

        orders = self.qm.get_orders_by_status(OrderStatus.READY)
        y = self.READY_TOP - 28 - pad
        if not orders:
            text(p, rx + rw // 2, y - 18, "No orders ready yet…", GRAY, 8, "italic")
        for o in orders[:3]:
            y -= ch + pad
            self._order_card(p, rx + 5, y, cw, ch, o, LT_GREEN, CARD_READY, "deliver")

        # ── DELIVERED ─────────────────────────────────────────────────────────
        rect(p, rx, self.DELIV_TOP - 28, rw, 28, GRAY, GRAY)
        text(p, rx + rw // 2, self.DELIV_TOP - 22, "🎉  DELIVERED", WHITE, 10, "bold")

        orders = list(reversed(self.qm.get_orders_by_status(OrderStatus.DELIVERED)))
        y = self.DELIV_TOP - 28 - pad
        if not orders:
            text(p, rx + rw // 2, y - 18, "No deliveries yet…", GRAY, 8, "italic")
        for o in orders[:3]:
            y -= ch + pad
            self._order_card(p, rx + 5, y, cw, ch, o, GRAY, CARD_DONE, "done")

        # ── Stats bar ─────────────────────────────────────────────────────────
        self._stats_bar(p, rx, rw)
        self.screen.update()

    def _order_card(self, p, x, y, w, h, order: Order, accent, bg, mode):
        """Draw one order card at (x,y) bottom-left."""
        rect(p, x, y, w, h, bg, accent, 2)
        rect(p, x, y, 6, h, accent)          # left accent bar

        # Badge
        rect(p, x + 10, y + h - 22, 52, 18, accent)
        text(p, x + 36, y + h - 20, f"#{order.order_id}", "#1A0000", 8, "bold")

        # Name
        cname = order.customer_name[:16]
        text(p, x + 70, y + h - 16, cname, WHITE, 11, "bold", "left")

        # Items
        summary = order.item_summary
        if len(summary) > 30: summary = summary[:28] + "…"
        text(p, x + 70, y + h - 30, summary, YELLOW, 8, "normal", "left")

        # Price
        text(p, x + 70, y + h - 44, f"₱{order.total_price:.2f}", "#FFD700", 8, "normal", "left")

        if mode == "timer":
            secs = max(order.remaining_sec, 0)
            timer_str = f"{secs // 60:02d}:{secs % 60:02d}"
            rect(p, x + w - 78, y + h // 2 - 15, 70, 30, AMBER, "#FF6600", 2)
            text(p, x + w - 43, y + h // 2 - 11, timer_str, WHITE, 14, "bold")

        elif mode == "deliver":
            btn = Button(x + w - 42, y + h // 2, 72, 30,
                         "DELIVER",
                         lambda oid=order.order_id: self._deliver(oid),
                         LT_GREEN, WHITE, 9)
            btn.draw(p)
            self.deliver_buttons.append((btn, order.order_id))

        elif mode == "done":
            text(p, x + w - 42, y + h // 2 - 6, "✓ DONE", LT_GREEN, 9, "bold")

    def _stats_bar(self, p, rx, rw):
        stats = self.qm.stats()
        bar_y = self.PANEL_Y + 1
        rect(p, rx, bar_y, rw, 36, DKRED, RED, 1)
        seg = rw // 4
        labels = [
            (f"Total: {stats['total']}",       WHITE),
            (f"Preparing: {stats['preparing']}", YELLOW),
            (f"Ready: {stats['ready']}",         LT_GREEN),
            (f"Delivered: {stats['delivered']}", GRAY),
        ]
        for i, (lbl, col) in enumerate(labels):
            text(p, rx + seg * i + seg // 2, bar_y + 10, lbl, col, 8, "bold")

    # ── Deliver ───────────────────────────────────────────────────────────────

    def _deliver(self, order_id: str):
        self.qm.deliver_order(order_id)

    # ── Click dispatcher ──────────────────────────────────────────────────────

    def _click(self, mx, my):
        for btn in self.static_buttons:
            if btn.click(mx, my):
                return
        for btn, _ in self.deliver_buttons:
            if btn.click(mx, my):
                return

    # ── Run ───────────────────────────────────────────────────────────────────

    def run(self):
        self.screen.mainloop()


# ── Entry ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = JolliKodApp()
    app.run()
