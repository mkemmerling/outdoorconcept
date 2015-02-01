"""Siebert form views."""

import io
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from reportlab.pdfgen import canvas

IMAGE_DIR = os.path.abspath(os.path.join(
    __file__, os.pardir, 'static', 'siebert', 'images'))


def siebert(request):
    """Siebert form template view."""
    return render_to_response(
        'siebert.html', {
        }, RequestContext(request))


def siebert_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="oc_siebert_formel.pdf"')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(20, 730, "Berechnung der Seilzugkraft bei horizontal "
                 "gespannten Seiten")
    p.drawString(20, 710, "Auf Basis der Siebert-Formel")
    p.drawString(20, 695, "Überarbeitet unter Berücksichtigung der "
                 "EN 15567:2013")

    logo = os.path.join(IMAGE_DIR, 'oc_logo.jpeg')
    p.drawImage(logo, 400, 730, 151, 60)
    schema = os.path.join(IMAGE_DIR, 'siebert_schema.jpeg')
    p.drawImage(schema, 400, 580, 151, 143)
    formula = os.path.join(IMAGE_DIR, 'siebert_formula.jpeg')
    p.drawImage(formula, 20, 580, 249, 65)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
