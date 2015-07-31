"""Siebert form views."""
from collections import namedtuple
from datetime import date
import io
import os

from django.http import HttpResponse
from django.utils.formats import localize
from django.utils.translation import get_language
from django.utils.translation import ugettext as _

from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

LINK_COLOR = CMYKColor(.52, .49, .07, 0)
IMAGE_DIR = os.path.abspath(os.path.join(
    __file__, os.pardir, 'static', 'siebert', 'images'))

VALUE_HELP = {
    'en': {
        'p': (
            ("Laut EN 15567:2013 müssen hier 600kg für die erste Person und "
             "80kg für jede",
             "weitere Person berechnet werden. Ausnahme: Bei Flying Fox "
             "(Zipline) muss",
             "mit 300kg kalkuliert werden. [en]",),
            16, 8),
        'q': (
            ("Das Seilgewicht finden Sie auf den Herstellerangaben zu Ihrem "
             "Seil. [en]",),
            14, 12),
        'f': (
            ("Distanz, zwischen der gedachten horizontalen Linie zwischen den "
             "beiden",
             "Anschlagpunkten (Sehne) und dem tiefsten Punkt des Seiles unter "
             "Belastung. [en]",),
            16, 8),
        'l': (
            ("Direkte Distanz zwischen den beiden Anschlagpunkten (Sehne). "
             "[en]",),
            14, 14),
        'fz_excl': (
            ("Dient der Tragwerkskalkulation. Je nach Art des Tragwerks (z.B. "
             "Bäume, Stahl-",
             "oder Betonkonstruktion etc.) muss hier mit dem jeweiligen "
             "Faktor multipliziert",
             "werden. [en]",),
            30, 8),
        'fz_incl': (
            ("Minimale Bruchlast der Elemente der Sicherheitsführung, wie "
             "etwa Stahlseil,",
             "Stahlseiklemmen, Verpressungen, Rapidglieder, Schäkel etc. "
             "[en]",),
            29, 8),
        },
    'de': {
        'p': (
            ("Laut EN 15567:2013 müssen hier 600kg für die erste Person und "
             "80kg für jede",
             "weitere Person berechnet werden. Ausnahme: Bei Flying Fox "
             "(Zipline) muss",
             "mit 300kg kalkuliert werden.",),
            16, 8),
        'q': (
            ("Das Seilgewicht finden Sie auf den Herstellerangaben zu Ihrem "
             "Seil.",),
            14, 12),
        'f': (
            ("Distanz, zwischen der gedachten horizontalen Linie zwischen den "
             "beiden",
             "Anschlagpunkten (Sehne) und dem tiefsten Punkt des Seiles unter "
             "Belastung.",),
            16, 8),
        'l': (
            ("Direkte Distanz zwischen den beiden Anschlagpunkten (Sehne).",),
            14, 14),
        'fz_excl': (
            ("Dient der Tragwerkskalkulation. Je nach Art des Tragwerks (z.B. "
             "Bäume, Stahl-",
             "oder Betonkonstruktion etc.) muss hier mit dem jeweiligen "
             "Faktor multipliziert",
             "werden.",),
            30, 8),
        'fz_incl': (
            ("Minimale Bruchlast der Elemente der Sicherheitsführung, wie "
             "etwa Stahlseil,",
             "Stahlseiklemmen, Verpressungen, Rapidglieder, Schäkel etc.",),
            29, 8),
        },
}

