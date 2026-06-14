import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import ProductStore, ReceiptStore
from logic  import Cart, BillingEngine, InventoryManager, SearchEngine, ReceiptFormatter

BG   = "#0f172a"
CARD = "#1e293b"
ACC  = "#6366f1"
ACC2 = "#818cf8"
GRN  = "#22c55e"
RED  = "#ef4444"
YLW  = "#f59e0b"
FG   = "#f1f5f9"
FG2  = "#94a3b8"
FONT = ("Segoe UI", 10)
HFONT= ("Segoe UI", 11, "bold")

product_store = ProductStore()
receipt_store = ReceiptStore()
cart          = Cart()
billing       = BillingEngine(product_store, receipt_store)
inventory_mgr = InventoryManager(product_store)
search_engine = SearchEngine(product_store)

if not product_store.all():
    demos = [
        ("Apple",       25.00,  50, "Fruits"),
        ("Banana",      15.00,  80, "Fruits"),
        ("Milk 1L",     75.00,  20, "Dairy"),
        ("Bread Loaf",  55.00,  15, "Bakery"),
        ("Eggs (12pc)", 120.00, 30, "Dairy"),
        ("Rice 1kg",    60.00, 100, "Grains"),
        ("Coffee Sachet",8.00, 200, "Beverages"),
        ("Bottled Water",18.00, 4,  "Beverages"),
    ]
    for n, p, q, c in demos:
        product_store.add(n, p, q, c)

def styled_btn(parent, text, cmd, color=ACC, fg=FG, **kw):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=color, fg=fg, activebackground=color,
                  font=FONT, relief="flat", cursor="hand2",
                  padx=10, pady=5, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=ACC2))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def make_tree(parent, cols, heights=14):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=CARD, foreground=FG, fieldbackground=CARD,
                    rowheight=28, font=FONT)
    style.configure("Custom.Treeview.Heading",
                    background=ACC, foreground=FG, font=HFONT)
    style.map("Custom.Treeview", background=[("selected", ACC)])
    tree = ttk.Treeview(parent, columns=cols, show="headings",
                        height=heights, style="Custom.Treeview")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center", minwidth=60)
    sb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    sb.grid(row=0, column=1, sticky="ns")
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    return tree

def lbl(parent, text, size=10, bold=False, color=FG, **kw):
    w = "bold" if bold else "normal"
    return tk.Label(parent, text=text, bg=BG, fg=color,
                    font=("Segoe UI", size, w), **kw)

def entry(parent, **kw):
    e = tk.Entry(parent, bg=CARD, fg=FG, insertbackground=FG,
                 font=FONT, relief="flat", **kw)
    return e

def card_frame(parent, **kw):
    return tk.Frame(parent, bg=CARD, **kw)

def build_products_tab(nb):
    frame = tk.Frame(nb, bg=BG)
    nb.add(frame, text="📦  Products")
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    tf = tk.Frame(frame, bg=BG, padx=10)
    tf.grid(row=1, column=0, sticky="nsew")
    tf.grid_rowconfigure(0, weight=1); tf.grid_columnconfigure(0, weight=1)

    COLS = ("ID", "Name", "Category", "Price (₱)", "Stock", "Status")
    tree = make_tree(tf, COLS, 18)
    tree.column("ID", width=90); tree.column("Name", width=200)
    tree.column("Category", width=110); tree.column("Price (₱)", width=90)
    tree.column("Stock", width=70); tree.column("Status", width=90)

    def tree_refresh():
        tree.delete(*tree.get_children())
        for p in product_store.all():
            status = "⚠ LOW" if p.is_low_stock else "OK"
            tag    = "low" if p.is_low_stock else ""
            tree.insert("", "end", values=(
                p.product_id, p.name, p.category,
                f"{p.price:.2f}", p.quantity, status), tags=(tag,))
        tree.tag_configure("low", foreground=YLW)

    toolbar = tk.Frame(frame, bg=BG, pady=8)
    toolbar.grid(row=0, column=0, sticky="ew", padx=10)

    lbl(toolbar, "Product Management", 14, bold=True).pack(side="left", padx=(0,20))
    styled_btn(toolbar, "+ Add",    lambda: product_dialog(tree_refresh),  GRN).pack(side="left", padx=3)
    styled_btn(toolbar, "✏ Edit",   lambda: product_edit(tree, tree_refresh), ACC).pack(side="left", padx=3)
    styled_btn(toolbar, "🗑 Delete", lambda: product_delete(tree, tree_refresh), RED).pack(side="left", padx=3)
    styled_btn(toolbar, "🔄 Refresh", tree_refresh,                          ACC).pack(side="right", padx=3)

    tree_refresh()
    return frame, tree_refresh

