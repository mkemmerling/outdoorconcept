"""Siebert form views."""
from collections import namedtuple
import io
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

IMAGE_DIR = os.path.abspath(os.path.join(
    __file__, os.pardir, 'static', 'siebert', 'images'))


def siebert(request):
    """Siebert form template view."""
    return render_to_response(
        'siebert.html', {
        }, RequestContext(request))


# 1 Centimeter = 28,3464567 Points
# A4: 210 x 297 (595.27 x 841.89)

# Page borders
Margin = namedtuple('Margin', 'bottom top left right')
margin = Margin(1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm)

Border = namedtuple('Border', 'bottom top left right')
border = Border(
    margin.bottom, A4[1] - margin.top, margin.left, A4[0] - margin.right)


def siebert_pdf(request):
    # data = request.GET

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="oc_siebert_formel.pdf"')

    buffer = io.BytesIO()
    doc = canvas.Canvas(buffer, pagesize=A4, pageCompression=1)

    author = "www.outdoorconcept.at"
    title = "Berechnung der Seilzugkraft bei horizontal gespannten Seiten"
    subject = "Auf Basis der Siebert-Formel"

    metadata(doc, author, title, subject)
    helplines(doc)
    header(doc, title, subject)

    doc.showPage()
    doc.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def metadata(doc, author, title, subject):
    doc.setAuthor(author)
    doc.setTitle(title)
    doc.setSubject(subject)


def helplines(doc):
    doc.setLineWidth(.3)
    pageborder = (
        (border.left, border.bottom, border.right, border.bottom),
        (border.right, border.bottom, border.right, border.top),
        (border.right, border.top, border.left, border.top),
        (border.left, border.top, border.left, border.bottom),
    )
    doc.lines(pageborder)


def header(doc, title, subject):
    doc.drawString(margin.left, 790, title)
    doc.drawString(margin.left, 770, subject)
    text = "Überarbeitet unter Berücksichtigung der EN 15567:2013"
    doc.drawString(margin.left, 755, text)

    logo = os.path.join(IMAGE_DIR, 'oc_logo.jpeg')
    w_logo, h_logo = 151, 60
    x, y = border.right - w_logo, border.top - h_logo
    doc.drawImage(logo, x, y, w_logo, h_logo)

    schema = os.path.join(IMAGE_DIR, 'siebert_schema.jpeg')
    w, h = 151, 143
    x, y = border.right - w, border.top - h_logo - h - 5
    doc.drawImage(schema, x, y, w, h)

    formula = os.path.join(IMAGE_DIR, 'siebert_formula.jpeg')
    doc.drawImage(formula, margin.left, 610, 249, 65)










