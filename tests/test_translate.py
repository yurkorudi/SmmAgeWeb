import requests
from lingua import Language, LanguageDetectorBuilder

detector = LanguageDetectorBuilder.from_all_languages().build()

def tranlate_to_uk(text: str): 
    lang = detector.detect_language_of(text)
    
    if lang is None:
        return text
    
    source = lang.iso_code_639_1.name.lower()
    
    if source == 'uk':
        return text
    
    url = 'https://api.mymemory.translated.net/get'
    
    resp = requests.get(
        url,
        params={
            'q': text,
            'langpair': f'{source}|uk'
        },
        timeout=20
    )
    
    
    resp.raise_for_status()
    
    data = resp.json()
    
    return data['responseData']['translatedText']



print(tranlate_to_uk('Yura, te quiero. Gracias por existir, eres muy importante para mí. ❤️'))