def product_dialog(refresh, product=None):
    win = tk.Toplevel(); win.title("Product"); win.configure(bg=BG)
    win.geometry("360x300"); win.resizable(False, False)
    fields = {}
    for i, (label, key, val) in enumerate([
        ("Name",     "name",     product.name          if product else ""),
        ("Category", "category", product.category      if product else "General"),
        ("Price",    "price",    str(product.price)    if product else ""),
        ("Quantity", "quantity", str(product.quantity) if product else ""),
    ]):
        lbl(win, label).grid(row=i, column=0, sticky="w", padx=20, pady=8)
        e = entry(win, width=28); e.insert(0, val)
        e.grid(row=i, column=1, padx=10, pady=8)
        fields[key] = e

    def save():
        try:
            name  = fields["name"].get().strip()
            cat   = fields["category"].get().strip() or "General"
            price = float(fields["price"].get())
            qty   = int(fields["quantity"].get())
            if not name: raise ValueError("Name required")
            if product:
                product_store.update(product.product_id, name, price, qty, cat)
            else:
                product_store.add(name, price, qty, cat)
            refresh(); win.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=win)

    styled_btn(win, "💾 Save", save, GRN).grid(row=4, column=0, columnspan=2, pady=15)

def product_edit(tree, refresh):
    sel = tree.selection()
    if not sel: return messagebox.showwarning("Select", "Select a product first.")
    pid = tree.item(sel[0])["values"][0]
    p   = product_store.get(str(pid))
    if p: product_dialog(refresh, p)

def product_delete(tree, refresh):
    sel = tree.selection()
    if not sel: return messagebox.showwarning("Select", "Select a product first.")
    pid = tree.item(sel[0])["values"][0]
    if messagebox.askyesno("Delete", f"Delete product {pid}?"):
        product_store.delete(str(pid))
        refresh()

