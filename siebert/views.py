"""Siebert form views."""
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from reportlab.pdfgen import canvas


def siebert(request):
    """Siebert form template view."""
    return render_to_response(
        'siebert.html', {
        }, RequestContext(request))


def siebert_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="oc_siebert.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 100, "Hello world.")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
