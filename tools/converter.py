from pdf2docx import Converter
from docx2pdf import convert
from typing import Optional


def convert_pdf_to_docx(pdf_path: str, docx_output_path: str) -> None:
    cv = Converter(pdf_path)
    cv.convert(docx_output_path, start=0)
    cv.close()


def convert_docx_to_pdf(docx_path: str, pdf_output_path: Optional[str] = None) -> None:
    if pdf_output_path:
        convert(docx_path, pdf_output_path)
    else:
        convert(docx_path)