def build_billing_tab(nb):
    frame = tk.Frame(nb, bg=BG)
    nb.add(frame, text="💳  Billing")
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=3)
    frame.grid_columnconfigure(1, weight=2)

    lbl(frame, "Billing / POS", 14, bold=True).grid(
        row=0, column=0, columnspan=2, sticky="w", padx=14, pady=8)

    left = tk.Frame(frame, bg=BG, padx=8)
    left.grid(row=1, column=0, sticky="nsew")
    left.grid_rowconfigure(1, weight=1); left.grid_columnconfigure(0, weight=1)

    lbl(left, "Products", bold=True).grid(row=0, column=0, sticky="w", pady=(0,4))

    pf = tk.Frame(left, bg=BG); pf.grid(row=1, column=0, sticky="nsew")
    pf.grid_rowconfigure(0, weight=1); pf.grid_columnconfigure(0, weight=1)
    PCOLS = ("ID", "Name", "Price (₱)", "Stock")
    ptree = make_tree(pf, PCOLS, 14)
    ptree.column("ID", width=80); ptree.column("Name", width=160)
    ptree.column("Price (₱)", width=80); ptree.column("Stock", width=60)

    qty_var = tk.StringVar(value="1")

    right = tk.Frame(frame, bg=BG, padx=8)
    right.grid(row=1, column=1, sticky="nsew")
    right.grid_rowconfigure(1, weight=1); right.grid_columnconfigure(0, weight=1)

    lbl(right, "Cart", bold=True).grid(row=0, column=0, sticky="w", pady=(0,4))
    cf = tk.Frame(right, bg=BG); cf.grid(row=1, column=0, sticky="nsew")
    cf.grid_rowconfigure(0, weight=1); cf.grid_columnconfigure(0, weight=1)
    CCOLS = ("Name", "Qty", "Unit ₱", "Total ₱")
    ctree = make_tree(cf, CCOLS, 10)
    ctree.column("Name", width=140); ctree.column("Qty", width=45)
    ctree.column("Unit ₱", width=70); ctree.column("Total ₱", width=75)

    totals_card = card_frame(right, padx=10, pady=8)
    totals_card.grid(row=2, column=0, sticky="ew", pady=6)
    totals_vars = {}
    for i, key in enumerate(["Subtotal", "Discount", "Tax (12%)", "TOTAL"]):
        bold   = key == "TOTAL"
        weight = "bold" if bold else "normal"
        color  = GRN if bold else FG
        lbl(totals_card, key + ":", bold=bold).grid(row=i, column=0, sticky="w", pady=2)
        v = tk.StringVar(value="₱0.00")
        totals_vars[key] = v
        tk.Label(totals_card, textvariable=v, bg=CARD, fg=color,
                 font=("Segoe UI", 10, weight)).grid(row=i, column=1, sticky="e", padx=20)

    def refresh_products():
        ptree.delete(*ptree.get_children())
        for p in product_store.all():
            ptree.insert("", "end", values=(p.product_id, p.name, f"{p.price:.2f}", p.quantity))

    def refresh_cart():
        ctree.delete(*ctree.get_children())
        for item in cart.items:
            ctree.insert("", "end", values=(
                item.product.name, item.qty,
                f"{item.product.price:.2f}", f"{item.subtotal:.2f}"))
        t = cart.totals()
        totals_vars["Subtotal"].set(f"₱{t['subtotal']:.2f}")
        totals_vars["Discount"].set(f"₱{t['discount']:.2f}")
        totals_vars["Tax (12%)"].set(f"₱{t['tax']:.2f}")
        totals_vars["TOTAL"].set(f"₱{t['total']:.2f}")

    def add_to_cart():
        sel = ptree.selection()
        if not sel: return messagebox.showwarning("Select", "Select a product.")
        pid = str(ptree.item(sel[0])["values"][0])
        p   = product_store.get(pid)
        try: qty = int(qty_var.get())
        except: return messagebox.showerror("Error", "Invalid quantity.")
        err = cart.add_item(p, qty)
        if err: messagebox.showerror("Error", err)
        refresh_cart()

    def remove_from_cart():
        sel = ctree.selection()
        if not sel: return messagebox.showwarning("Select", "Select a cart item.")
        name = ctree.item(sel[0])["values"][0]
        for item in cart.items:
            if item.product.name == name:
                cart.remove_item(item.product.product_id); break
        refresh_cart()

    def clear_cart():
        cart.clear(); refresh_cart()

    def checkout_dialog():
        if cart.is_empty: return messagebox.showwarning("Cart", "Cart is empty.")
        t   = cart.totals()
        amt = simpledialog.askfloat("Payment",
              f"Total: ₱{t['total']:.2f}\n\nEnter amount paid (₱):",
              minvalue=0)
        if amt is None: return
        receipt, err = billing.checkout(cart, amt)
        if err:
            messagebox.showerror("Payment Error", err)
        else:
            refresh_products(); refresh_cart()
            tab1_refresh(); tab3_refresh()
            show_receipt_popup(receipt)

    qf = tk.Frame(left, bg=BG, pady=6); qf.grid(row=2, column=0, sticky="w")
    lbl(qf, "Qty:").pack(side="left", padx=(0,6))
    entry(qf, textvariable=qty_var, width=6).pack(side="left")
    styled_btn(qf, "➕ Add to Cart", add_to_cart, GRN).pack(side="left", padx=8)

    btn_row = tk.Frame(right, bg=BG); btn_row.grid(row=3, column=0, sticky="ew", pady=4)
    styled_btn(btn_row, "🗑 Remove", lambda: remove_from_cart(), RED).pack(side="left", padx=3)
    styled_btn(btn_row, "🧹 Clear",  lambda: clear_cart(),       YLW, fg="#0f172a").pack(side="left", padx=3)
    styled_btn(btn_row, "💰 Checkout", checkout_dialog, GRN).pack(side="right", padx=3)

    refresh_products()
    return frame, refresh_products, refresh_cart

