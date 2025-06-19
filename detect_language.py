import fasttext
LANG_DETECT_MODEL_PATH = "models/lid.176.bin"

def detect_language(text: str) -> str:
    text = text.replace("\n", " ")
    model = fasttext.load_model(LANG_DETECT_MODEL_PATH)
    prediction = model.predict(text)
    if prediction and len(prediction) > 0 and len(prediction[0]) > 0:
        return prediction[0][0].replace("__label__", "")
    else:
        return "Error detecting language"
