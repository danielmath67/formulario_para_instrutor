import io
from xml.sax.saxutils import escape
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def gerar_pdf(relatorio):
    buffer = io.BytesIO()
    estilos = getSampleStyleSheet()
    normal = estilos['BodyText']
    normal.fontSize = 10
    normal.leading = 14
    normal.spaceBefore = 0
    normal.spaceAfter = 0
    normal.splitLongWords = True
    documento = SimpleDocTemplate(buffer, pagesize=A4, title='Ficha do aluno',
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elementos = [Paragraph('Ficha do aluno - Instrutor de trânsito', estilos['Title']),
        Paragraph('Registrada em ' + timezone.localtime(relatorio.criado_em).strftime('%d/%m/%Y %H:%M'), normal),
        Spacer(1, 12)]
    for rotulo, valor in relatorio.campos():
        texto = escape(valor).replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br/>')
        elementos.append(Paragraph("<b>" + escape(rotulo) + "</b><br/>" + texto, normal))
        elementos.append(Spacer(1, 4))

    documento.build(elementos)
    return buffer.getvalue()
