import os, urllib2
from partaidetza.settings import LANGUAGES, OPENTRAD_CODE, AT_LANGUAGE_PRIORITY

# AUTOMATIC_TRANSLATION FUNCTIONS

def get_best_translation_source(dict,target_lang):
    """Get the best translation source"""
    translated_text = ""
    for source_lang in AT_LANGUAGE_PRIORITY:
        if source_lang != target_lang:
            if dict[source_lang] != '':
                translated_text = translate_text_opentrad(dict[source_lang].cleaned_data.get(\
                                                        dict[source_lang].cleaned_data.keys()[0]), source_lang, target_lang)
                if "Error: Mode " not in translated_text:
                    break
    return translated_text

def translate_text_opentrad(text, source_language, target_language):
    """Translate text automatically from source_language to target_language"""    
    
    url="http://api.opentrad.com/translate.php"
    url_text="?text="+text.strip()
    url_lang="&lang={0}-{1}".format(source_language,target_language)
    url_client="&cod_client="+OPENTRAD_CODE
    URL=url+url_text+url_lang+url_client

    try:
        return urllib2.urlopen(URL.replace(' ','%20').encode("utf-8")).read()
    except:
        return urllib2.urlopen(URL.replace(' ','%20')).read()   
