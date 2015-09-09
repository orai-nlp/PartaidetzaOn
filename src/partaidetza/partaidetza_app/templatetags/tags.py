from django.template.defaultfilters import stringfilter
from django import template
from settings import *
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _,get_language
from partaidetza_app.views import Area
import json


register = template.Library()



@register.filter
@stringfilter
def int_to_string(value):
    return value
    
@register.filter
def new_or_none(value, string):
    if value is None or value == "":
        return _(string)
    else:
        return value      
        
@register.filter
def get_area_name(area_id):
    return Area.objects.get(id=int(area_id)).area
    
@register.filter
def correct_float_format(value):
    return str(value).replace(',','.')

@register.filter
def get_lang_form(dict,lang):
    """Get a form from a dict by lang"""
    return dict[lang]
    
    
@register.filter
def sort_by_default_language(list,lang):
    """Order language list by selected language"""
    sorted_list=[]
    for language in list:
        if language[0] == lang:
            sorted_list = [language]+sorted_list
        else:
            sorted_list += [language]
    return sorted_list
        
    
@register.filter
def clean_doc_name(doc):
    """Removes the timestamp from the file name"""
    return MEDIA_URL+"".join(doc.split('_')[1])


@register.filter
def show_login(url):
    """return true if login box needs to be visible"""
    print url
    return "?next" in url
    
    
@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter
def cut_text(obj):
    if len(obj)>300:
        return obj[:300]+'...'
    else:
        return obj
        
@register.filter
def get_dict_element(dict, key):
    """return a combined key dict element"""
    return dict[key]

@register.filter
def get_form_by_index(forms,index):
    return forms[index]

######################
## Haystack helpers ##
######################

@register.filter
def get_titles(object):
    titles = []
    for lang in LANGUAGES:
        try:
            title = object.get_title(lang[0])
        except Exception as error:
            title = ""
        titles += [title]
    return titles
    
@register.filter
def get_summaries(object):
    summaries = []
    for lang in LANGUAGES:
        try:
            summary = object.get_summary(lang[0])
        except Exception as error:
            summary = ""
        summaries += [summary]
    return summaries
    
@register.filter
def get_necessities(object):
    necessities = []
    for lang in LANGUAGES:
        try:
            necesity = object.get_necesity(lang[0])
        except Exception as error:
            necesity = ""
        necessities += [necesity]
    return necessities 
    
    
@register.filter
def get_recipients(object):
    recipients = []
    for lang in LANGUAGES:
        try:
            recipient = object.get_recipient(lang[0])
        except Exception as error:
            recipient = ""
        recipients += [recipient]
    return recipients
    
@register.filter
def get_wheres(object):
    wheres = []
    for lang in LANGUAGES:
        try:
            where = object.get_where(lang[0])
        except Exception as error:
            where = ""
        wheres += [where]
    return wheres   

@register.filter
def get_explanations(object):
    explanations = []
    for lang in LANGUAGES:
        try:
            explanation = object.get_explanation(lang[0])

        except Exception as error:
            explanation = ""
        explanations += [explanation]
    return explanations   
    
@register.filter
def get_sources(object):
    sources = []
    for lang in LANGUAGES:
        try:
            source = object.get_source(lang[0])
        except Exception as error:
            source = ""
        sources += [source]
    return sources       


############################
## MODEL'S GETTER METHODS ##    
############################

@register.filter
def get_title(object,lang):
    """Get the title of a object"""
    return object.get_title(lang)
    
@register.filter
def get_summary(object,lang):
    """Get the summary of a object"""
    return object.get_summary(lang)
    
@register.filter
def get_summary(object,lang):
    """Get the summary of a object"""
    return object.get_summary(lang)
    
@register.filter
def get_recipient(object,lang):
    """Get the recipient of a object"""
    return object.get_recipient(lang)
    
@register.filter
def get_necessity(object,lang):
    """Get the necessity of a object"""
    return object.get_necessity(lang)
    
@register.filter
def get_where(object,lang):
    """Get the where of a object"""
    return object.get_where(lang)
    
@register.filter
def get_explanation(object,lang):
    """Get the explanation of a object"""
    return object.get_explanation(lang)
    
@register.filter
def get_source(object,lang):
    """Get the source of a object"""
    return object.get_source(lang)
    
@register.filter
def already_voted(object,user):
    """Check if the project has been voted"""
    return object.already_voted(user)
    
@register.filter
def already_fonded(object,user):
    """Check if the project has been fonded"""
    return object.already_fonded(user)
    
@register.filter
def is_author(object,user):
    """Check if user the author of the object"""
    return object.is_author(user)    
    
@register.filter
def get_content(object,lang):
    """Get the title of a object"""
    return object.get_content(lang)
