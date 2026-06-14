# author : Benedict Paul Quilon
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
import turtle
import math
import time
import os
import random
from datetime import datetime

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

try:
    from PIL import Image, ImageDraw
except ImportError:
    pass

def merge_sort(arr, key=lambda x: x, reverse=False):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)

    return _merge(left, right, key, reverse)

def _merge(left, right, key, reverse):
    result = []
    i: int = 0
    j: int = 0
    while i < len(left) and j < len(right):
        val_left = key(left[i])
        val_right = key(right[j])

        if isinstance(val_left, str): val_left = val_left.lower()
        if isinstance(val_right, str): val_right = val_right.lower()

        if reverse:
            condition = val_left > val_right
        else:
            condition = val_left < val_right

        if condition:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def filtered_search(arr, search_term):

    result = []
    target = search_term.lower().strip()

    for item in arr:

        if target in item['name'].lower() or target in item['item_code'].lower() or target in item['category'].lower():
            result.append(item)

    return result

class TransactionStack:

    def __init__(self):
        self.stack = []

    def push(self, action, item):

        self.stack.append({'action': action, 'item': item})

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None

    def size(self):
        return len(self.stack)

class TextDatabase:

    def __init__(self, filename="inventory.txt"):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):

            today = datetime.now().strftime("%Y-%m-%d")
            seed_content = (
                f"ITEM101|Wireless Mouse|Electronics|1250.0|150|{today}\n"
                f"ITEM102|Mechanical Keyboard|Electronics|3500.0|45|{today}\n"
                f"ITEM103|Desk Lamp|Office|850.5|200|{today}\n"
                f"ITEM104|Ergonomic Chair|Office|4500.0|10|{today}\n"
                f"ITEM105|USB-C Hub|Accessories|1550.0|70|{today}\n"
            )
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(seed_content)

    def load_data(self):

        inventory = {}
        if not os.path.exists(self.filename):
            return inventory
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    item_code = parts[0]
                    inventory[item_code] = {
                        "item_code": parts[0],
                        "name": parts[1],
                        "category": parts[2],
                        "price": float(parts[3]),
                        "stock": int(parts[4]),
                        "date": parts[5]
                    }
        return inventory

    def save_data(self, data_dict):

        with open(self.filename, 'w', encoding='utf-8') as f:
            for item in data_dict.values():
                line = f"{item['item_code']}|{item['name']}|{item['category']}|{item['price']}|{item['stock']}|{item['date']}\n"
                f.write(line)

def draw_pie_chart(inventory_list, on_back=None):

    category_counts = {}
    total_items = 0

    for item in inventory_list:
        cat = item.get('category', 'Unknown')
        stock = int(item.get('stock', 0))
        category_counts[cat] = category_counts.get(cat, 0) + stock
        total_items += stock

    if total_items == 0:
        return

    try:
        window = tk.Toplevel()
        window.title("Inventory Distribution by Category")
        window.geometry("700x550")

        if on_back:
            def back_action():
                window.destroy()
                on_back()
            btn = tk.Button(window, text="⬅ Back to Selection", font=("Arial", 12, "bold"), bg="#1A2F24", fg="white", relief="flat", padx=10, pady=5, command=back_action)
            btn.pack(side="top", anchor="nw", padx=10, pady=10)

        window.configure(bg="#242424")
        canvas = tk.Canvas(window, width=700, height=500, highlightthickness=0, bg="#242424")
        canvas.pack(fill="both", expand=True)

        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("#242424")

        t = turtle.RawTurtle(screen)
        t.speed(0)
        t.hideturtle()
        t.pencolor("black")

        colors = ['#3EB489', '#2E8B68', '#1A2F24', '#85C1E9', '#F1C40F', '#E74C3C', '#9B59B6']

        radius = 150
        cx = -100
        cy = 0
        current_angle = 0
        color_idx = 0

        for cat, count in category_counts.items():
            arc_angle = (count / total_items) * 360

            t.fillcolor(colors[color_idx % len(colors)])
            t.begin_fill()

            t.penup()
            t.goto(cx, cy)
            t.pendown()

            t.setheading(current_angle)
            t.forward(radius)

            t.left(90)
            t.circle(radius, arc_angle)

            t.goto(cx, cy)
            t.end_fill()

            current_angle += arc_angle

            t.setheading(0)
            t.penup()
            leg_y = 150 - (color_idx * 30)
            t.goto(150, leg_y)
            t.pendown()
            t.fillcolor(colors[color_idx % len(colors)])
            t.begin_fill()
            for _ in range(4):
                t.forward(15)
                t.right(90)
            t.end_fill()

            t.pencolor("white")
            t.penup()
            t.goto(175, leg_y - 12)
            t.write(f"{cat}: {count}", align="left", font=("Arial", 12, "bold"))
            t.pencolor("black")
            t.pendown()

            color_idx += 1

    except turtle.Terminator:
        pass
    except tk.TclError:
        pass

