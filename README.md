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

### Paso 2: Ejecutar desde consola

```bash
python translate.py <ruta_archivo> --target_lang en --source_lang es --model aws|azure|deepl
```

### Ejemplo:

```bash
python translate.py document.pdf --target_lang en --source_lang es --model deepl
```

Este ejemplo:

* Traduce `document.pdf` de español a inglés
* Usa DeepL como proveedor

> Si el archivo es PDF, lo convierte a `.docx`, lo traduce y luego lo vuelve a guardar como `.pdf` traducido.

### Tipos de entrada soportados

* `.docx`: documento Word editable
* `.pdf`: cualquier PDF con contenido seleccionable

### Modelos soportados (`--model`)

* `aws`: Amazon Translate
* `azure`: Microsoft Azure Translator
* `deepl`: DeepL Translator

### Idiomas (`--target_lang` y `--source_lang`)

* Usa códigos estándar ISO 639-1 (ej: `en`, `es`, `fr`, `de`, `pt`, etc.)
* DeepL requiere dialecto en destino: `EN-US`, `EN-GB`, `PT-PT`, `PT-BR`, etc.
* Si usas `--source_lang auto`, se activará la detección automática (usa fastText)



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
