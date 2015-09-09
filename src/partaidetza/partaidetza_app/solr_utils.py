from partaidetza.partaidetza_app.forms import LoginForm, SearchBoxForm
from partaidetza.partaidetza_app.search_indexes import ProposalIndex
from haystack.query import SQ, SearchQuerySet
from partaidetza.settings import MORE_LIKE_THIS_RESULTS_NUMBER

def search_in_titles(index,query,language='all',type="all"):
    """Perform a query in title_* field"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(title_X=query)
    if type == "all":
        if language == 'eu':
            return index.objects.filter(title_eu=query)
        elif language == 'es':
            return index.objects.filter(title_es=query)
        elif language == 'en':
            return index.objects.filter(title_en=query)
        elif language == 'fr':
            return index.objects.filter(title_en=query)
        elif language == 'all':
            return index.objects.filter(SQ(title_eu=query)|SQ(title_es=query)|SQ(title_en=query)|SQ(title_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter(title_eu=query,type=type)
        elif language == 'es':
            return index.objects.filter(title_es=query,type=type)
        elif language == 'en':
            return index.objects.filter(title_en=query,type=type)
        elif language == 'fr':
            return index.objects.filter(title_en=query,type=type)
        elif language == 'all':
            return index.objects.filter((SQ(title_eu=query)|SQ(title_es=query)|SQ(title_en=query)|SQ(title_fr=query)),type=type)
        
def search_in_summaries(index,query,language='all',type="all"):
    """Perform a query in summary_* field"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(summary_X=query)
    if type == "all":
        if language == 'eu':
            return index.objects.filter(summary_eu=query)
        elif language == 'es':
            return index.objects.filter(summary_es=query)
        elif language == 'en':
            return index.objects.filter(summary_en=query)
        elif language == 'fr':
            return index.objects.filter(summary_en=query)
        elif language == 'all':
            return index.objects.filter(SQ(summary_eu=query)|SQ(summary_es=query)|SQ(summary_en=query)|SQ(summary_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter(summary_eu=query,type=type)
        elif language == 'es':
            return index.objects.filter(summary_es=query,type=type)
        elif language == 'en':
            return index.objects.filter(summary_en=query,type=type)
        elif language == 'fr':
            return index.objects.filter(summary_en=query,type=type)
        elif language == 'all':
            return index.objects.filter((SQ(summary_eu=query)|SQ(summary_es=query)|SQ(summary_en=query)|SQ(summary_fr=query)),type=type)
        
def search_in_recipients(index,query,language='all',type="all"):
    """Perform a query in recipient_* field"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(recipient_X=query)
    if type =="all":
        if language == 'eu':
            return index.objects.filter(recipient_eu=query)
        elif language == 'es':
            return index.objects.filter(recipient_es=query)
        elif language == 'en':
            return index.objects.filter(recipient_en=query)
        elif language == 'fr':
            return index.objects.filter(recipient_en=query)
        elif language == 'all':
            return index.objects.filter(SQ(recipient_eu=query)|SQ(recipient_es=query)|SQ(recipient_en=query)|SQ(recipient_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter(recipient_eu=query,type=type)
        elif language == 'es':
            return index.objects.filter(recipient_es=query,type=type)
        elif language == 'en':
            return index.objects.filter(recipient_en=query,type=type)
        elif language == 'fr':
            return index.objects.filter(recipient_en=query,type=type)
        elif language == 'all':
            return index.objects.filter((SQ(recipient_eu=query)|SQ(recipient_es=query)|SQ(recipient_en=query)|SQ(recipient_fr=query)),type=type)
        
def search_in_necessities(index,query,language='all',type="all"):
    """Perform a query in necessity_* field"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(necessity_X=query)
    if type=="all":
        if language == 'eu':
            return index.objects.filter(necessity_eu=query)
        elif language == 'es':
            return index.objects.filter(necessity_es=query)
        elif language == 'en':
            return index.objects.filter(necessity_en=query)
        elif language == 'fr':
            return index.objects.filter(necessity_en=query)
        elif language == 'all':
            return index.objects.filter(SQ(necessity_eu=query)|SQ(necessity_es=query)|SQ(necessity_en=query)|SQ(necessity_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter(necessity_eu=query,type=type)
        elif language == 'es':
            return index.objects.filter(necessity_es=query,type=type)
        elif language == 'en':
            return index.objects.filter(necessity_en=query,type=type)
        elif language == 'fr':
            return index.objects.filter(necessity_en=query,type=type)
        elif language == 'all':
            return index.objects.filter((SQ(necessity_eu=query)|SQ(necessity_es=query)|SQ(necessity_en=query)|SQ(necessity_fr=query)),type=type)
        
def search_in_wheres(index,query,language='all',type="all"):
    """Perform a query in where_* field"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(where_X=query)
    if type == "all":
        if language == 'eu':
            return index.objects.filter(where_eu=query)
        elif language == 'es':
            return index.objects.filter(where_es=query)
        elif language == 'en':
            return index.objects.filter(where_en=query)
        elif language == 'fr':
            return index.objects.filter(where_en=query)
        elif language == 'all':
            return index.objects.filter(SQ(where_eu=query)|SQ(where_es=query)|SQ(where_en=query)|SQ(where_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter(where_eu=query,type=type)
        elif language == 'es':
            return index.objects.filter(where_es=query,type=type)
        elif language == 'en':
            return index.objects.filter(where_en=query,type=type)
        elif language == 'fr':
            return index.objects.filter(where_en=query,type=type)
        elif language == 'all':
            return index.objects.filter((SQ(where_eu=query)|SQ(where_es=query)|SQ(where_en=query)|SQ(where_fr=query)),type=type)
            
def search_in_explanations(index,query,language='all',type="all"):
    """Perform a query in explanation_* field"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(explanation_X=query)
    if type == "all":
        if language == 'eu':
            return index.objects.filter(explanation_eu=query)
        elif language == 'es':
            return index.objects.filter(explanation_es=query)
        elif language == 'en':
            return index.objects.filter(explanation_en=query)
        elif language == 'fr':
            return index.objects.filter(explanation_en=query)
        elif language == 'all':
            return index.objects.filter(SQ(explanation_eu=query)|SQ(explanation_es=query)|SQ(explanation_en=query)|SQ(explanation_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter(explanation_eu=query,type=type)
        elif language == 'es':
            return index.objects.filter(explanation_es=query,type=type)
        elif language == 'en':
            return index.objects.filter(explanation_en=query,type=type)
        elif language == 'fr':
            return index.objects.filter(explanation_en=query,type=type)
        elif language == 'all':
            return index.objects.filter((SQ(explanation_eu=query)|SQ(explanation_es=query)|SQ(explanation_en=query)|SQ(explanation_fr=query)),type=type)    
            
            
def search_in_sources(index,query,language='all',type="all"):
    """Perform a query in source_* field"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(source_X=query)
    if type == "all":
        if language == 'eu':
            return index.objects.filter(source_eu=query)
        elif language == 'es':
            return index.objects.filter(source_es=query)
        elif language == 'en':
            return index.objects.filter(source_en=query)
        elif language == 'fr':
            return index.objects.filter(source_en=query)
        elif language == 'all':
            return index.objects.filter(SQ(source_eu=query)|SQ(source_es=query)|SQ(source_en=query)|SQ(source_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter(source_eu=query,type=type)
        elif language == 'es':
            return index.objects.filter(source_es=query,type=type)
        elif language == 'en':
            return index.objects.filter(source_en=query,type=type)
        elif language == 'fr':
            return index.objects.filter(source_en=query,type=type)
        elif language == 'all':
            return index.objects.filter((SQ(source_eu=query)|SQ(source_es=query)|SQ(source_en=query)|SQ(source_fr=query)),type=type)                   
            
        
def search_in_all(index, query, language='all',type="all"):
    """Perform a query in all texts"""
    # IMPORTANT: This function needs to be adapted to new languages:
    # Add this to each new language:
    # elif language == 'X':
    #    return index.objects.filter(SQ(title_X=query)|SQ(summary_X=query)|SQ(recipient_X=query)|SQ(necessity_X=query)|SQ(where_X=query))
    if type == "all":
        if language == 'eu':
            return index.objects.filter(SQ(title_eu=query)|SQ(summary_eu=query)|SQ(recipient_eu=query)|SQ(necessity_eu=query)|SQ(where_eu=query)|SQ(explanation_eu=query)|SQ(source_eu=query))
        elif language == 'es':
            return index.objects.filter(SQ(title_es=query)|SQ(summary_es=query)|SQ(recipient_es=query)|SQ(necessity_es=query)|SQ(where_es=query)|SQ(explanation_es=query)|SQ(source_es=query))
        elif language == 'en':
            return index.objects.filter(SQ(title_en=query)|SQ(summary_en=query)|SQ(recipient_en=query)|SQ(necessity_en=query)|SQ(where_en=query)|SQ(explanation_en=query)|SQ(source_en=query))
        elif language == 'fr':
            return index.objects.filter(SQ(title_fr=query)|SQ(summary_fr=query)|SQ(recipient_fr=query)|SQ(necessity_fr=query)|SQ(where_fr=query)|SQ(explanation_fr=query)|SQ(source_fr=query))
        elif language == 'all':
            return index.objects.filter(SQ(text_eu=query)|SQ(text_es=query)|SQ(text_en=query)|SQ(text_fr=query))
    else:
        if language == 'eu':
            return index.objects.filter((SQ(title_eu=query)|SQ(summary_eu=query)|SQ(recipient_eu=query)|SQ(necessity_eu=query)|SQ(where_eu=query)|SQ(explanation_eu=query)|SQ(source_eu=query)),type=type)
        elif language == 'es':
            return index.objects.filter((SQ(title_es=query)|SQ(summary_es=query)|SQ(recipient_es=query)|SQ(necessity_es=query)|SQ(where_es=query)|SQ(explanation_es=query)|SQ(source_es=query)),type=type)
        elif language == 'en':
            return index.objects.filter((SQ(title_en=query)|SQ(summary_en=query)|SQ(recipient_en=query)|SQ(necessity_en=query)|SQ(where_en=query)|SQ(explanation_en=query)|SQ(source_en=query)),type=type)
        elif language == 'fr':
            return index.objects.filter((SQ(title_fr=query)|SQ(summary_fr=query)|SQ(recipient_fr=query)|SQ(necessity_fr=query)|SQ(where_fr=query)|SQ(explanation_fr=query)|SQ(source_fr=query)),type=type)
        elif language == 'all':
            return index.objects.filter((SQ(text_eu=query)|SQ(text_es=query)|SQ(text_en=query)|SQ(text_fr=query)),type=type)
            
######################
# MAIN SEARCH METHOD #
######################

def search(search_form):
    """Searches in Solr system"""

    results =[]
    index = ProposalIndex()
    if search_form.is_valid():
        search_form_cd = search_form.cleaned_data
        query = search_form_cd.get("search_query")
        type = search_form_cd.get("search_type")
        where = search_form_cd.get("search_where")
        area = search_form_cd.get("search_area")  
        language = search_form_cd.get("search_lang")
        # Is the query empty?
        if query == '' and type == 'all' and where == 'all' and area == 'all' and language == 'all':
            return False
        else: # the query is not empty 
            if type != 'all': # The type is selected, search only in the selection
                # Proposals
                if type == 'proposal':
                    if where != 'all': # where is selected, search only in the selection
                        if query != '': # The query is not empty
                            if language != 'all': # language is selected
                                # 'where' condition:
                                if where == 'title': # title+lang
                                    results = search_in_titles(index,query,language=language,type="Proposal")
                                elif where == 'summary': # summary+lang
                                    results = search_in_summaries(index,query,language=language,type="Proposal")
                                elif where == 'necessity': # necessity+lang
                                    results = search_in_necessities(index,query,language=language,type="Proposal")
                                elif where == 'recipient': # recipient+lang
                                    results = search_in_recipients(index,query,language=language,type="Proposal")
                                elif where == 'where': # where+lang
                                    results = search_in_wheres(index,query,language=language,type="Proposal")
                            else: # search in any language
                                if where == 'title': # title+lang
                                    results = search_in_titles(index,query,type="Proposal")
                                elif where == 'summary': # summary+lang
                                    results = search_in_summaries(index,query,type="Proposal")
                                elif where == 'necessity': # necessity+lang
                                    results = search_in_necessities(index,query,type="Proposal")
                                elif where == 'recipient': # recipient+lang
                                    results = search_in_recipients(index,query,type="Proposal")
                                elif where == 'where': # where+lang
                                    results = search_in_wheres(index,query,type="Proposal")
                        else:
                            pass #The query is empty, so do nothing
                            
                    else: # search everywhere
                        if query != '': # The query is not empty
                            if language != 'all': # language is selected
                                results = search_in_all(index,query,language=language,type="Proposal")
                            else:
                                results = search_in_all(index,query,language,type="Proposal")
                        else:
                            pass #The query is empty, so do nothing
                            
                else:        
                    # Projects
                    if where != 'all': # where is selected, search only in the selection
                        if query != '': # The query is not empty
                            if language != 'all': # language is selected
                                # 'where' condition:
                                if where == 'title': # title+lang
                                    results = search_in_titles(index,query,language=language,type="Project")
                                elif where == 'summary': # summary+lang
                                    results = search_in_summaries(index,query,language=language,type="Project")
                                elif where == 'necessity': # necessity+lang
                                    results = search_in_necessities(index,query,language=language,type="Project")
                                elif where == 'recipient': # recipient+lang
                                    results = search_in_recipients(index,query,language=language,type="Project")
                                elif where == 'where': # where+lang
                                    results = search_in_wheres(index,query,language=language,type="Project")
                                elif where == 'explanation': # explanation+lang
                                    results = search_in_explanations(index,query,language=language,type="Project")
                                elif where == 'source': # source+lang
                                    results = search_in_sources(index,query,language=language,type="Project")
                            else: # search in any language
                                if where == 'title': # title+lang
                                    results = search_in_titles(index,query,type="Project")
                                elif where == 'summary': # summary+lang
                                    results = search_in_summaries(index,query,type="Project")
                                elif where == 'necessity': # necessity+lang
                                    results = search_in_necessities(index,query,type="Project")
                                elif where == 'recipient': # recipient+lang
                                    results = search_in_recipients(index,query,type="Project")
                                elif where == 'where': # where+lang
                                    results = search_in_wheres(index,query,type="Project")
                                elif where == 'explanation': # explanation+lang
                                    results = search_in_explanations(index,query,type="Project")
                                elif where == 'source': # source+lang
                                    results = search_in_sources(index,query,type="Project")
                        else:
                            pass #The query is empty, so do nothing   
                    else: # search everywhere
                        if query != '': # The query is not empty
                            if language != 'all': # language is selected
                                results = search_in_all(index,query,language=language,type="Project")
                            else:
                                results = search_in_all(index,query,language,type="Project")
                        else:
                            pass #The query is empty, so do nothing             
            else: # Search everywhere
                if where != 'all': # where is selected, search only in the selection
                    if query != '': # The query is not empty
                        if language != 'all': # language is selected
                            # 'where' condition:
                            if where == 'title': # title+lang
                                results = search_in_titles(index,query,language=language,type="all")
                            elif where == 'summary': # summary+lang
                                results = search_in_summaries(index,query,language=language,type="all")
                            elif where == 'necessity': # summary+lang
                                results = search_in_necessities(index,query,language=language,type="all")
                            elif where == 'recipient': # summary+lang
                                results = search_in_recipients(index,query,language=language,type="all")
                            elif where == 'where': # summary+lang
                                results = search_in_wheres(index,query,language=language,type="all")
                        else: # search in any language
                            if where == 'title': # title+lang
                                results = search_in_titles(index,query,type="all")
                            elif where == 'summary': # summary+lang
                                results = search_in_summaries(index,query,type="all")
                            elif where == 'necessity': # summary+lang
                                results = search_in_necessities(index,query,type="all")
                            elif where == 'recipient': # summary+lang
                                results = search_in_recipients(index,query,type="all")
                            elif where == 'where': # summary+lang
                                results = search_in_wheres(index,query,type="all")
                    else:
                        pass #The query is empty, so do nothing
                            
                else: # search everywhere
                    if query != '': # The query is not empty
                        if language != 'all': # language is selected
                            results = search_in_all(index,query,language=language,type="all")
                        else:
                            results = search_in_all(index,query,language,type="all")
                    else:
                        pass #The query is empty, so do nothing
            
            # search in area
            if area != 'all':
                if results != []:
                    results = results.filter(area__contains=str(area))    
                else:
                    if type != "all":
                        results = index.objects.filter(area__contains=str(area),type=type.title())
                    else:
                        results = index.objects.filter(area__contains=str(area))
            
        print "RESULTS: ",results
        return results
    else:
        return False

############################
## MORE LIKE THIS METHODS ##
############################
  
def get_more_like_this(object,content_type):
    """Get related objects from Database"""
    related_objects = SearchQuerySet().filter(type=content_type).more_like_this(object)
    return related_objects[:MORE_LIKE_THIS_RESULTS_NUMBER]
    
def get_more_like_this_in_titles(query,language="all",type="all"):
    """Get related titles from Database"""
    related_titles = []
    if query!='':
        index =  ProposalIndex()
        related_titles = search_in_titles(index,query,language=language,type=type)
    return related_titles[:MORE_LIKE_THIS_RESULTS_NUMBER]
    
def get_more_like_this_in_summaries(query,language="all",type="all"):
    """Get related summaries from Database"""
    related_summaries = []
    if query!='':
        index =  ProposalIndex()
        related_summaries = search_in_summaries(index,query,language=language,type=type)
    return related_summaries[:MORE_LIKE_THIS_RESULTS_NUMBER]
    
def get_more_like_this_in_recipients(query,language="all",type="all"):
    """Get related recipients from Database"""
    related_recipients = []
    if query!='':
        index =  ProposalIndex()
        related_recipients = search_in_recipients(index,query,language=language,type=type)
    return related_recipients[:MORE_LIKE_THIS_RESULTS_NUMBER]
    
def get_more_like_this_in_necessities(query,language="all",type="all"):
    """Get related necessities from Database"""
    related_necessities = []
    if query!='':
        index =  ProposalIndex()
        related_necessities = search_in_necessities(index,query,language=language,type=type)
    return related_necessities[:MORE_LIKE_THIS_RESULTS_NUMBER]
    
def get_more_like_this_in_wheres(query,language="all",type="all"):
    """Get related wheres from Database"""
    related_wheres = []
    if query!='':
        index =  ProposalIndex()
        related_wheres = search_in_wheres(index,query,language=language,type=type)
    return related_wheres[:MORE_LIKE_THIS_RESULTS_NUMBER]
    
def get_more_like_this_in_sources(query,language="all",type="all"):
    """Get related sources from Database"""
    related_sources = []
    if query!='':
        index =  ProposalIndex()
        related_sources = search_in_sources(index,query,language=language,type=type)
    return related_sources[:MORE_LIKE_THIS_RESULTS_NUMBER]
    
def get_more_like_this_in_explanations(query,language="all",type="all"):
    """Get related explanations from Database"""
    related_explanations = []
    if query!='':
        index =  ProposalIndex()
        related_explanations = search_in_explanations(index,query,language=language,type=type)
    return related_explanations[:MORE_LIKE_THIS_RESULTS_NUMBER]