def draw_bar_chart(inventory_list, mode="stock", on_back=None):

    category_totals = {}

    for item in inventory_list:
        cat = item.get('category', 'Unknown')
        stock = int(item.get('stock', 0))
        price = float(item.get('price', 0.0))
        val = stock if mode == "stock" else (stock * price)
        category_totals[cat] = category_totals.get(cat, 0) + val

    if not category_totals:
        return

    try:
        window = tk.Toplevel()
        title = "Total Inventory Stock by Category" if mode == "stock" else "Total Inventory Value (₱) by Category"
        window.title(title)
        window.geometry("700x550")

        if on_back:
            def back_action_bar():
                window.destroy()
                on_back()
            btn_b = tk.Button(window, text="⬅ Back to Selection", font=("Arial", 12, "bold"), bg="#1A2F24", fg="white", relief="flat", padx=10, pady=5, command=back_action_bar)
            btn_b.pack(side="top", anchor="nw", padx=10, pady=10)

        window.configure(bg="#242424")
        canvas = tk.Canvas(window, width=700, height=500, highlightthickness=0, bg="#242424")
        canvas.pack(fill="both", expand=True)

        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("#242424")
        t = turtle.RawTurtle(screen)
        t.speed(0)
        t.hideturtle()

        colors = ['#3EB489', '#2E8B68', '#1A2F24', '#85C1E9', '#F1C40F', '#E74C3C', '#9B59B6']

        max_val = float(max(category_totals.values()))
        if max_val == 0:
            max_val = 1.0

        num_bars = len(category_totals)

        x_start = -280
        y_start = -150
        max_height = 300
        total_width = 560

        t.pencolor("white")
        t.penup()
        t.goto(x_start - 20, y_start)
        t.pendown()
        t.goto(x_start + total_width + 20, y_start)

        t.penup()
        t.goto(x_start - 20, y_start)
        t.pendown()
        t.goto(x_start - 20, y_start + max_height + 40)

        t.penup()
        max_label = f"Max: ₱{max_val:,.0f}" if mode == "value" else f"Max: {int(max_val)}"
        t.goto(x_start - 30, y_start + max_height)
        t.write(max_label, align="right", font=("Arial", 10, "bold"))
        t.pencolor("black")

        if num_bars > 0:
            bar_width = (total_width / num_bars) * 0.7
            spacing = (total_width / num_bars) * 0.3
        else:
            bar_width = 50.0
            spacing = 20.0

        if bar_width > 80:
            bar_width = 80.0

        current_x = float(x_start)
        color_idx = 0

        for cat, val in category_totals.items():
            val_f = float(val)
            height = (val_f / max_val) * max_height if max_val > 0 else 0.0

            t.penup()
            t.goto(current_x, y_start)
            t.pendown()

            t.fillcolor(colors[color_idx % len(colors)])
            t.begin_fill()

            t.setheading(90)
            t.forward(height)
            t.right(90)
            t.forward(bar_width)
            t.right(90)
            t.forward(height)
            t.right(90)
            t.forward(bar_width)
            t.end_fill()

            t.penup()
            t.goto(current_x + bar_width/2, y_start - 25)
            display_cat = cat if len(cat) <= 12 else cat[:10] + ".."
            t.pencolor("white")
            t.write(display_cat, align="center", font=("Arial", 10, "bold"))
            t.pencolor("black")

            t.goto(current_x + bar_width/2, y_start + height + 5)
            val_lbl = f"₱{val:,.0f}" if mode == "value" else str(int(val))
            t.pencolor("white")
            t.write(val_lbl, align="center", font=("Arial", 9, "normal"))
            t.pencolor("black")

            current_x += bar_width + spacing
            color_idx += 1

    except turtle.Terminator:
        pass
    except tk.TclError:
        pass

