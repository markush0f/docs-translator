# Multi-Provider Document Translator

Este proyecto permite traducir archivos `.docx` mediante tres servicios diferentes de traducción automática: **Amazon Translate**, **Azure Translator** y **DeepL**, todos integrados en un mismo sistema modular. Además, incorpora detección automática del idioma, logging y métricas por proveedor.

---

## ✅ ¿Qué hace?

* Traduce archivos `.docx` manteniendo el formato.
* Detecta automáticamente el idioma del texto fuente (opcional).
* Permite elegir entre tres proveedores: AWS, Azure y DeepL.
* Guarda logs en consola y en archivo `logs/logs.txt`.
* Consulta métricas de uso en Azure y Amazon Translate.

---

## ⚙️ Requisitos

* Python 3.10 o superior
* Cuenta en AWS, Azure y/o DeepL con claves válidas
* Instalar dependencias con:

```bash
pip install -r requirements.txt
```

---

## 🧪 Cómo usarlo

### Paso 1: Crear archivo `.env` con tus claves

```env
# AWS
AWS_ACCESS_KEY_ID=TU_CLAVE
AWS_SECRET_ACCESS_KEY=TU_SECRETO
AWS_DEFAULT_REGION=eu-west-1

# Azure
AZURE_TRANSLATOR_KEY=TU_CLAVE
AZURE_SUBSCRIPTION_ID=TU_SUBSCRIPCION
AZURE_TRANSLATOR_RESOURCE_ID=/subscriptions/.../resourceGroups/.../providers/...

# DeepL
DEEPL_API_KEY=TU_API_KEY
```

### Paso 2: Usar uno de los traductores en `main.py`

```python
from processor import translate_docx
from models.aws_translator import AWSTranslator
# from models.azure_translator import AzureTranslator
# from models.deepl_translator import DeepLTranslator

translator = AWSTranslator()
translate_docx("document.docx", "translated.docx", "en", "auto", translator.translate_text)
```

Puedes cambiar `AWSTranslator()` por `AzureTranslator()` o `DeepLTranslator()` según el proveedor que quieras usar. El valor `"auto"` activará la detección automática del idioma fuente con fastText.

---

## 🌍 Traducción por proveedor

### 🔹 Amazon Translate

* Usa `boto3` y la API oficial.
* Soporta detección manual o automática.
* Hasta **2 millones de caracteres gratis al mes** durante 12 meses.
* Requiere tener activado **Cost Explorer** para ver métricas desde código.

### 🔹 Azure Translator

* Traducción vía REST con `requests`.
* Requiere clave, región y subscription ID.
* Se puede consultar el uso (caracteres traducidos) con Azure Monitor.

### 🔹 DeepL

* Traducción usando el SDK oficial (`deepl`).
* Gratis hasta **500.000 caracteres/mes** en la versión Free.
* Requiere especificar dialecto del idioma destino (ej: `EN-US`, `EN-GB`).
* Permite traducción por lotes y detección automática si no defines `"from"`.

---

## 📈 Consultar métricas

### Amazon Translate

```python
from metrics.aws_metrics import get_amazon_translate_usage
print(get_amazon_translate_usage())
```

### Azure Translator

```python
from metrics.azure_metrics import count_total_characters_translated
count_total_characters_translated()
```

---

## ✔ Logs

Todos los módulos usan el sistema de logging configurado en `logger_config.py`. Los logs se guardan en tiempo real tanto en consola como en el archivo:

```
logs/logs.txt
```

Cada módulo define su propio nombre de logger (`AWS-Translator`, `AzureMetrics`, etc.), y puedes configurar el nivel (`DEBUG`, `INFO`, `ERROR`, etc.).

---

## 🧠 Notas adicionales

* No subas tu archivo `.env` a ningún repositorio público.
* Si Cost Explorer (AWS) o Azure Monitor no muestra métricas, espera hasta 24h después de habilitarlos.
* Este proyecto puede ampliarse fácilmente para soportar traducción de archivos PDF, interfaz web u otros proveedores como Hugging Face.
