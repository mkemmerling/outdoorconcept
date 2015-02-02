"""Siebert form views."""

import io
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

IMAGE_DIR = os.path.abspath(os.path.join(
    __file__, os.pardir, 'static', 'siebert', 'images'))


def siebert(request):
    """Siebert form template view."""
    return render_to_response(
        'siebert.html', {
        }, RequestContext(request))


# 1 Centimeter = 28,3464567 Points
# A4: 210 x 297 (595.27 x 841.89)

cm1 = 28.35
cm1_5 = 42.52
cm2 = 56.68

# Page borders
bottom_left = (cm1_5, cm1_5)
bottom_right = (A4[0] - cm1_5, cm1_5)
top_left = (cm1_5, A4[1] - cm1_5)
top_right = (A4[0] - cm1_5, A4[1] - cm1_5)


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
        bottom_left + bottom_right,
        bottom_right + top_right,
        top_right + top_left,
        top_left + bottom_left,
    )
    doc.lines(pageborder)


def header(doc, title, subject):
    doc.drawString(cm1_5, 790, title)
    doc.drawString(cm1_5, 770, subject)
    text = "Überarbeitet unter Berücksichtigung der EN 15567:2013"
    doc.drawString(cm1_5, 755, text)

    logo = os.path.join(IMAGE_DIR, 'oc_logo.jpeg')
    w_logo, h_logo = 151, 60
    x, y = top_right[0] - w_logo, top_right[1] - h_logo
    doc.drawImage(logo, x, y, w_logo, h_logo)

    schema = os.path.join(IMAGE_DIR, 'siebert_schema.jpeg')
    w, h = 151, 143
    x, y = top_right[0] - w, top_right[1] - h_logo - h - 5
    doc.drawImage(schema, x, y, w, h)

    formula = os.path.join(IMAGE_DIR, 'siebert_formula.jpeg')
    doc.drawImage(formula, cm1_5, 610, 249, 65)










