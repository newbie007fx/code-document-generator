from xhtml2pdf import pisa
from markdown import markdown
from io import BytesIO

def generate_pdf_from_markdown(md_text: str) -> BytesIO:
    html = markdown(md_text, extensions=["fenced_code", "tables"])
    html = f"<html><body>{html}</body></html>"

    pdf_file = BytesIO()
    pisa.CreatePDF(src=html, dest=pdf_file)
    pdf_file.seek(0)
    return pdf_file