import requests
import uuid
import os
from dotenv import load_dotenv
import fitz  

load_dotenv()

key = os.getenv("AZURE_TRANSLATOR_KEY")
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "northeurope"

path = "/translate"
constructed_url = endpoint + path

params = {
    "api-version": "3.0",
    "from": "en", 
    "to": "es",    
}

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Ocp-Apim-Subscription-Region": location,
    "Content-type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}


# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    
    full_text = ""
    
    # Extraer texto de cada página
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text("text") + "\n"
    
    return full_text

# Función para traducir el texto
def translate_text(text: str, target_lang: str) -> str:
    global used_characters
    
    # Contar los caracteres en el texto que se va a traducir
    text_length = len(text)
    
    # Verificar si tienes suficientes caracteres disponibles
    if used_characters + text_length > total_free_characters:
        remaining_characters = total_free_characters - used_characters
        print(f"Advertencia: Solo te quedan {remaining_characters} caracteres disponibles para traducir.")
        # Puedes decidir no hacer la traducción si no hay suficientes caracteres disponibles
        # o proceder con la traducción, aunque se podría cobrar si sobrepasas el límite
        return None
    
    body = [{"text": text}]
    params["to"] = target_lang  # Establecer el idioma de destino dinámicamente
    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response_json = response.json()

    # Retornar el texto traducido
    return response_json[0]["translations"][0]["text"]

# Función para guardar un PDF traducido
def save_translated_pdf(input_pdf_path: str, output_pdf_path: str, translated_text: str):
    doc = fitz.open(input_pdf_path)

    translated_lines = translated_text.split("\n")
    line_index = 0

    # Reemplazar el texto de cada página
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_instances = page.search_for(" ")  # Buscando áreas de texto
        
        for instance in text_instances:
            if line_index < len(translated_lines):
                page.insert_text(instance[:2], translated_lines[line_index])  # Inserta el texto traducido
                line_index += 1

    # Guardar el PDF traducido
    doc.save(output_pdf_path)

    print(f"Documento traducido guardado como: {output_pdf_path}")
