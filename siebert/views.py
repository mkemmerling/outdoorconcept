"""Siebert form views."""
from collections import namedtuple
from datetime import date
import io
import os

from django.http import HttpResponse
# from django.shortcuts import render_to_response
# from django.template import RequestContext

from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

LINK_COLOR = CMYKColor(.52, .49, .07, 0)
IMAGE_DIR = os.path.abspath(os.path.join(
    __file__, os.pardir, 'static', 'siebert', 'images'))


# def siebert(request):
#     """Siebert form template view."""
#     return render_to_response(
#         'siebert.html', {
#         }, RequestContext(request))


# 1 Centimeter = 28,3464567 Points
# A4: 210 x 297 (595.27 x 841.89)

# Page margins and borders
Margin = namedtuple('Margin', 'bottom top left right')
margin = Margin(1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm)
Border = namedtuple('Border', 'bottom top left right')
border = Border(
    margin.bottom, A4[1] - margin.top, margin.left, A4[0] - margin.right)


def siebert_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="oc_siebert_formel.pdf"')

    buffer = io.BytesIO()
    doc = canvas.Canvas(buffer, pagesize=A4, pageCompression=1)

    author = "www.outdoorconcept.at"
    title1 = "Berechnung der Seilzugkraft"
    title2 = "bei horizontal gespannten Seiten"
    subject = "Auf Basis der Siebert-Formel"

    metadata(doc, author, " ".join((title1, title1)), subject)
    # helplines(doc)
    header(doc, title1, title2, subject)
    body(doc, request.GET)
    footer(doc)

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


def header(doc, title1, title2, subject):
    text = doc.beginText()
    text.setFont('Helvetica-Bold', 16)
    text.setTextOrigin(border.left, border.top - 12)
    text.textLine(title1)
    text.textLine(title2)
    text.setFont('Helvetica', 12)
    text.moveCursor(0, 32)
    text.textLine(subject)
    text.textLine("Überarbeitet unter Berücksichtigung der EN 15567:2013")
    doc.drawText(text)

    logo = ImageReader(os.path.join(IMAGE_DIR, 'oc_logo.jpeg'))
    w_logo, h_logo = scale(logo.getSize(), .42)
    x, y = border.right - w_logo, border.top - h_logo
    doc.drawImage(logo, x, y, w_logo, h_logo)

    link = "http://www.outdoorconcept.at"
    link_rect = (x, y, x + w_logo, y + h_logo)
    doc.linkURL(link, link_rect)

    schema = ImageReader(os.path.join(IMAGE_DIR, 'siebert_schema.jpeg'))
    w_schema, h_schema = scale(schema.getSize(), .21)
    x, y = border.right - w_schema, border.top - h_logo - h_schema - .2 * cm
    doc.drawImage(schema, x, y, w_schema, h_schema)

    formula = ImageReader(os.path.join(IMAGE_DIR, 'siebert_formula.jpeg'))
    w, h = scale(formula.getSize(), .29)
    doc.drawImage(formula, margin.left, y, w, h)


def body(doc, data):
    text = doc.beginText()
    text.setTextOrigin(border.left, 530)

    # ELement properties
    text.setFont('Helvetica', 12)
    if data.get('flyingFox', False):
        content = "Es handelt sich um einen Flying Fox (Zipline)."
    else:
        content = ""
    text.textLine(content)
    text.moveCursor(0, 5)
    try:
        nrPersons = int(data.get('nrPersons', 0))
    except:
        content = ""
    else:
        if nrPersons == 1:
            content = ("Das Element darf gleichzeitig nur von 1 Person "
                       "verwendet werden.")
        else:
            content = ("Das Element darf gleichzeitig von {} Personen "
                       "verwendet werden.".format(nrPersons))
    text.textLine(content)
    text.moveCursor(0, 20)

    # Siebert formula
    print_value(text, data, 'p', "Personenlast", "p", "kg")
    print_value(text, data, 'q', "Seilgewicht", "q", "g/m")
    print_value(text, data, 'f', "Durchhang", "f", "m")
    print_value(text, data, 'l', "Spannweite", "l", "m")
    text.moveCursor(0, 14)
    print_value(text, data, 'fz_excl', "Seilzugkraft", "Fz", "kN",
                "exklusive Faktor")
    print_value(text, data, 'fz_incl', "Seilzugkraft", "Fz", "kN",
                "inklusive Faktor")

    # Developer data
    doc.setLineWidth(.5)
    doc.line(border.left, 290, border.right, 290)
    text.setTextOrigin(border.left, 270)
    print_text(text, data, 'developer', "Bauträger")
    print_text(text, data, 'location', "Standort des Seilgartens")
    print_text(text, data, 'description', "Bezeichnung der Übung")
    print_text(text, data, 'number', "Nummer der Übung")

    # Signature
    text.setTextOrigin(border.right - 300, 140)
    text.setFont('Helvetica', 10)
    text.textLine("Für die Korrektheit der Angaben:")
    text.moveCursor(0, 20)
    text.setFont('Helvetica', 12)
    text.textLine(data.get('date', ''))
    doc.line(border.right, 105, border.right - 300, 105)
    text.setFont('Helvetica', 10)
    text.textOut("Datum")
    text.moveCursor(150, 0)
    text.textLine("Unterschrift")

    doc.drawText(text)


def print_value(text, data, key, name, parameter, unit, description=None):
    text.setFont('Helvetica-Bold', 12)
    value = data.get(key, '')
    if value:
        value += " " + unit
    text.textOut(name)
    text.setFont('Helvetica-Oblique', 12)
    text.moveCursor(100, 0)
    text.textOut(parameter)
    text.moveCursor(30, 0)
    text.setFont('Helvetica', 12)
    text.textLine(value)
    text.moveCursor(-130, 0)
    if description:
        text.setFont('Helvetica', 10)
        text.textLine(description)
    text.moveCursor(0, 6)


def print_text(text, data, key, name):
    text.setFont('Helvetica-Bold', 12)
    value = data.get(key, '')
    text.textOut(name)
    text.moveCursor(170, 0)
    text.setFont('Helvetica', 12, 24)
    text.textLine(value)
    text.moveCursor(-170, 0)


def footer(doc):
    text = doc.beginText()
    text.setTextOrigin(border.left, border.bottom + 3)
    text.setFont('Helvetica', 10)
    text.textOut("© ")
    text.setFillColor(LINK_COLOR)
    text.textOut("www.outdoorconcept.at ")
    text.setFillColor(black)
    text.textLine(" {} / Philipp Strasser mit freundlicher Genehmigung von "
                  "Walter Siebert.".format(date.today().year))
    doc.drawText(text)

    link = "http://www.outdoorconcept.at"
    # doc.stringWidth("www.outdoorconcept.at", 'Helvetica', 10) is too short
    link_rect = (border.left + 10, border.bottom + 14, 160, border.bottom - 2)
    doc.linkURL(link, link_rect)


def scale(size, factor):
    return [l * factor for l in size]
