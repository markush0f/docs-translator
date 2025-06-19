from processor import translate_docx
from models.azure_translator import translate_text as azure_translate
from models.deepl_translator import translate_text as deepl_translate


def get_translator(model: str):
    if model == "azure":
        return azure_translate
    elif model == "deepl":
        return deepl_translate
    else:
        raise ValueError(f"Modelo '{model}' no soportado.")


if __name__ == "__main__":
    model = "azure"
    input_path = "document.docx"
    target_lang = "en"
    output_path = f"translated_document_{model}.docx"
    source_lang = "es"

    translate_func = get_translator(model)
    translate_docx(input_path, output_path, target_lang, source_lang, translate_func)
    print(f"Documento traducido con {model} guardado en: {output_path}")