def show_receipt_popup(receipt):
    win = tk.Toplevel(); win.title("Receipt"); win.configure(bg=BG)
    win.geometry("520x560")
    txt = tk.Text(win, bg=CARD, fg=GRN, font=("Courier New", 10),
                  relief="flat", padx=10, pady=10)
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    txt.insert("1.0", ReceiptFormatter.format(receipt))
    txt.config(state="disabled")
    styled_btn(win, "Close", win.destroy, RED).pack(pady=6)

def build_inventory_tab(nb):
    frame = tk.Frame(nb, bg=BG)
    nb.add(frame, text="🏭  Inventory")
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    lbl(frame, "Inventory Management", 14, bold=True).grid(
        row=0, column=0, sticky="w", padx=14, pady=8)

    alert_var = tk.StringVar()
    alert_lbl = tk.Label(frame, textvariable=alert_var, bg=YLW, fg="#0f172a",
                         font=("Segoe UI", 10, "bold"), anchor="w", padx=10, pady=4)
    alert_lbl.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,6))

    tf = tk.Frame(frame, bg=BG, padx=10); tf.grid(row=2, column=0, sticky="nsew")
    tf.grid_rowconfigure(0, weight=1); tf.grid_columnconfigure(0, weight=1)
    COLS = ("ID", "Name", "Category", "Price (₱)", "Stock", "Status")
    tree = make_tree(tf, COLS, 16)
    tree.column("ID", width=90); tree.column("Name", width=200)

    def refresh():
        tree.delete(*tree.get_children())
        low = inventory_mgr.low_stock_alerts()
        if low:
            alert_var.set("⚠  Low stock alert: " + ", ".join(p.name for p in low))
            alert_lbl.config(bg=YLW, fg="#0f172a")
        else:
            alert_var.set("  ✅  All stock levels are healthy.")
            alert_lbl.config(bg="#166534", fg=FG)
        for p in product_store.all():
            status = "⚠ LOW" if p.is_low_stock else "OK"
            tag    = "low"   if p.is_low_stock else ""
            tree.insert("", "end", values=(
                p.product_id, p.name, p.category,
                f"{p.price:.2f}", p.quantity, status), tags=(tag,))
        tree.tag_configure("low", foreground=YLW)

    def restock():
        sel = tree.selection()
        if not sel: return messagebox.showwarning("Select", "Select a product.")
        pid = str(tree.item(sel[0])["values"][0])
        qty = simpledialog.askinteger("Restock", "Add how many units?", minvalue=1)
        if qty:
            err = inventory_mgr.restock(pid, qty)
            if err: messagebox.showerror("Error", err)
            refresh(); tab1_refresh()

    bf = tk.Frame(frame, bg=BG, pady=6); bf.grid(row=3, column=0, sticky="w", padx=10)
    styled_btn(bf, "📦 Restock Selected", restock,  GRN).pack(side="left", padx=4)
    styled_btn(bf, "🔄 Refresh",          refresh,  ACC).pack(side="left", padx=4)

    refresh()
    return frame, refresh

def build_receipts_tab(nb):
    frame = tk.Frame(nb, bg=BG)
    nb.add(frame, text="🧾  Receipts")
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    lbl(frame, "Receipt History", 14, bold=True).grid(
        row=0, column=0, sticky="w", padx=14, pady=8)

    pane = tk.PanedWindow(frame, orient="horizontal", bg=BG, sashwidth=6)
    pane.grid(row=1, column=0, sticky="nsew", padx=10)

    left = tk.Frame(pane, bg=BG); pane.add(left, width=420)
    left.grid_rowconfigure(0, weight=1); left.grid_columnconfigure(0, weight=1)
    COLS = ("Receipt ID", "Date/Time", "Total ₱", "Change ₱")
    rtree = make_tree(left, COLS, 18)
    rtree.column("Receipt ID", width=130); rtree.column("Date/Time", width=150)
    rtree.column("Total ₱", width=80); rtree.column("Change ₱", width=70)

    right = tk.Frame(pane, bg=BG); pane.add(right)
    txt = tk.Text(right, bg=CARD, fg=GRN, font=("Courier New", 9),
                  relief="flat", padx=8, pady=8, state="disabled")
    txt.pack(fill="both", expand=True)

    def refresh():
        rtree.delete(*rtree.get_children())
        for r in receipt_store.all():
            rtree.insert("", "end", values=(r.receipt_id, r.timestamp,
                                            f"{r.total:.2f}", f"{r.change:.2f}"))

    def on_select(event):
        sel = rtree.selection()
        if not sel: return
        rid = rtree.item(sel[0])["values"][0]
        r   = receipt_store.get(rid)
        if r:
            txt.config(state="normal")
            txt.delete("1.0", "end")
            txt.insert("1.0", ReceiptFormatter.format(r))
            txt.config(state="disabled")

    rtree.bind("<<TreeviewSelect>>", on_select)
    refresh()
    return frame, refresh

