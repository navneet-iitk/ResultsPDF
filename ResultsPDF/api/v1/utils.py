import io
import logging
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

logger = logging.getLogger(__name__)


def json_to_pdf(links_json):
    buffer = io.BytesIO()
    p = Canvas(buffer, bottomup=0)
    # p = Canvas(filename, bottomup=0)
    textobject = p.beginText()
    textobject.setTextOrigin(inch, inch)
    textobject.setFont("Helvetica-Oblique", 14)
    for link in links_json:
        textobject.textLine(link)
    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer