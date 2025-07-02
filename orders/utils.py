from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Order

def generate_invoice_pdf(order: Order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica", 12)
    y = 750

    p.drawString(50, y, f"Invoice #: {order.invoice_number or order.id}")
    y -= 20
    p.drawString(50, y, f"Customer: {order.user.email}")
    y -= 20
    p.drawString(50, y, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    y -= 40

    p.drawString(50, y, "Items:")
    y -= 20

    for item in order.items.all():
        line = f"{item.menu_item.name} x {item.quantity} - ${item.price:.2f}"
        p.drawString(60, y, line)
        y -= 20

    y -= 10
    p.drawString(50, y, f"Total: ${order.total_price:.2f}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer