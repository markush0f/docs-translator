from processor import translate_docx
from models.azure_translator import translate_text as azure_translate

def get_translator(model: str):
    if model == "azure":
        return azure_translate
    else:
        raise ValueError(f"Modelo '{model}' no soportado.")

if __name__ == "__main__":
    input_path = "document.docx"
    output_path = "translated_document.docx"
    target_lang = "en"
    model = "azure"  

    translate_func = get_translator(model)
    translate_docx(input_path, output_path, target_lang, translate_func)
    print(f"Documento traducido con {model} guardado en: {output_path}")
