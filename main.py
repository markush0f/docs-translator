import argparse
import os
from tools.processor import translate_docx
from models.azure_translator import translate_text as azure_translate
from models.deepl_translator import translate_text as deepl_translate
from models.aws_translator import translate_text as aws_translate
from tools.converter import convert_pdf_to_docx, convert_docx_to_pdf
from typing import Literal

# py main.py documento.pdf en --source_lang es --model azure
ModelType = Literal["azure", "deepl", "aws"]


def get_translator(model: ModelType):
    translators = {
        "azure": azure_translate,
        "deepl": deepl_translate,
        "aws": aws_translate,
    }
    try:
        return translators[model]
    except KeyError:
        raise ValueError(f"Modelo '{model}' no soportado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Traducir documentos .docx o .pdf usando AWS, Azure o DeepL."
    )
    parser.add_argument(
        "input_path", type=str, help="Ruta del archivo a traducir (PDF o DOCX)"
    )
    parser.add_argument(
        "target_lang", type=str, help="Idioma destino (ej: 'en', 'fr', 'de')"
    )
    parser.add_argument(
        "--source_lang",
        type=str,
        default="auto",
        help="Idioma fuente (por defecto: auto)",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["azure", "deepl", "aws"],
        default="aws",
        help="Proveedor de traducción (default: aws)",
    )

    args = parser.parse_args()

    input_path = args.input_path
    target_lang = args.target_lang
    source_lang = args.source_lang
    model: ModelType = args.model

    translate_func = get_translator(model)

    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)
    is_pdf = ext.lower() == ".pdf"

    if is_pdf:
        temp_docx = f"{name}_converted.docx"
        convert_pdf_to_docx(input_path, temp_docx)
        output_docx = f"translated_{name}_{source_lang}_to_{target_lang}_{model}.docx"
        translate_docx(temp_docx, output_docx, target_lang, source_lang, translate_func)
        final_pdf = f"translated_{name}_{model}.pdf"
        convert_docx_to_pdf(output_docx, final_pdf)
    else:
        output_docx = f"translated_{name}_{source_lang}_to_{target_lang}_{model}.docx"
        translate_docx(
            input_path, output_docx, target_lang, source_lang, translate_func
        )
