from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import pdfkit
from ClassSearch import ClassSearch
import markdown2
import pdfkit


def selectFirstEventUFC(paginaEventos:ClassSearch):
    result = None
    for link in paginaEventos.soup.find_all("a", {"class": "border-b border-tap_3 border-dotted hover:border-solid"}):
        if "UFC" in link.text:
            result = link
            break
    paginaEventos.closeConexion()

    return result
def parsearNombreParaElPDF(pdf:str):
    pdf = pdf.replace(".","").replace(" ","_").replace(":","")
    pdf+= ".pdf"    

    return pdf


def convert_markdown_to_pdf(markdown_file, pdf_file):

    print("Nombre actual -> ",pdf_file)
    pdf_file = parsearNombreParaElPDF(pdf_file)

    print("Nombre parseado -> ",pdf_file)

    # Lee el archivo Markdown
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convierte el Markdown a HTML
    html_content = markdown2.markdown(markdown_content)
    # Configura el path de wkhtmltopdf si es necesario
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")  # Ajusta según tu instalación

    # Añade la metaetiqueta de codificación UTF-8
    full_html = f"""<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Documento PDF</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>"""


    # Convierte el HTML a PDF
    pdfkit.from_string(full_html, pdf_file, configuration=config)  # Cambiado a `full_html`

def getNameEvent(soupUFC): return soupUFC.find('h2',{'class': "text-2xl md:text-2xl text-center font-bold text-tap_3"}).text