def generate_static_chart(inventory_list, chart_type, filepath_out):

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    width, height = 600, 400
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    colors = ['#3EB489', '#2E8B68', '#1A2F24', '#85C1E9', '#F1C40F', '#E74C3C', '#9B59B6']

    if chart_type == "Pie":
        category_counts = {}
        total = 0
        for item in inventory_list:
            cat = item.get('category', 'Unknown')
            stock = int(item.get('stock', 0))
            category_counts[cat] = category_counts.get(cat, 0) + stock
            total += stock

        if total == 0: return False

        start_angle = 0
        color_idx = 0
        bbox = [100, 50, 400, 350]

        leg_x, leg_y = 430, 80

        for cat, cnt in category_counts.items():
            sweep = (cnt / total) * 360
            draw.pieslice(bbox, start=start_angle, end=start_angle + sweep, fill=colors[color_idx % len(colors)], outline="white")
            start_angle += sweep

            draw.rectangle([leg_x, leg_y, leg_x+15, leg_y+15], fill=colors[color_idx % len(colors)])
            draw.text((leg_x+25, leg_y), f"{cat}: {cnt}", fill="black")
            leg_y += 30
            color_idx += 1

    elif chart_type == "Bar":
        category_totals = {}
        for item in inventory_list:
            cat = item.get('category', 'Unknown')
            stock = int(item.get('stock', 0))
            category_totals[cat] = category_totals.get(cat, 0) + stock

        if not category_totals: return False
        max_val = max(category_totals.values()) if max(category_totals.values()) > 0 else 1

        num_bars = len(category_totals)
        bar_width = min((400 / num_bars) * 0.7, 80)
        spacing = (400 / num_bars) * 0.3

        x_start = 100
        y_bottom = 350
        max_height = 250

        draw.line([(x_start-10, y_bottom), (550, y_bottom)], fill="black", width=2)
        draw.line([(x_start-10, y_bottom), (x_start-10, y_bottom - max_height - 20)], fill="black", width=2)

        color_idx = 0
        current_x = x_start
        for cat, val in category_totals.items():
            h = (val / max_val) * max_height
            draw.rectangle([current_x, y_bottom - h, current_x + bar_width, y_bottom], fill=colors[color_idx % len(colors)])

            display_cat = cat if len(cat) <= 10 else cat[:8] + ".."
            draw.text((current_x, y_bottom + 10), display_cat, fill="black")
            draw.text((current_x, y_bottom - h - 15), str(val), fill="black")

            current_x += bar_width + spacing
            color_idx += 1

    img.save(filepath_out)
    return True

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

mintmain = "#3EB489"
minthover = "#2E8B68"
mintgreen = "#1A2F24"

class ProductFrame(ctk.CTkFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, fg_color=mintgreen, **kwargs)

        weights = [1, 3, 2, 1, 1, 1, 0, 0]
        for i, w in enumerate(weights):
            self.grid_columnconfigure(i, weight=w)

        self.item_lbl = ctk.CTkLabel(self, text=data['item_code'], width=100, anchor="w", text_color=mintmain, font=("Arial", 12, "bold"))
        self.item_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.name_lbl = ctk.CTkLabel(self, text=data['name'], width=200, anchor="w")
        self.name_lbl.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.cat_lbl = ctk.CTkLabel(self, text=data['category'], width=120, anchor="w")
        self.cat_lbl.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.price_lbl = ctk.CTkLabel(self, text=f"₱{data['price']:,.2f}", width=80, anchor="w")
        self.price_lbl.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.stock_lbl = ctk.CTkLabel(self, text=str(data['stock']), width=80, anchor="w", text_color=mintmain)
        self.stock_lbl.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.date_lbl = ctk.CTkLabel(self, text=data.get('date', 'N/A'), width=90, anchor="w")
        self.date_lbl.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        for child in self.winfo_children():
            child.bind("<Enter>", self.on_enter)
            child.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(fg_color="#244232")

    def on_leave(self, event):
        self.configure(fg_color=mintgreen)

