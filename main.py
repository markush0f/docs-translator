from tools.processor import translate_docx
from models.azure_translator import translate_text as azure_translate
from models.deepl_translator import translate_text as deepl_translate
from models.aws_translator import translate_text as aws_translate
from typing import Literal

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
    model: ModelType = "aws"
    input_path = "document.docx"
    filename = input_path.rsplit(".", 1)[0]
    target_lang = "en"
    output_path = f"translated_{filename}_{model}.docx"
    source_lang = "es"

    translate_func = get_translator(model)
    translate_docx(input_path, output_path, target_lang, source_lang, translate_func)
    print(f"Documento traducido con {model} guardado en: {output_path}")