SECURITY_HINTS = {
    'en': ((
        "Bitte beachten Sie, dass mit dieser Formel lediglich Kräfte zwischen "
        "zwei annähernd horizontal liegenden Anschlag-",
        "punkten berechnet werden können. [en]",
        ), {
        'start_lines': (
            "Für Berechnungen von nicht horizontalen Verspannungen, "
            "seitlichen Abspannungen, vertikalen Lasten, Geschwindig-",
            "keiten von Zipline Fahrten, Holzbelastbarkeit oder für "
            "Belastungstests von diversen Komponeneten etc. kontaktieren",
        ),
        'link_line': (
            "Sie bitte",
            "Tel. +43 676 43 13 959 oder Ihren Statiker. [en]"
        )},
        ("Diskussion zu dieser Formel finden Sie im RopeCourseForum (",
         "). [en]"),
        ("stellt lediglich diese Berechnungshilfe zur Verfügung und haftet "
         "nicht für die korrekte Anwendung oder",
         "Datenerhebung. [en]")
        ),
    'de': ((
        "Bitte beachten Sie, dass mit dieser Formel lediglich Kräfte zwischen "
        "zwei annähernd horizontal liegenden Anschlag-",
        "punkten berechnet werden können.",
        ), {
        'start_lines': (
            "Für Berechnungen von nicht horizontalen Verspannungen, "
            "seitlichen Abspannungen, vertikalen Lasten, Geschwindig-",
            "keiten von Zipline Fahrten, Holzbelastbarkeit oder für "
            "Belastungstests von diversen Komponeneten etc. kontaktieren",
        ),
        'link_line': (
            "Sie bitte",
            "Tel. +43 676 43 13 959 oder Ihren Statiker."
        )},
        ("Diskussion zu dieser Formel finden Sie im RopeCourseForum (", ")."),
        ("stellt lediglich diese Berechnungshilfe zur Verfügung und haftet "
         "nicht für die korrekte Anwendung oder",
         "Datenerhebung.")
        ),
}

# 1 Centimeter = 28,3464567 Points
# A4: 210 x 297 (595.27 x 841.89)

# Page margins and borders
Margin = namedtuple('Margin', 'bottom top left right')
margin = Margin(1.5 * cm, 1.5 * cm, 2.5 * cm, 1.5 * cm)
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
    title1 = _("Berechnung der Seilzugkraft [en]")
    title2 = _("bei horizontal gespannten Seiten [en]")
    subject = _("Auf Basis der Siebert-Formel [en]")

    metadata(doc, author, " ".join((title1, title2)), subject)
    # For debugging only
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


# For debugging only
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
    text.setFont('Helvetica', 11)
    text.moveCursor(0, 20)
    text.textLine(subject)
    text.textLine(
        _("Überarbeitet unter Berücksichtigung der EN 15567:2013 [en]"))
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
    doc.drawImage(formula, margin.left, y + 30, w, h)


def body(doc, data):
    lang = get_language()
    if lang not in ('en', 'de'):
        lang = 'en'

    text = doc.beginText()
    text.setTextOrigin(border.left, 590)

    # ELement properties
    text.setFont('Helvetica', 11)
    if data.get('flyingFox', False):
        content = _("Es handelt sich um einen Flying Fox (Zipline). [en]")
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
            content = _("Das Element darf gleichzeitig maximal von 1 Person "
                        "verwendet werden. [en]")
        else:
            content = _("Das Element darf gleichzeitig maximal von "
                        "{nrPersons} Personen verwendet werden. [en]").format(
                        nrPersons=nrPersons)
    text.textLine(content)
    text.moveCursor(0, 15)

    # Siebert formula
    print_value(text, data, 'p', _("Personenlast [en]"), "p", "kg",
                VALUE_HELP[lang]['p'])
    print_value(text, data, 'q', _("Seilgewicht [en]"), "q", "g/m",
                VALUE_HELP[lang]['q'])
    print_value(text, data, 'f', _("Durchhang [en]"), "f", "m",
                VALUE_HELP[lang]['f'])
    print_value(text, data, 'l', _("Spannweite [en]"), "l", "m",
                VALUE_HELP[lang]['l'])
    text.moveCursor(0, 14)
    print_value(text, data, 'fz_excl', _("Seilzugkraft [en]"), "Fz", "kN",
                VALUE_HELP[lang]['fz_excl'], False, _("exklusive Faktor [en]"))
    print_value(text, data, 'fz_incl', _("Seilzugkraft [en]"), "Fz", "kN",
                VALUE_HELP[lang]['fz_incl'], True, _("inklusive Faktor [en]"))

    # Developer data
    doc.setLineWidth(.5)
    doc.line(border.left, 365, border.right, 365)
    text.setTextOrigin(border.left, 345)
    print_info(doc, text, data, 'developer', _("Bauträger [en]"))
    print_info(doc, text, data, 'location', _("Standort des Seilgartens [en]"))
    print_info(doc, text, data, 'description', _("Bezeichnung der Übung [en]"))
    print_info(doc, text, data, 'number', _("Nummer der Übung [en]"))

    # Signature
    text.setTextOrigin(border.right - 300, 245)
    text.setFont('Helvetica', 10)
    text.textLine(_("Für die Korrektheit der Angaben: [en]"))
    text.moveCursor(0, 20)
    text.setFont('Helvetica', 12)
    text.textLine(data.get('date', ''))
    doc.line(border.right, 210, border.right - 300, 210)
    text.setFont('Helvetica', 10)
    text.textOut(_("Date"))
    text.moveCursor(150, 0)
    text.textLine(_("Signature"))

    print_security_hints(text, lang)

    doc.drawText(text)


