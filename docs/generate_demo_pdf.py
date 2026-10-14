"""Generate the three-page project brief from local screenshots and seed totals."""

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
OUTPUT = ROOT / "output" / "pdf" / "E-Commerce-Project-Overview.pdf"
SUMMARY = json.loads((ROOT / "docs" / "demo-data-summary.json").read_text())
COUNTS = SUMMARY["demo_counts"]
VALUE = SUMMARY["demo_order_value"]
W, H = A4
M = 38
CW = W - 2 * M
INK = colors.HexColor("#142638")
TEAL = colors.HexColor("#087E8B")
MUTED = colors.HexColor("#526475")
LINE = colors.HexColor("#D9E4E9")
MINT = colors.HexColor("#E9F6F4")
PALE = colors.HexColor("#F3F7FA")
WHITE = colors.white

FONT_ROOT = Path("C:/Windows/Fonts")
if (FONT_ROOT / "segoeui.ttf").exists():
    pdfmetrics.registerFont(TTFont("Body", str(FONT_ROOT / "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("Bold", str(FONT_ROOT / "segoeuib.ttf")))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Bold", italic="Body", boldItalic="Bold")
else:
    pdfmetrics.registerFontFamily("Helvetica", normal="Helvetica", bold="Helvetica-Bold")
FONT = "Body" if "Body" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
BOLD = "Bold" if FONT == "Body" else "Helvetica-Bold"


def text(c, value, x, top, size=11, color=INK, bold=False):
    c.setFillColor(color)
    c.setFont(BOLD if bold else FONT, size)
    c.drawString(x, H - top - size, value)


def paragraph(c, value, x, top, width, size=10.4, color=MUTED, leading=None):
    style = ParagraphStyle("p", fontName=FONT, fontSize=size,
                           leading=leading or size * 1.42, textColor=color, alignment=TA_LEFT)
    p = Paragraph(value, style)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, H - top - height)
    return height


def box(c, x, top, width, height, fill=PALE, stroke=None, radius=12):
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.roundRect(x, H - top - height, width, height, radius, fill=1, stroke=bool(stroke))


def rule(c, top, x=M, width=CW):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(x, H - top, x + width, H - top)


def page(c, number, label):
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 8, W, 8, fill=1, stroke=0)
    text(c, "ECOMMERCE AI  /  PROJECT BRIEF", M, 30, 8.4, TEAL, True)
    text(c, "11 OCT 2026", W - M - 78, 30, 8.4, MUTED)
    rule(c, 798)
    text(c, "LOCAL DEMO  |  " + label, M, 808, 7.4, MUTED)
    text(c, f"{number} / 3", W - M - 28, 808, 8, TEAL, True)


def image(c, filename, x, top, width, height):
    source = ImageReader(str(ASSETS / filename))
    sw, sh = source.getSize()
    scale = min(width / sw, height / sh)
    dw, dh = sw * scale, sh * scale
    c.drawImage(source, x + (width - dw) / 2, H - top - dh,
                dw, dh, mask="auto")
    return dh


