import json
import os
import uuid
from datetime import datetime

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.json")
RECEIPTS_FILE = os.path.join(BASE_DIR, "receipts.json")

LOW_STOCK_THRESHOLD = 5
TAX_RATE            = 0.12
DISCOUNT_TIERS      = {
    500:  0.05,
    1000: 0.10,
    2000: 0.15,
}

class Product:
    def __init__(self, product_id: str, name: str, price: float, quantity: int,
                 category: str = "General"):
        self.product_id = product_id
        self.name       = name
        self.price      = float(price)
        self.quantity   = int(quantity)
        self.category   = category

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name":       self.name,
            "price":      self.price,
            "quantity":   self.quantity,
            "category":   self.category,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Product":
        return cls(
            d["product_id"], d["name"],
            d["price"],      d["quantity"],
            d.get("category", "General"),
        )

    @property
    def is_low_stock(self) -> bool:
        return self.quantity <= LOW_STOCK_THRESHOLD

    def __repr__(self) -> str:
        return f"<Product {self.product_id}: {self.name} ₱{self.price:.2f} qty={self.quantity}>"

class CartItem:
    def __init__(self, product: Product, qty: int = 1):
        self.product = product
        self.qty     = qty

    @property
    def subtotal(self) -> float:
        return self.product.price * self.qty

    def to_dict(self) -> dict:
        return {"product": self.product.to_dict(), "qty": self.qty}

class Receipt:
    def __init__(self, receipt_id: str, items: list[dict], subtotal: float,
                 discount: float, tax: float, total: float,
                 amount_paid: float, change: float, timestamp: str):
        self.receipt_id  = receipt_id
        self.items       = items
        self.subtotal    = subtotal
        self.discount    = discount
        self.tax         = tax
        self.total       = total
        self.amount_paid = amount_paid
        self.change      = change
        self.timestamp   = timestamp

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, d: dict) -> "Receipt":
        return cls(**d)

class ProductStore:
    def __init__(self):
        self._products: dict[str, Product] = {}
        self._load()

    def _load(self):
        if os.path.exists(PRODUCTS_FILE):
            with open(PRODUCTS_FILE, "r") as f:
                data = json.load(f)
            self._products = {d["product_id"]: Product.from_dict(d) for d in data}

    def save(self):
        with open(PRODUCTS_FILE, "w") as f:
            json.dump([p.to_dict() for p in self._products.values()], f, indent=2)

    def all(self) -> list[Product]:
        return list(self._products.values())

    def get(self, product_id: str) -> Product | None:
        return self._products.get(product_id)

    def find_by_name(self, query: str) -> list[Product]:
        q = query.lower()
        return [p for p in self._products.values() if q in p.name.lower()]

    def find_by_id(self, pid: str) -> Product | None:
        return self._products.get(pid)

    def add(self, name: str, price: float, quantity: int,
            category: str = "General") -> Product:
        pid = str(uuid.uuid4())[:8].upper()
        p   = Product(pid, name, price, quantity, category)
        self._products[pid] = p
        self.save()
        return p

    def update(self, product_id: str, name: str | None = None,
               price: float | None = None, quantity: int | None = None,
               category: str | None = None) -> bool:
        p = self._products.get(product_id)
        if not p:
            return False
        if name     is not None: p.name     = name
        if price    is not None: p.price    = float(price)
        if quantity is not None: p.quantity = int(quantity)
        if category is not None: p.category = category
        self.save()
        return True

    def delete(self, product_id: str) -> bool:
        if product_id not in self._products:
            return False
        del self._products[product_id]
        self.save()
        return True

    def low_stock(self) -> list[Product]:
        return [p for p in self._products.values() if p.is_low_stock]

class ReceiptStore:
    def __init__(self):
        self._receipts: list[Receipt] = []
        self._load()

    def _load(self):
        if os.path.exists(RECEIPTS_FILE):
            with open(RECEIPTS_FILE, "r") as f:
                data = json.load(f)
            self._receipts = [Receipt.from_dict(d) for d in data]

    def save(self):
        with open(RECEIPTS_FILE, "w") as f:
            json.dump([r.to_dict() for r in self._receipts], f, indent=2)

    def add(self, receipt: Receipt):
        self._receipts.append(receipt)
        self.save()

    def all(self) -> list[Receipt]:
        return list(reversed(self._receipts))

    def get(self, receipt_id: str) -> Receipt | None:
        return next((r for r in self._receipts if r.receipt_id == receipt_id), None)
