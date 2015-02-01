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
        'attachment; filename="oc_siebert_form.pdf"')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # p.drawString(100, 100, "Hello world.")

    logo = os.path.join(IMAGE_DIR, 'oc_logo.jpeg')
    p.drawImage(logo, 400, 730, 151, 60)
    schema = os.path.join(IMAGE_DIR, 'siebert_schema.jpeg')
    p.drawImage(schema, 400, 580, 151, 143)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