def arrow(c, x, top):
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    y = H - top
    c.line(x, y, x + 17, y)
    c.line(x + 12, y + 4, x + 17, y)
    c.line(x + 12, y - 4, x + 17, y)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("eCommerce AI - Project Scope, Demo Data and Solution")
    c.setAuthor("eCommerce AI project")
    c.setSubject("Three-page illustrated project brief with real local app screenshots")

    page(c, 1, "PROBLEM & SCOPE")
    text(c, "eCommerce AI", M, 66, 34, INK, True)
    text(c, "From empty screens to a working store demo", M, 115, 15, TEAL)
    paragraph(c, "A local commerce prototype that brings catalog, stock, orders and pricing "
              "experiments into one interface for store operators and project reviewers.",
              M, 153, CW, 11.2)

    gap = 16
    col = (CW - gap) / 2
    box(c, M, 217, col, 141, PALE)
    box(c, M + col + gap, 217, col, 141, MINT)
    text(c, "THE PROBLEM", M + 16, 232, 9.6, MUTED, True)
    paragraph(c, "Store information is hard to evaluate when products, stock and orders "
              "are disconnected. In this prototype, empty lists also made the dashboard "
              "and pricing tools impossible to demonstrate meaningfully.",
              M + 16, 258, col - 32, 10.5)
    text(c, "THE SOLUTION", M + col + gap + 16, 232, 9.6, TEAL, True)
    paragraph(c, "Use one React interface and one local API, backed by linked SQLite records. "
              "Synthetic demo data now fills the operational screens and supports a "
              "repeatable, transparent pricing walkthrough.",
              M + col + gap + 16, 258, col - 32, 10.5)

    text(c, "How it works", M, 388, 17, INK, True)
    bw = (CW - 54) / 3
    for index, (title, subtitle) in enumerate([
        ("React admin UI", "Catalog, dashboard, orders"),
        ("Express / Node API", "CRUD and pricing rules"),
        ("SQLite database", "Products, users, order items"),
    ]):
        x = M + index * (bw + 27)
        box(c, x, 425, bw, 77, MINT if index == 1 else PALE, LINE)
        text(c, title, x + 12, 442, 10.5, INK, True)
        paragraph(c, subtitle, x + 12, 465, bw - 24, 8.7)
        if index < 2:
            arrow(c, x + bw + 5, 464)
    paragraph(c, "UI and API share <b>http://localhost:6220</b>. The FastAPI/Django alternatives "
              "and shared Python AI modules are separate examples, outside this running demo.",
              M, 517, CW, 9.4)

    text(c, "Scope of the current demonstration", M, 569, 17, INK, True)
    rows = [
        ("Catalog & inventory", "View products, prices, categories and stock; create, edit and delete products."),
        ("Orders & dashboard", "Inspect orders and line items; compute product/order counts and total order value."),
        ("Pricing sandbox", "Preview a price using demand, stock and competitor inputs; the catalog price is unchanged."),
        ("Demo accounts & data", "Registration/basic login APIs and persistent sample records; prototype sign-in UI."),
    ]
    y = 610
    for index, (name, detail) in enumerate(rows):
        if index % 2 == 0:
            box(c, M, y - 2, CW, 39, PALE, radius=4)
        text(c, name, M + 10, y + 4, 9.5, INK, True)
        paragraph(c, detail, M + 164, y + 2, CW - 174, 9.0)
        y += 43
    c.showPage()

    page(c, 2, "DEMO DATA & SCREENS")
    text(c, "A store you can explore", M, 65, 27, INK, True)
    paragraph(c, "All people, purchases and reviews are fictional. The dataset includes "
              "six product categories, 36 linked order items, and 10 stored reviews "
              "(reviews have no screen in the current UI).", M, 111, CW, 10.7)

    card_width = (CW - 30) / 4
    for index, (value, label) in enumerate([
        (str(COUNTS["products"]), "PRODUCTS"), (str(COUNTS["orders"]), "ORDERS"),
        (str(COUNTS["users"]), "DEMO ACCOUNTS"), (f"${VALUE:,.2f}", "ORDER VALUE"),
    ]):
        x = M + index * (card_width + 10)
        box(c, x, 174, card_width, 74, MINT if index == 3 else PALE)
        text(c, value, x + 12, 189, 20 if index < 3 else 16, INK, True)
        text(c, label, x + 12, 224, 7.3, TEAL, True)
    paragraph(c, "Average order value: <b>$127.97</b>. The total includes every order status; "
              "it is sample order value, not settled payments.", M, 263, CW, 9.4)

    text(c, "Real screens from the populated demo", M, 307, 16, INK, True)
    image(c, "dashboard-metrics.jpg", M, 346, col, 237)
    image(c, "order-detail.jpg", M + col + gap, 346, col, 237)
    paragraph(c, "<b>Dashboard:</b> counts and order value come from SQLite through the API. "
              "The displayed 98% coverage is a placeholder.", M, 592, col, 9.2)
    paragraph(c, "<b>Order #16:</b> smartwatch $129 + backpack $54 + organizer $22 = $205. "
              "The screen shows quantities and fulfillment status.", M + col + gap, 592, col, 9.2)

    text(c, "Scenarios worth demonstrating", M, 654, 14, INK, True)
    paragraph(c, "<b>Stock pressure:</b> Pulse Smartwatch has 3 units; Connect USB-C Hub has 0. "
              "<b>Fulfillment:</b> 8 delivered, 4 shipped, 2 processing and 2 pending orders. "
              "<b>Accounts:</b> one demo admin and eight synthetic customers.",
              M, 681, CW, 9.5)
    box(c, M, 744, CW, 38, MINT, radius=7)
    text(c, "OPEN  localhost:6220/dashboard", M + 12, 751, 9, TEAL, True)
    text(c, "RESEED  python tools/seed_demo_data.py  (safe to rerun)", M + 12, 765, 8.1, MUTED)
    c.showPage()

    page(c, 3, "PRICING & DELIVERY")
    text(c, "Pricing, fixes & next steps", M, 65, 26, INK, True)
    paragraph(c, "The pricing tool exposes a simple rule so reviewers can trace the result. "
              "It previews a suggestion; it does not update the product or place an order.",
              M, 110, CW, 10.6)

    image(c, "pricing-detail.jpg", M, 164, col, 224)
    box(c, M + col + gap, 164, col, 224, MINT)
    sx = M + col + gap + 14
    text(c, "PULSE SMARTWATCH", sx, 177, 9.0, TEAL, True)
    paragraph(c, "Base $129  |  Demand 0.8<br/>Stock 3  |  Competitor $145", sx, 200, col - 28, 9.2)
    for index, (label, value) in enumerate([
        ("Demand adjustment", "$149.64"),
        ("Low-stock uplift (+10%)", "$164.604"),
        ("Blend with competitor", "$154.802"),
        ("Rounded preview", "$154.80"),
    ]):
        top = 249 + index * 31
        text(c, label, sx, top, 9, MUTED)
        text(c, value, sx + 150, top, 9.8, TEAL if index == 3 else INK, index == 3)
    paragraph(c, "Observed result from the live pricing sandbox. The base rule is "
              "price x (1 + 0.2 x demand), followed by stock and competitor adjustments.",
              M, 404, CW, 9.2)

    text(c, "What was fixed for this demo", M, 454, 15, INK, True)
    paragraph(c, "<b>Startup:</b> rebuilt the missing SQLite native binding and started UI/API on port 6220. "
              "<b>Empty screens:</b> seeded linked data with a pre-seed backup and duplicate protection. "
              "<b>Readability:</b> corrected catalog title, price and label contrast in light mode.",
              M, 483, CW, 9.7)

    text(c, "Current boundaries and the work ahead", M, 563, 15, INK, True)
    limitations = [
        ("Access", "Sign-in UI bypasses API validation; stored passwords are plaintext and routes lack "
         "authorization. Next: hashed passwords, sessions and enforced roles."),
        ("Intelligence", "Recommendations return the newest products, including zero-stock items. Pricing is "
         "rule-based. Next: stock-aware recommendations and integrated AI modules."),
        ("Commerce & metrics", "Cart/checkout, payments and shipping integrations are absent. Conversion, "
         "coverage and pulse are placeholders. Next: complete checkout and measured analytics."),
    ]
    y = 595
    for title, body in limitations:
        text(c, title, M, y, 9.0, TEAL, True)
        height = paragraph(c, body, M + 103, y, CW - 103, 9.1)
        y += max(height, 26) + 11
    rule(c, 756)
    paragraph(c, "Verified: SQLite integrity, foreign keys, matching order totals, zero inserts on a second "
              "seed run, frontend build (legacy ESLint plugin disabled), live screens and $154.80 pricing. "
              "Evidence: Node controllers/routes "
              "and React components; details in docs/demo-guide.md.", M, 765, CW, 7.4, leading=10)
    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
