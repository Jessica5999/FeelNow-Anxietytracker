# translation_utils.py
from deep_translator import GoogleTranslator

def translate_text(text, target_language):
    translator = GoogleTranslator(target=target_language)  # Initialize the GoogleTranslator object
    translation = translator.translate(text)  # Translate the text
    return translation