def build_search_tab(nb):
    frame = tk.Frame(nb, bg=BG)
    nb.add(frame, text="🔍  Search")
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    lbl(frame, "Search Products", 14, bold=True).grid(
        row=0, column=0, sticky="w", padx=14, pady=8)

    tf = tk.Frame(frame, bg=BG, padx=10); tf.grid(row=2, column=0, sticky="nsew")
    tf.grid_rowconfigure(0, weight=1); tf.grid_columnconfigure(0, weight=1)
    COLS = ("ID", "Name", "Category", "Price (₱)", "Stock", "Status")
    stree = make_tree(tf, COLS, 16)
    stree.column("ID", width=90); stree.column("Name", width=200)

    q_var = tk.StringVar()

    def do_search():
        results = search_engine.search(q_var.get())
        stree.delete(*stree.get_children())
        for p in results:
            status = "⚠ LOW" if p.is_low_stock else "OK"
            tag    = "low" if p.is_low_stock else ""
            stree.insert("", "end", values=(
                p.product_id, p.name, p.category,
                f"{p.price:.2f}", p.quantity, status), tags=(tag,))
        stree.tag_configure("low", foreground=YLW)

    sf = tk.Frame(frame, bg=BG, padx=10); sf.grid(row=1, column=0, sticky="ew", pady=(0,8))
    se = tk.Entry(sf, textvariable=q_var, width=40, bg=CARD, fg=FG,
                  insertbackground=FG, font=("Segoe UI", 12), relief="flat")
    se.pack(side="left", ipady=6, padx=(0,8))
    styled_btn(sf, "🔍 Search", do_search, ACC).pack(side="left")
    styled_btn(sf, "Show All", lambda: [q_var.set(""), do_search()], FG2, fg=BG).pack(side="left", padx=6)

    se.bind("<Return>", lambda e: do_search())
    do_search()
    return frame

def main():
    global tab1_refresh, tab2_refresh_products, tab2_refresh_cart, tab3_refresh

    root = tk.Tk()
    root.title("3_N_1 POS System")
    root.configure(bg=BG)
    root.geometry("1100x680")
    root.minsize(900, 580)

    header = tk.Frame(root, bg=ACC, height=52)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="🛒  BACTAD POS System",
             bg=ACC, fg=FG, font=("Segoe UI", 16, "bold")).pack(side="left", padx=20)
    tk.Label(header, text="Point of Sale • Inventory • Billing",
             bg=ACC, fg=ACC2, font=("Segoe UI", 9)).pack(side="right", padx=20)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook",       background=BG, borderwidth=0)
    style.configure("TNotebook.Tab",   background=CARD, foreground=FG2,
                    font=("Segoe UI", 10, "bold"), padding=[14, 8])
    style.map("TNotebook.Tab",
              background=[("selected", ACC)],
              foreground=[("selected", FG)])

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=8, pady=8)

    _, tab1_refresh                           = build_products_tab(nb)
    _, tab2_refresh_products, tab2_refresh_cart = build_billing_tab(nb)
    _, tab3_refresh                           = build_inventory_tab(nb)
    build_receipts_tab(nb)
    build_search_tab(nb)

    root.mainloop()

if __name__ == "__main__":
    main()
