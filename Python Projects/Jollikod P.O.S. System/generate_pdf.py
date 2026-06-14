"""
generate_pdf.py — JolliKod: Kanto Style Fastfood
Generates a UI/UX documentation PDF using reportlab.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import PageBreak
import datetime
import os

# ── Brand Colors ──────────────────────────────────────────────────────────────
JRED    = colors.HexColor("#CC0000")
DKRED   = colors.HexColor("#8B0000")
YELLOW  = colors.HexColor("#FFD700")
AMBER   = colors.HexColor("#E65100")
GREEN   = colors.HexColor("#2E7D32")
GRAY    = colors.HexColor("#757575")
LTGRAY  = colors.HexColor("#F5F5F5")
DARKBG  = colors.HexColor("#1A0000")
WHITE   = colors.white
BLACK   = colors.black

W, H = A4

OUTPUT = os.path.join(os.path.dirname(__file__), "JolliKod_UIUX_Documentation.pdf")


# ── Custom Styles ─────────────────────────────────────────────────────────────

def make_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title", fontSize=38, fontName="Helvetica-Bold",
            textColor=YELLOW, alignment=TA_CENTER, spaceAfter=6
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", fontSize=16, fontName="Helvetica-Oblique",
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=4
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta", fontSize=11, fontName="Helvetica",
            textColor=LTGRAY, alignment=TA_CENTER
        ),
        "section": ParagraphStyle(
            "section", fontSize=16, fontName="Helvetica-Bold",
            textColor=JRED, spaceBefore=18, spaceAfter=6,
            borderPad=4
        ),
        "subsection": ParagraphStyle(
            "subsection", fontSize=12, fontName="Helvetica-Bold",
            textColor=DKRED, spaceBefore=10, spaceAfter=4
        ),
        "body": ParagraphStyle(
            "body", fontSize=10, fontName="Helvetica",
            textColor=BLACK, leading=15, alignment=TA_JUSTIFY,
            spaceAfter=6
        ),
        "bullet": ParagraphStyle(
            "bullet", fontSize=10, fontName="Helvetica",
            textColor=BLACK, leading=14, leftIndent=18,
            bulletIndent=6, spaceAfter=3
        ),
        "code": ParagraphStyle(
            "code", fontSize=9, fontName="Courier",
            textColor=colors.HexColor("#1A0000"),
            backColor=colors.HexColor("#FFF8E1"),
            borderPad=4, leading=13, spaceAfter=6
        ),
        "caption": ParagraphStyle(
            "caption", fontSize=8, fontName="Helvetica-Oblique",
            textColor=GRAY, alignment=TA_CENTER, spaceAfter=4
        ),
        "highlight": ParagraphStyle(
            "highlight", fontSize=10, fontName="Helvetica-Bold",
            textColor=DKRED, spaceAfter=4
        ),
    }
    return styles


# ── Cover Page ────────────────────────────────────────────────────────────────

def cover_page(styles):
    elems = []

    # Red header block simulated with a colored table
    cover_data = [[Paragraph("JolliKod", styles["cover_title"])]]
    cover_tbl = Table(cover_data, colWidths=[16*cm])
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), JRED),
        ("TOPPADDING",    (0, 0), (-1, -1), 28),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 28),
        ("ROUNDEDCORNERS", [8]),
    ]))
    elems.append(Spacer(1, 1.5*cm))
    elems.append(cover_tbl)

    sub_data = [[Paragraph('"Kanto Style Fastfood"', styles["cover_sub"])]]
    sub_tbl = Table(sub_data, colWidths=[16*cm])
    sub_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DKRED),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elems.append(sub_tbl)
    elems.append(Spacer(1, 1*cm))

    # Gold divider
    elems.append(HRFlowable(width="100%", thickness=4, color=YELLOW))
    elems.append(Spacer(1, 0.5*cm))

    doc_title = Paragraph("UI/UX Design Documentation", ParagraphStyle(
        "dt", fontSize=20, fontName="Helvetica-Bold",
        textColor=DKRED, alignment=TA_CENTER))
    elems.append(doc_title)
    elems.append(Spacer(1, 0.4*cm))

    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    meta = Paragraph(
        f"Version 1.0  •  Generated: {date_str}<br/>"
        "Subject: Real-Time Ordering System Design<br/>"
        "Platform: Python 3 / Turtle Graphics",
        ParagraphStyle("meta2", fontSize=10, fontName="Helvetica",
                       textColor=GRAY, alignment=TA_CENTER, leading=16)
    )
    elems.append(meta)
    elems.append(Spacer(1, 1.2*cm))
    elems.append(HRFlowable(width="100%", thickness=2, color=JRED))
    elems.append(Spacer(1, 0.5*cm))

    # Summary box
    summary_data = [[Paragraph(
        "<b>Executive Summary</b><br/><br/>"
        "JolliKod is a Python-based real-time fastfood ordering and queue management system "
        "inspired by the iconic Jollibee visual identity. Built entirely with Python's "
        "Turtle Graphics library, it demonstrates how classic computer graphics primitives "
        "can power a functional, animated, and visually rich application without any "
        "third-party UI framework. The system solves the real-world problem of kitchen "
        "queue transparency by surfacing live cook timers, automatic status transitions, "
        "and a precision-sorted preparing queue.",
        ParagraphStyle("ex", fontSize=10, fontName="Helvetica",
                       textColor=BLACK, leading=15, alignment=TA_JUSTIFY)
    )]]
    s_tbl = Table(summary_data, colWidths=[16*cm])
    s_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#FFF8E1")),
        ("BOX",           (0, 0), (-1, -1), 1.5, YELLOW),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
    ]))
    elems.append(s_tbl)
    elems.append(PageBreak())
    return elems


# ── Section builder ───────────────────────────────────────────────────────────

def section(title, body_paras, styles):
    elems = []
    elems.append(HRFlowable(width="100%", thickness=1.5, color=JRED))
    elems.append(Paragraph(title, styles["section"]))
    elems.extend(body_paras)
    elems.append(Spacer(1, 0.3*cm))
    return elems


def bullet_list(items, styles):
    return [Paragraph(f"• {item}", styles["bullet"]) for item in items]


def info_table(rows, col_labels, styles):
    data = [col_labels] + rows
    t = Table(data, colWidths=[4.5*cm, 11.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),   JRED),
        ("TEXTCOLOR",     (0, 0), (-1, 0),   WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),   "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1),  9),
        ("FONTNAME",      (0, 1), (-1, -1),  "Helvetica"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),  [LTGRAY, WHITE]),
        ("BOX",           (0, 0), (-1, -1),  0.8, GRAY),
        ("INNERGRID",     (0, 0), (-1, -1),  0.4, GRAY),
        ("TOPPADDING",    (0, 0), (-1, -1),  5),
        ("BOTTOMPADDING", (0, 0), (-1, -1),  5),
        ("LEFTPADDING",   (0, 0), (-1, -1),  8),
    ]))
    return t


# ── Content Sections ──────────────────────────────────────────────────────────

def build_content(styles):
    B = styles["body"]
    S = styles["subsection"]
    H = styles["highlight"]
    elems = []

    # ── 1. Problem Statement ──────────────────────────────────────────────────
    elems += section("1. Problem Statement", [
        Paragraph(
            "Traditional kanto (street-corner) fastfood stalls and small eateries suffer "
            "from three compounding operational problems:", B),
        *bullet_list([
            "<b>No queue visibility</b> — Customers and staff have no reliable way to know "
            "which orders are cooking, how long remains, and which are ready.",
            "<b>Order confusion</b> — Multiple concurrent orders from different customers "
            "are tracked mentally, leading to mix-ups and delays.",
            "<b>Inefficient delivery handoff</b> — Staff forget to call customers when "
            "food is ready, resulting in cold food and customer dissatisfaction.",
        ], styles),
        Spacer(1, 0.2*cm),
        Paragraph(
            "JolliKod directly addresses each of these by providing a <b>real-time, "
            "automated order queue</b> with live countdown timers, automatic status "
            "promotion, and a one-click delivery handoff.", B),
    ], styles)

    # ── 2. App Goals ──────────────────────────────────────────────────────────
    elems += section("2. Application Goals", [
        Paragraph("The application targets three stakeholder goals:", B),
        Spacer(1, 0.1*cm),
        info_table([
            ["Kitchen Staff",   "See all active orders sorted by cook time remaining so they can attend to the most urgent ones first."],
            ["Cashier / Order Taker", "Quickly add items to a cart, enter a customer name, and place the order with two taps."],
            ["Students / Educators", "Demonstrate real-time threading, queue data structures, and sorting algorithms in a visual, motivating context."],
        ], ["Stakeholder", "Goal"], styles),
        Spacer(1, 0.3*cm),
        Paragraph(
            "Secondary goals include showcasing that Python's built-in Turtle Graphics "
            "module is capable of rendering a functional, styled UI — challenging the "
            "assumption that Turtle is only for beginner drawing exercises.", B),
    ], styles)

    # ── 3. UI Layout & Design ─────────────────────────────────────────────────
    elems += section("3. UI Layout & Design System", [
        Paragraph(S.name, S),  # placeholder trick
        Paragraph("<b>3.1  Screen Layout (1300 × 800 px)</b>", S),
        Paragraph(
            "The canvas is divided into two vertical panels separated by a 10-pixel gutter:", B),
        info_table([
            ["Header (full width)", "App brand bar — JolliKod logo, subtitle, animated bee mascots, gold stripe."],
            ["Left Panel (640 px)", "ORDER MENU — five clickable item cards, cart summary, CLEAR / PLACE ORDER actions."],
            ["Right Panel (650 px)", "LIVE ORDER QUEUE — three stacked sections: Preparing, Ready to Serve, Delivered."],
            ["Stats Bar (bottom)", "Real-time counter strip: Total / Preparing / Ready / Delivered order counts."],
        ], ["Region", "Purpose"], styles),

        Spacer(1, 0.3*cm),
        Paragraph("<b>3.2  Color System (Jollibee-Inspired)</b>", S),
        info_table([
            ["#CC0000  —  Red",     "Primary brand color. Header background, section borders, ADD button accents."],
            ["#FFD700  —  Gold",    "Jollibee gold. Logo text, prices, cart totals, header stripe, CTA buttons."],
            ["#E65100  —  Amber",   "PREPARING section. Conveys urgency — food is actively cooking."],
            ["#2E7D32  —  Green",   "READY TO SERVE. Positive signal — food is done, deliver now."],
            ["#757575  —  Gray",    "DELIVERED section. Neutral — order lifecycle is complete."],
            ["#1A0000  —  Near-black", "Canvas background. Maximises contrast with red/gold foreground."],
        ], ["Color Token", "Usage"], styles),

        Spacer(1, 0.3*cm),
        Paragraph("<b>3.3  Typography</b>", S),
        *bullet_list([
            "All text rendered via Turtle's <i>turtle.write()</i> using <b>Arial</b> — the closest cross-platform "
            "equivalent to Helvetica Neue available without font installation.",
            "Font sizes range from 8 pt (badge labels) to 34 pt (hero logo), giving a clear visual hierarchy.",
            "Bold weight used for order IDs, customer names, prices, and section headers.",
            "Italic used for the brand tagline and empty-state messages.",
        ], styles),
    ], styles)

    # ── 4. UX Flow ────────────────────────────────────────────────────────────
    elems += section("4. User Experience Flow", [
        Paragraph(
            "The entire ordering lifecycle is a linear five-step flow with zero navigation "
            "between screens — everything is visible simultaneously on one canvas:", B),
        Spacer(1, 0.2*cm),
        info_table([
            ["Step 1 — Browse", "Staff scans left panel. Each menu card shows item name, price, and cook time at a glance."],
            ["Step 2 — Add to Cart", "Click '+ ADD' button on any card. Cart updates immediately showing quantities and running total."],
            ["Step 3 — Place Order", "Click 'PLACE ORDER'. A dialog asks for the customer name. Submission creates the order."],
            ["Step 4 — Preparing", "Order appears in the PREPARING queue with a live MM:SS countdown. Timer ticks every second."],
            ["Step 5 — Ready → Deliver", "When timer hits 00:00, order auto-moves to READY TO SERVE. Staff clicks DELIVER."],
            ["Step 6 — Delivered", "Order moves to DELIVERED section. Receipt is complete. Stats bar updates."],
        ], ["Step", "Description"], styles),

        Spacer(1, 0.3*cm),
        Paragraph("<b>Design Decisions for UX Clarity</b>", S),
        *bullet_list([
            "Single-canvas design eliminates navigation — staff sees the full state at once.",
            "Color-coded status sections (amber / green / gray) allow status recognition in peripheral vision.",
            "Countdown timers prevent staff from constantly checking the kitchen — they know exactly when to look.",
            "Insertion-sort on the PREPARING queue keeps the most urgent order always at the top.",
            "Empty-state messages ('No orders ready yet…') prevent confusion when sections are empty.",
        ], styles),
    ], styles)

    # ── 5. Algorithm: Insertion Sort ─────────────────────────────────────────
    elems += section("5. Algorithm: Insertion Sort for Queue Precision", [
        Paragraph(
            "The PREPARING queue uses <b>Insertion Sort</b> to order active cooking orders "
            "by their remaining cook time (ascending). This ensures the order closest to "
            "completion is always displayed at the top of the queue panel.", B),

        Paragraph("<b>Why Insertion Sort?</b>", S),
        *bullet_list([
            "<b>Small input size</b> — A real-world kitchen rarely handles more than 8–10 "
            "simultaneous orders. Insertion sort's O(n²) worst case is negligible at this scale.",
            "<b>Nearly-sorted input</b> — After each one-second tick, only one value "
            "(remaining_sec) decreases by 1. The list is almost already sorted, making "
            "insertion sort approach O(n) — its best case performance.",
            "<b>Stable sort</b> — Orders with equal remaining time preserve their arrival "
            "order (FIFO), which is the fairest tie-breaking rule.",
            "<b>Pedagogical clarity</b> — The algorithm is easy to trace step-by-step, "
            "making it ideal for a school/teaching demonstration.",
        ], styles),

        Spacer(1, 0.2*cm),
        Paragraph("<b>Pseudocode</b>", S),
        Paragraph(
            "for i from 1 to n-1:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;key = arr[i]<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;j = i - 1<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;while j >= 0 and arr[j].remaining_sec > key.remaining_sec:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arr[j+1] = arr[j]<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;j -= 1<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;arr[j+1] = key",
            styles["code"]),

        Paragraph("<b>Worked Example</b>", S),
        Paragraph(
            "Given three concurrent orders with remaining times [18, 7, 12]:", B),
        info_table([
            ["Pass 1 (i=1)", "[18, 7, 12]  →  key=7;  18>7 so shift  →  [7, 18, 12]"],
            ["Pass 2 (i=2)", "[7, 18, 12]  →  key=12; 18>12 so shift →  [7, 12, 18]"],
            ["Result",       "[7, 12, 18]  —  Order with 7 s remaining shown first ✓"],
        ], ["Pass", "State"], styles),
        Spacer(1, 0.1*cm),
        Paragraph(
            "The kitchen staff immediately sees the most urgent order (7 s) at the top "
            "of the PREPARING panel without any manual intervention.", B),
    ], styles)

    # ── 6. Architecture ───────────────────────────────────────────────────────
    elems += section("6. System Architecture", [
        Paragraph(
            "The project is intentionally split into <b>three Python files</b> following "
            "a simplified MVC (Model-View-Controller) pattern:", B),
        info_table([
            ["models.py",        "Data layer. Defines MenuItem, Order, OrderStatus enum, and MENU_CATALOGUE. No UI or logic dependencies."],
            ["queue_manager.py", "Controller / Engine. Manages order state transitions, background tick thread, and insertion sort. No UI dependency."],
            ["main.py",          "View. Turtle Graphics UI, click handling, dynamic refresh loop via ontimer(). Imports both models and queue_manager."],
        ], ["File", "Responsibility"], styles),

        Spacer(1, 0.3*cm),
        Paragraph("<b>Threading Model</b>", S),
        *bullet_list([
            "<b>Main thread</b> — Runs the Turtle screen event loop (mainloop). Handles all drawing and click events.",
            "<b>Background tick thread</b> (daemon) — Sleeps 1 second per iteration, decrements remaining_sec for each PREPARING order, calls _mark_ready() when timer expires.",
            "<b>Thread safety</b> — All reads/writes to the shared orders list are guarded by a threading.Lock() to prevent race conditions.",
            "<b>Refresh loop</b> — screen.ontimer(callback, 1000) re-draws the right panel every second from the main thread, ensuring Turtle is never called from the background thread.",
        ], styles),
    ], styles)

    # ── 7. Menu Catalogue ─────────────────────────────────────────────────────
    elems += section("7. Menu Catalogue", [
        Paragraph(
            "Five items are available at launch, covering the core kanto fastfood categories:", B),
        info_table([
            ["Jollikod Fries",        "₱59",  "10 s", "F"],
            ["Kanto Fried Chicken",   "₱129", "20 s", "C"],
            ["Kanto Burger",          "₱89",  "15 s", "B"],
            ["Streetside Rice Meal",  "₱75",  "12 s", "R"],
            ["Kanto Spaghetti",       "₱95",  "18 s", "S"],
        ],
        ["Item Name", "Price", "Cook Time", "Badge"], styles),
        Spacer(1, 0.2*cm),
        Paragraph(
            "Cook times are expressed in seconds for live demonstration purposes. "
            "In a production deployment these would map to real minutes "
            "(e.g. Fries = 10 min, Fried Chicken = 20 min).", B),
    ], styles)

    # ── 8. Future Improvements ────────────────────────────────────────────────
    elems += section("8. Future Improvements", [
        *bullet_list([
            "<b>Sound alerts</b> — Play a chime when an order transitions to READY TO SERVE.",
            "<b>Receipt printing</b> — Generate a text-based receipt per order with order ID, items, and total.",
            "<b>Multi-station support</b> — Allow separate cashier and kitchen views on different windows.",
            "<b>Persistent storage</b> — Save order history to SQLite for end-of-day reporting.",
            "<b>Priority orders</b> — Flag VIP or senior citizen orders for queue bumping.",
            "<b>Touch screen mode</b> — Larger hit targets for tablet/kiosk deployment.",
            "<b>Fractional cook timers</b> — Display tenths of seconds for very short-cook items.",
        ], styles),
    ], styles)

    return elems


# ── Page Template ─────────────────────────────────────────────────────────────

def draw_page_decoration(canvas, doc):
    canvas.saveState()
    # Header stripe
    canvas.setFillColor(JRED)
    canvas.rect(0, H - 1*cm, W, 1*cm, fill=1, stroke=0)
    canvas.setFillColor(YELLOW)
    canvas.rect(0, H - 1*cm - 4, W, 4, fill=1, stroke=0)
    # Header text
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(WHITE)
    canvas.drawString(1.5*cm, H - 0.7*cm, "JolliKod — Kanto Style Fastfood")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(W - 1.5*cm, H - 0.7*cm, "UI/UX Documentation")
    # Footer
    canvas.setFillColor(DKRED)
    canvas.rect(0, 0, W, 0.8*cm, fill=1, stroke=0)
    canvas.setFillColor(YELLOW)
    canvas.rect(0, 0.8*cm, W, 3, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(WHITE)
    canvas.drawString(1.5*cm, 0.25*cm, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    canvas.drawCentredString(W / 2, 0.25*cm, f"Page {doc.page}")
    canvas.drawRightString(W - 1.5*cm, 0.25*cm, "Confidential — School Project")
    canvas.restoreState()


# ── Build PDF ─────────────────────────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=1.8*cm,   bottomMargin=1.5*cm,
        title="JolliKod UI/UX Documentation",
        author="JolliKod Dev Team",
        subject="Kanto Style Fastfood — Ordering System Design",
    )

    styles = make_styles()
    story  = []
    story += cover_page(styles)
    story += build_content(styles)

    doc.build(story, onFirstPage=draw_page_decoration,
                     onLaterPages=draw_page_decoration)
    print(f"[OK] PDF saved to: {OUTPUT}")
    # Auto-open the PDF on Windows
    import subprocess
    subprocess.Popen(["start", "", OUTPUT], shell=True)
    return OUTPUT


if __name__ == "__main__":
    build_pdf()