class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Inventory Management System")
        # Professor required always maximized
        self.update_idletasks()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}+0+0")

        if os.path.exists("logo.ico"):
            self.iconbitmap("logo.ico")

        try:
            self.after(0, lambda: self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0"))
        except Exception:
            pass

        self.bg_canvas = tk.Canvas(self, bg="#0A110E", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.draw_turtle_background()

        self.db = TextDatabase()
        self.inventory_hashmap = self.db.load_data()
        self.undo_stack = TransactionStack()
        self.current_display_list = list(self.inventory_hashmap.values())
        self.editing_item_code = None

        self.start_loading()

    def start_loading(self):
        self.loading_box = ctk.CTkFrame(self, fg_color="#0A110E")
        self.loading_box.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.loading_label = ctk.CTkLabel(self.loading_box, text="SMART INVENTORY", font=("Helvetica", 48, "bold"), text_color=mintmain)
        self.loading_label.pack(pady=(200, 20))

        self.loading_msg = ctk.CTkLabel(self.loading_box, text="System Startup...", font=("Arial", 14), text_color="gray")
        self.loading_msg.pack(pady=10)

        self.loading_bar = ctk.CTkProgressBar(self.loading_box, width=350, height=15, progress_color=mintmain, fg_color=mintgreen)
        self.loading_bar.set(0)
        self.loading_bar.pack(pady=20)

        self.bar_progress = 0
        self.update_bar()

    def update_bar(self):
        if self.bar_progress < 1:
            self.bar_progress += 0.04
            self.loading_bar.set(self.bar_progress)
            if self.bar_progress > 0.4: self.loading_msg.configure(text="Loading Files...")
            if self.bar_progress > 0.7: self.loading_msg.configure(text="Starting UI...")
            self.after(50, self.update_bar)
        else:
            self.show_main_ui()

    def show_main_ui(self):
        self.loading_box.destroy()
        self.setup_ui()

    def setup_ui(self):

        self.dash_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dash_frame.pack(pady=(10, 0), padx=10, fill="x")

        self.card_total_items = ctk.CTkFrame(self.dash_frame, fg_color=mintgreen, corner_radius=10)
        self.card_total_items.grid(row=0, column=0, padx=5, sticky="ew")
        self.lbl_total_items_val = ctk.CTkLabel(self.card_total_items, text="0", font=("Arial", 28, "bold"), text_color="white")
        self.lbl_total_items_val.pack(pady=(10, 0))
        ctk.CTkLabel(self.card_total_items, text="Total Items", font=("Arial", 14), text_color=mintmain).pack(pady=(0, 10))

        self.card_total_value = ctk.CTkFrame(self.dash_frame, fg_color=mintgreen, corner_radius=10)
        self.card_total_value.grid(row=0, column=1, padx=5, sticky="ew")
        self.lbl_total_value_val = ctk.CTkLabel(self.card_total_value, text="₱0.00", font=("Arial", 28, "bold"), text_color="white")
        self.lbl_total_value_val.pack(pady=(10, 0))
        ctk.CTkLabel(self.card_total_value, text="Total Value (₱)", font=("Arial", 14), text_color=mintmain).pack(pady=(0, 10))

        self.card_low_stock = ctk.CTkFrame(self.dash_frame, fg_color=mintgreen, corner_radius=10)
        self.card_low_stock.grid(row=0, column=2, padx=5, sticky="ew")
        self.lbl_low_stock_val = ctk.CTkLabel(self.card_low_stock, text="0", font=("Arial", 28, "bold"), text_color="#E74C3C")
        self.lbl_low_stock_val.pack(pady=(10, 0))
        ctk.CTkLabel(self.card_low_stock, text="Low Stock Alerts", font=("Arial", 14), text_color=mintmain).pack(pady=(0, 10))

        self.dash_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, padx=10, fill="x")

        self.entry_item = ctk.CTkEntry(self.top_frame, placeholder_text="Item Code")
        self.entry_item.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ctk.CTkEntry(self.top_frame, placeholder_text="Product Name")
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)
        self.entry_cat = ctk.CTkEntry(self.top_frame, placeholder_text="Category")
        self.entry_cat.grid(row=0, column=2, padx=5, pady=5)
        self.entry_price = ctk.CTkEntry(self.top_frame, placeholder_text="Price")
        self.entry_price.grid(row=0, column=3, padx=5, pady=5)
        self.entry_stock = ctk.CTkEntry(self.top_frame, placeholder_text="Stock qty")
        self.entry_stock.grid(row=0, column=4, padx=5, pady=5)

        self.btn_add = ctk.CTkButton(self.top_frame, text="Add/Update Item", fg_color=mintmain, hover_color=minthover, text_color="black", font=("Arial", 12, "bold"), command=self.add_item)
        self.btn_add.grid(row=0, column=5, padx=5, pady=5)

        for i in range(6): self.top_frame.grid_columnconfigure(i, weight=1)

        self.mid_frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.mid_frame_top.pack(pady=2, padx=10, fill="x")

        self.entry_search = ctk.CTkEntry(self.mid_frame_top, placeholder_text="Search Anything...", width=250)
        self.entry_search.grid(row=0, column=0, padx=5, pady=5)
        self.entry_search.bind("<KeyRelease>", lambda e: self.search_item())

        self.btn_sort_name = ctk.CTkButton(self.mid_frame_top, text="Sort by Name", width=120, command=lambda: self.sort_items('name'))
        self.btn_sort_name.grid(row=0, column=2, padx=5, pady=5)
        self.btn_sort_price = ctk.CTkButton(self.mid_frame_top, text="Sort by Price", width=120, command=lambda: self.sort_items('price'))
        self.btn_sort_price.grid(row=0, column=3, padx=5, pady=5)
        self.btn_reset = ctk.CTkButton(self.mid_frame_top, text="Reset View", width=100, command=self.reset_view)
        self.btn_reset.grid(row=0, column=4, padx=5, pady=5)

        for i in range(5): self.mid_frame_top.grid_columnconfigure(i, weight=1)

        self.mid_frame_bot = ctk.CTkFrame(self, fg_color="transparent")
        self.mid_frame_bot.pack(pady=(0,5), padx=10, fill="x")

        self.btn_print = ctk.CTkButton(self.mid_frame_bot, text="Print Inventory", fg_color="#2E86C1", hover_color="#21618C", font=("Arial", 12, "bold"), width=100, command=self.show_print_options)
        self.btn_print.grid(row=0, column=0, padx=5, pady=5)

        self.chart_var = ctk.StringVar(value="Pie")
        self.rad_pie = ctk.CTkRadioButton(self.mid_frame_bot, text="Pie Chart", variable=self.chart_var, value="Pie", fg_color=mintmain)
        self.rad_pie.grid(row=0, column=2, padx=5)
        self.rad_bar = ctk.CTkRadioButton(self.mid_frame_bot, text="Bar Chart", variable=self.chart_var, value="Bar", fg_color=mintmain)
        self.rad_bar.grid(row=0, column=3, padx=5)

        self.btn_graph = ctk.CTkButton(self.mid_frame_bot, text="Show Chart", fg_color=mintmain, hover_color=minthover, text_color="black", font=("Arial", 12, "bold"), command=self.show_chart)
        self.btn_graph.grid(row=0, column=4, padx=5)

        self.btn_undo = ctk.CTkButton(self.mid_frame_bot, text="Undo", width=100, fg_color="#C0392B", command=self.undo_action)
        self.btn_undo.grid(row=0, column=5, padx=5)

        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.refresh_ui_list()

    def refresh_ui_list(self):
        total_items = len(self.inventory_hashmap)
        total_value = sum(item['price'] * item['stock'] for item in self.inventory_hashmap.values())
        low_stock = sum(1 for item in self.inventory_hashmap.values() if item['stock'] < 10)

        if hasattr(self, 'lbl_total_items_val'):
            self.lbl_total_items_val.configure(text=str(total_items))
            self.lbl_total_value_val.configure(text=f"₱{total_value:,.2f}")
            self.lbl_low_stock_val.configure(text=str(low_stock))

            for widget in self.list_frame.winfo_children(): widget.destroy()

            header = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            header.pack(fill="x", pady=2)

            weights = [1, 3, 2, 1, 1, 1, 0, 0]
            titles = ["Item Code", "Name", "Category", "Price", "Stock", "Date Added"]
            for i, (w, t) in enumerate(zip(weights, titles)):
                header.grid_columnconfigure(i, weight=w)
                color = mintmain if i in [0, 4] else "white"
                ctk.CTkLabel(header, text=t, anchor="w", font=("Arial", 14, "bold"), text_color=color).grid(row=0, column=i, padx=5, sticky="ew")

            count = 0
            for item in self.current_display_list:
                row = ProductFrame(self.list_frame, item)
                row.pack(fill="x", pady=2)
                ctk.CTkButton(row, text="Edit", width=40, command=lambda itm=item: self.load_item_to_form(itm)).grid(row=0, column=6, padx=5)
                ctk.CTkButton(row, text="X", width=30, fg_color="#C0392B", command=lambda ic=item['item_code']: self.delete_item(ic)).grid(row=0, column=7, padx=5)
                count += 1
            self.title(f"Smart Inventory Management System - {count} Items")

    def _sync_db(self):
        self.db.save_data(self.inventory_hashmap)

    def load_item_to_form(self, item):
        self.editing_item_code = item['item_code']
        for entry, val in zip([self.entry_item, self.entry_name, self.entry_cat, self.entry_price, self.entry_stock],
                                  [item['item_code'], item['name'], item['category'], str(item['price']), str(item['stock'])]):
            entry.delete(0, 'end')
            entry.insert(0, val)

    def add_item(self):
        code, name, cat = self.entry_item.get().strip(), self.entry_name.get().strip(), self.entry_cat.get().strip()
        try:
            price, stock = float(self.entry_price.get()), int(self.entry_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Check numeric fields.")
            return

        if not code or not name:
            messagebox.showerror("Error", "Code/Name required.")
            return

        old_item = None
        if self.editing_item_code and self.editing_item_code in self.inventory_hashmap:
            old_item = self.inventory_hashmap[self.editing_item_code]
            if self.editing_item_code != code:
                if code in self.inventory_hashmap:
                    messagebox.showerror("Error", "Code already exists.")
                    return
                del self.inventory_hashmap[self.editing_item_code]
        else:
            old_item = self.inventory_hashmap.get(code)

        new_item = {"item_code": code, "name": name, "category": cat, "price": price, "stock": stock,
                    "date": old_item["date"] if old_item else datetime.now().strftime("%Y-%m-%d")}

        self.inventory_hashmap[code] = new_item
        self._sync_db()
        self.undo_stack.push("UPDATE" if old_item else "ADD", {"old": old_item, "new": new_item} if old_item else new_item)
        self.editing_item_code = None
        self.reset_view()
        for entry in [self.entry_item, self.entry_name, self.entry_cat, self.entry_price, self.entry_stock]: entry.delete(0, 'end')

    def delete_item(self, code):
        if code in self.inventory_hashmap:
            deleted = self.inventory_hashmap.pop(code)
            self._sync_db()
            self.undo_stack.push("DELETE", deleted)
            self.reset_view()

    def undo_action(self):
        action = self.undo_stack.pop()
        if not action: return
        t, item = action['action'], action['item']
        if t == "ADD":
            if item['item_code'] in self.inventory_hashmap: del self.inventory_hashmap[item['item_code']]
        elif t == "DELETE":
            self.inventory_hashmap[item['item_code']] = item
        elif t == "UPDATE":
            old, new = item['old'], item['new']
            if new['item_code'] in self.inventory_hashmap: del self.inventory_hashmap[new['item_code']]
            self.inventory_hashmap[old['item_code']] = old
        self._sync_db()
        self.reset_view()

    def sort_items(self, criteria):
        self.current_display_list = merge_sort(list(self.inventory_hashmap.values()), key=lambda x: x[criteria])
        self.refresh_ui_list()
    
    def draw_turtle_background(self):
        screen = turtle.TurtleScreen(self.bg_canvas)
        screen.bgcolor("#0A110E")
        screen.tracer(0, 0)
        t = turtle.RawTurtle(screen)
        t.hideturtle()
        t.speed(0)
        R = 40
        dx, dy = math.sqrt(3) * R, 1.5 * R
        width, height = 2400, 1400
        cols, rows = int(width / dx) + 2, int(height / dy) + 2
        start_x, start_y = -width/2, height/2
        random.seed(101)
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * dx + (dx/2 if row % 2 != 0 else 0)
                y = start_y - row * dy
                if random.random() < 0.25: continue
                t.pencolor(random.choice(["#12221A", "#1A3A2F", "#2E8B68", "#3EB489"]))
                fill = random.random() < 0.08
                if fill: t.fillcolor("#0E1A14")
                t.penup()
                for i in range(7):
                    angle_rad = math.pi / 180 * (60 * (i%6) + 30)
                    hx, hy = x + R * math.cos(angle_rad), y + R * math.sin(angle_rad)
                    if i == 0:
                        t.goto(hx, hy)
                        if fill: t.begin_fill()
                        t.pendown()
                    else: t.goto(hx, hy)
                if fill: t.end_fill()
                if random.random() < 0.15:
                    t.penup(); t.goto(x, y); t.dot(random.choice([3, 4, 5]), "#3EB489")
        screen.update()

    def search_item(self):
        target = self.entry_search.get().strip()
        if not target:
            self.reset_view()
            return
        found = filtered_search(list(self.inventory_hashmap.values()), target)
        self.current_display_list = merge_sort(found, key=lambda x: x['name']) if found else []
        self.refresh_ui_list()

    def show_chart(self):
        sel = self.chart_var.get()
        if sel == "Pie": draw_pie_chart(list(self.inventory_hashmap.values()))
        else: draw_bar_chart(list(self.inventory_hashmap.values()), mode="stock")

    def show_print_options(self):
        prt = ctk.CTkToplevel(self)
        prt.title("Print Options")
        prt.geometry("380x350")
        prt.transient(self)
        ctk.CTkLabel(prt, text="PDF Settings", font=("Arial", 16, "bold"), text_color=mintmain).pack(pady=10)
        self.pdf_paper_var = ctk.StringVar(value="A4")
        ctk.CTkOptionMenu(prt, variable=self.pdf_paper_var, values=["A4", "Letter", "Legal"]).pack(pady=5)
        self.pdf_chart_var = ctk.StringVar(value="None")
        f = ctk.CTkFrame(prt, fg_color="transparent")
        f.pack(pady=5)
        for v in ["None", "Pie", "Bar"]: ctk.CTkRadioButton(f, text=v, variable=self.pdf_chart_var, value=v).pack(side="left", padx=5)
        ctk.CTkButton(prt, text="Generate PDF", command=lambda: [prt.destroy(), self.generate_pdf(True, self.pdf_chart_var.get(), self.pdf_paper_var.get())]).pack(pady=20)

    def generate_pdf(self, open_file=False, chart_type="None", paper_size="A4"):
        if FPDF is None:
            messagebox.showerror("Error", "FPDF not installed.")
            return
        pdf = FPDF(format=paper_size.lower())
        pdf.add_page(); pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Inventory Report", 0, 1, 'C')
        pdf.set_font("Arial", 'I', 10); pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C')
        if chart_type in ["Pie", "Bar"]:
            temp = "chart_temp.png"
            if generate_static_chart(self.current_display_list, chart_type, temp):
                pdf.image(temp, x=30, w=150); pdf.ln(5)
                try: os.remove(temp)
                except: pass
        pdf.set_font("Arial", 'B', 11); w = [30, 60, 40, 30, 30]
        for h, width in zip(["Code", "Name", "Category", "Price", "Stock"], w): pdf.cell(width, 10, h, 1, 0, 'C')
        pdf.ln(); pdf.set_font("Arial", '', 10)
        for item in self.current_display_list:
            pdf.cell(w[0], 10, str(item['item_code']), 1)
            pdf.cell(w[1], 10, (item['name'][:22] if len(item['name']) < 25 else item['name'][:22]+"..."), 1)
            pdf.cell(w[2], 10, str(item['category']), 1)
            pdf.cell(w[3], 10, f"{item['price']:.2f}", 1, 0, 'R')
            pdf.cell(w[4], 10, str(item['stock']), 1, 0, 'C'); pdf.ln()
        f_name = "Inventory_Report.pdf"
        try:
            pdf.output(f_name)
            if open_file: os.startfile(os.path.abspath(f_name))
        except Exception as e: messagebox.showerror("Error", str(e))

    def reset_view(self):
        self.current_display_list = list(self.inventory_hashmap.values())
        self.refresh_ui_list()

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
