import uuid
from datetime import datetime
from models import (
    Product, ProductStore, CartItem, Receipt, ReceiptStore,
    TAX_RATE, DISCOUNT_TIERS, LOW_STOCK_THRESHOLD,
)

class Cart:
    def __init__(self):
        self._items: dict[str, CartItem] = {}

    def add_item(self, product: Product, qty: int = 1) -> str:
        if qty <= 0:
            return "Quantity must be positive."
        if product.quantity < qty:
            return f"Only {product.quantity} unit(s) of '{product.name}' in stock."
        if product.product_id in self._items:
            current = self._items[product.product_id].qty
            if product.quantity < current + qty:
                return f"Cannot add {qty} more. Only {product.quantity - current} left."
            self._items[product.product_id].qty += qty
        else:
            self._items[product.product_id] = CartItem(product, qty)
        return ""

    def remove_item(self, product_id: str) -> bool:
        if product_id in self._items:
            del self._items[product_id]
            return True
        return False

    def update_qty(self, product_id: str, qty: int) -> str:
        if product_id not in self._items:
            return "Item not in cart."
        item = self._items[product_id]
        if qty <= 0:
            del self._items[product_id]
            return ""
        if item.product.quantity < qty:
            return f"Only {item.product.quantity} unit(s) available."
        item.qty = qty
        return ""

    def clear(self):
        self._items.clear()

    @property
    def items(self) -> list[CartItem]:
        return list(self._items.values())

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    @property
    def subtotal(self) -> float:
        return sum(i.subtotal for i in self._items.values())

    def compute_discount(self) -> float:
        sub  = self.subtotal
        rate = 0.0
        for threshold in sorted(DISCOUNT_TIERS.keys()):
            if sub >= threshold:
                rate = DISCOUNT_TIERS[threshold]
        return round(sub * rate, 2)

    def compute_tax(self, after_discount: float) -> float:
        return round(after_discount * TAX_RATE, 2)

    def totals(self) -> dict:
        sub      = round(self.subtotal, 2)
        discount = self.compute_discount()
        taxable  = round(sub - discount, 2)
        tax      = self.compute_tax(taxable)
        total    = round(taxable + tax, 2)
        return {
            "subtotal":  sub,
            "discount":  discount,
            "tax":       tax,
            "total":     total,
        }

class BillingEngine:
    def __init__(self, product_store: ProductStore, receipt_store: ReceiptStore):
        self.product_store = product_store
        self.receipt_store = receipt_store

    def checkout(self, cart: Cart, amount_paid: float) -> tuple[Receipt | None, str]:
        if cart.is_empty:
            return None, "Cart is empty."

        t = cart.totals()
        if amount_paid < t["total"]:
            return None, (
                f"Insufficient payment. Total is ₱{t['total']:.2f}, "
                f"you paid ₱{amount_paid:.2f}."
            )

        for item in cart.items:
            p = self.product_store.get(item.product.product_id)
            if not p or p.quantity < item.qty:
                return None, f"Stock error for '{item.product.name}'. Please refresh cart."
            p.quantity -= item.qty
        self.product_store.save()

        change = round(amount_paid - t["total"], 2)

        receipt = Receipt(
            receipt_id  = "RCP-" + str(uuid.uuid4())[:8].upper(),
            items       = [i.to_dict() for i in cart.items],
            subtotal    = t["subtotal"],
            discount    = t["discount"],
            tax         = t["tax"],
            total       = t["total"],
            amount_paid = amount_paid,
            change      = change,
            timestamp   = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.receipt_store.add(receipt)
        cart.clear()
        return receipt, ""

class InventoryManager:
    def __init__(self, store: ProductStore):
        self.store = store

    def low_stock_alerts(self) -> list[Product]:
        return self.store.low_stock()

    def restock(self, product_id: str, qty: int) -> str:
        p = self.store.get(product_id)
        if not p:
            return "Product not found."
        if qty <= 0:
            return "Restock quantity must be positive."
        p.quantity += qty
        self.store.save()
        return ""

class SearchEngine:
    def __init__(self, store: ProductStore):
        self.store = store

    def search(self, query: str) -> list[Product]:
        query = query.strip()
        if not query:
            return self.store.all()
        by_id   = self.store.find_by_id(query.upper())
        by_name = self.store.find_by_name(query)
        seen, results = set(), []
        for p in ([by_id] if by_id else []) + by_name:
            if p and p.product_id not in seen:
                seen.add(p.product_id)
                results.append(p)
        return results

class ReceiptFormatter:
    STORE_NAME = "BACTAD POS"
    WIDTH      = 48

    @classmethod
    def format(cls, receipt: Receipt) -> str:
        w   = cls.WIDTH
        sep = "─" * w
        lines = [
            cls._center("★ " + cls.STORE_NAME + " ★", w),
            cls._center("Official Receipt", w),
            sep,
            f"  Receipt No : {receipt.receipt_id}",
            f"  Date/Time  : {receipt.timestamp}",
            sep,
            f"  {'ITEM':<22} {'QTY':>4} {'PRICE':>8} {'TOTAL':>9}",
            sep,
        ]
        for entry in receipt.items:
            p    = entry["product"]
            qty  = entry["qty"]
            name = p["name"][:22]
            price = p["price"]
            total = price * qty
            lines.append(f"  {name:<22} {qty:>4} {price:>8.2f} {total:>9.2f}")

        lines += [
            sep,
            f"  {'Subtotal':>34} ₱{receipt.subtotal:>9.2f}",
            f"  {'Discount':>34} ₱{receipt.discount:>9.2f}",
            f"  {'Tax (12% VAT)':>34} ₱{receipt.tax:>9.2f}",
            sep,
            f"  {'TOTAL':>34} ₱{receipt.total:>9.2f}",
            f"  {'Amount Paid':>34} ₱{receipt.amount_paid:>9.2f}",
            f"  {'Change':>34} ₱{receipt.change:>9.2f}",
            sep,
            cls._center("Thank you for shopping!", w),
            cls._center("Please come again 😊", w),
            sep,
        ]
        return "\n".join(lines)

    @staticmethod
    def _center(text: str, width: int) -> str:
        return text.center(width)