def print_value(text, data, key, name, parameter, unit, help, bold=False,
                description=None):
    text.setFont('Helvetica-Bold', 11)
    value = data.get(key, '')
    if value:
        value = format_value(key, value) + " " + unit
    text.textOut(name)
    text.setFont('Helvetica-Oblique', 11)
    text.moveCursor(100, 0)
    text.textOut(parameter)
    text.moveCursor(30, 0)
    font = 'Helvetica-Bold' if bold else 'Helvetica'
    text.setFont(font, 11)

    text.textLine(value)

    text.moveCursor(-130, 0)
    if description:
        text.setFont('Helvetica', 10)
        text.textLine(description)

    text.moveCursor(200, -help[1])
    text.setFont('Helvetica', 8)
    for line in help[0]:
        text.textLine(line)
    text.moveCursor(-200, help[2])


def format_value(key, value):
    if key in ('p', 'q'):
        cast = int
    elif key in ('f', 'l'):
        cast = float if '.' in value else int
    else:
        cast = float

    try:
        value = cast(value)
    except ValueError:
        return value
    else:
        return localize(round(value, 2))


def print_info(doc, text, data, key, name):
    max_length = border.right - 150

    text.setFont('Helvetica-Bold', 11)
    value = data.get(key, '')
    text.textOut(name)
    text.moveCursor(150, 0)
    # If necessary lower font size to ensure the value does not overflow
    # the right border; determined font size for checks by try & error
    if doc.stringWidth(value, 'Helvetica', 12.2) > max_length:
        text.setFont('Helvetica', 9, 22)
    elif doc.stringWidth(value, 'Helvetica', 13.3) > max_length:
        text.setFont('Helvetica', 10, 22)
    else:
        text.setFont('Helvetica', 11, 22)
    text.textLine(value)
    text.moveCursor(-150, 0)


def print_security_hints(text, lang):
    text.setTextOrigin(border.left, 165)
    text.setFont('Helvetica-Bold', 9)
    text.textLine(_("Wichtige Sicherheitshinweise und Anmerkungen [en]"))
    text.moveCursor(0, 3)

    paras = SECURITY_HINTS[lang]

    text.setFont('Helvetica', 9)
    para1 = paras[0]
    for line in para1:
        text.textLine(line)
    text.moveCursor(0, 3)

    para2 = paras[1]
    for line in para2['start_lines']:
        text.textLine(line)
    link_line = para2['link_line']
    text.textOut(link_line[0])
    text.setFillColor(LINK_COLOR)
    text.textOut(" office@outdoorconcept.at ")
    text.setFillColor(black)
    text.textLine(link_line[1])
    text.moveCursor(0, 3)

    para3 = paras[2]
    text.textOut(para3[0])
    text.setFillColor(LINK_COLOR)
    text.textOut("http://www.rcforum.cc")
    text.setFillColor(black)
    text.textLine(para3[1])
    text.moveCursor(0, 3)

    para4 = paras[3]
    text.setFont('Helvetica-Oblique', 9)
    text.textOut("outdoorconcept ")
    text.setFont('Helvetica', 9)
    for line in para4:
        text.textLine(line)


def footer(doc):
    text = doc.beginText()
    text.setTextOrigin(border.left, border.bottom + 3)
    text.setFont('Helvetica', 9)
    text.textOut("© ")
    text.setFillColor(LINK_COLOR)
    text.textOut("www.outdoorconcept.at ")
    text.setFillColor(black)
    copyright = _("Philipp Strasser by courtesy of Walter Siebert.")
    text.textLine(" {} / {}".format(date.today().year, copyright))
    doc.drawText(text)

    link = "http://www.outdoorconcept.at"
    link_rect = (border.left + 10, border.bottom + 12, border.left + 120,
                 border.bottom + 12)
    doc.linkURL(link, link_rect)


def scale(size, factor):
    return [l * factor for l in size]
