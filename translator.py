from googletrans import Translator

translator = Translator()


def translate_text(text, src_lang, dest_lang):
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text
