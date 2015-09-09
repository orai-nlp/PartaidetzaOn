from django.core.management.base import BaseCommand, CommandError

from settings import LANGUAGES, BASEDIR

def create_search_index_file():
    """Create search_indexes.py file in order to create Solr dynamic indexes"""
    ###############
    ## PROPOSALS ##
    ###############
    
    # LANGUAGE FIELDS
    proposal_language_fields = ""
    for lang in LANGUAGES:
        proposal_language_fields += "    text_"+lang[0]+"= indexes.CharField(use_template=True, template_name='search/indexes/partaidetza_app/proposal_text_"+lang[0]+".txt')\n"
        proposal_language_fields += "    title_"+lang[0]+"=indexes.CharField()\n"
        proposal_language_fields += "    summary_"+lang[0]+"=indexes.CharField()\n"
        proposal_language_fields += "    necessity_"+lang[0]+"=indexes.CharField()\n"
        proposal_language_fields += "    recipient_"+lang[0]+"=indexes.CharField()\n"
        proposal_language_fields += "    where_"+lang[0]+"=indexes.CharField()\n"
            
    # PREPARE METHODS    
    proposal_prepare_methods=""
        
    proposal_prepare_methods += """    def prepare_area(self,obj):
        try:
            return map(lambda x: int(x), Proposal.objects.get(id=int(obj.id)).get_area())
        except Exception as error:
            return []\n\n"""
            
    proposal_prepare_methods += """    def prepare_type(self,obj):
        return 'Proposal'\n\n"""    
    for lang in LANGUAGES:
        proposal_prepare_methods += """    def prepare_title_{0}(self,obj):
        try:
            return Proposal.objects.get(id=int(obj.id)).get_title('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        proposal_prepare_methods += """    def prepare_summary_{0}(self,obj):
        try:
            return Proposal.objects.get(id=int(obj.id)).get_summary('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        proposal_prepare_methods += """    def prepare_necessity_{0}(self,obj):
        try:
            return Proposal.objects.get(id=int(obj.id)).get_necessity('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        proposal_prepare_methods += """    def prepare_recipient_{0}(self,obj):
        try:
            return Proposal.objects.get(id=int(obj.id)).get_recipient('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        proposal_prepare_methods += """    def prepare_where_{0}(self,obj):
        try:
            return Proposal.objects.get(id=int(obj.id)).get_where('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        
    
    ##############
    ## PROJECTS ##
    ##############
    
    # LANGUAGE FIELDS
    project_language_fields = ""
    for lang in LANGUAGES:
        project_language_fields += "    text_"+lang[0]+"= indexes.CharField(use_template=True, template_name='search/indexes/partaidetza_app/project_text_"+lang[0]+".txt')\n"
        project_language_fields += "    title_"+lang[0]+"=indexes.CharField()\n"
        project_language_fields += "    summary_"+lang[0]+"=indexes.CharField()\n"
        project_language_fields += "    necessity_"+lang[0]+"=indexes.CharField()\n"
        project_language_fields += "    recipient_"+lang[0]+"=indexes.CharField()\n"
        project_language_fields += "    where_"+lang[0]+"=indexes.CharField()\n"
        project_language_fields += "    explanation_"+lang[0]+"=indexes.CharField()\n"
        project_language_fields += "    source_"+lang[0]+"=indexes.CharField()\n"
            
    # PREPARE METHODS    
    project_prepare_methods=""
        
    project_prepare_methods += """    def prepare_area(self,obj):
        try:
            return map(lambda x: int(x), ProjectCard.objects.get(id=int(obj.id)).get_area())
        except Exception as error:
            return []\n\n"""
    project_prepare_methods += """    def prepare_type(self,obj):
        return 'Project'\n\n"""     
        
    for lang in LANGUAGES:
        project_prepare_methods += """    def prepare_title_{0}(self,obj):
        try:
            return ProjectCard.objects.get(id=int(obj.id)).get_title('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        project_prepare_methods += """    def prepare_summary_{0}(self,obj):
        try:
            return ProjectCard.objects.get(id=int(obj.id)).get_summary('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        project_prepare_methods += """    def prepare_necessity_{0}(self,obj):
        try:
            return ProjectCard.objects.get(id=int(obj.id)).get_necessity('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        project_prepare_methods += """    def prepare_recipient_{0}(self,obj):
        try:
            return ProjectCard.objects.get(id=int(obj.id)).get_recipient('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        project_prepare_methods += """    def prepare_where_{0}(self,obj):
        try:
            return ProjectCard.objects.get(id=int(obj.id)).get_where('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        project_prepare_methods += """    def prepare_explanation_{0}(self,obj):
        try:
            return ProjectCard.objects.get(id=int(obj.id)).get_explanation('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        project_prepare_methods += """    def prepare_source_{0}(self,obj):
        try:
            return ProjectCard.objects.get(id=int(obj.id)).get_source('{0}')""".format(lang[0])+"""
        except Exception as error:
            return ''\n\n"""
        
     
    ############
    ## GLOBAL ##
    ############
    
    # FILE CONTENTS
    file_content = """
import datetime
from haystack import indexes
from partaidetza.partaidetza_app.models import Proposal, ProjectCard
                
                
class ProposalIndex(indexes.SearchIndex, indexes.Indexable):   
    text= indexes.CharField(document=True, use_template=True, template_name='search/indexes/partaidetza_app/proposal_text.txt') 
    recipient_number = indexes.IntegerField(model_attr='recipient_number')
    cost = indexes.FloatField(model_attr='cost')
    date = indexes.DateField(model_attr='date')
    author = indexes.IntegerField()
    area = indexes.MultiValueField()
    type = indexes.CharField()
    # LANGUAGE FIELDS:
{0}            
            
    def get_model(self):
        return Proposal
        
    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated.'''
        return self.get_model().objects.all()
        
{1}


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):   
    text= indexes.CharField(document=True, use_template=True, template_name='search/indexes/partaidetza_app/project_text.txt') 
    recipient_number = indexes.IntegerField(model_attr='recipient_number')
    cost = indexes.FloatField(model_attr='cost')
    date = indexes.DateField(model_attr='date')
    author = indexes.IntegerField()
    area = indexes.MultiValueField()
    status = indexes.IntegerField()
    type = indexes.CharField()
    
# LANGUAGE FIELDS:
{2}            
            
    def get_model(self):
        return ProjectCard
        
    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated.'''
        return self.get_model().objects.all()
        
{3} 
                
        
        """.format(proposal_language_fields,proposal_prepare_methods,project_language_fields,project_prepare_methods)
        
        
    search_indexes_file = open(BASEDIR+'/partaidetza_app/search_indexes.py','w')
    search_indexes_file.write(file_content)
    search_indexes_file.close()
        
    print BASEDIR+"/partaidetza_app/search_indexes.py created succesfully!"
    
    
def create_proposal_search_templates():
    """Create templates in order to create Solr dynamic indexes"""
    
    for lang in LANGUAGES:
        file_content = """
{% load tags %}

{{ object|get_title:'"""+lang[0]+"""' }}
{{ object|get_summary:'"""+lang[0]+"""' }}
{{ object|get_necessity:'"""+lang[0]+"""' }}
{{ object|get_recipient:'"""+lang[0]+"""' }}
{{ object|get_where:'"""+lang[0]+"""' }}    """
        template_file = open(BASEDIR+'/partaidetza_templates/search/indexes/partaidetza_app/proposal_text_'+lang[0]+'.txt','w')
        template_file.write(file_content)
        template_file.close()
        print BASEDIR+"/partaidetza_templates/search/indexes/partaidetza_app/proposal_text_"+lang[0]+".txt created succesfully!"
        

def create_project_search_templates():
    """Create templates in order to create Solr dynamic indexes"""
    
    for lang in LANGUAGES:
        file_content = """
{% load tags %}

{{ object|get_title:'"""+lang[0]+"""' }}
{{ object|get_summary:'"""+lang[0]+"""' }}
{{ object|get_necessity:'"""+lang[0]+"""' }}
{{ object|get_recipient:'"""+lang[0]+"""' }}
{{ object|get_where:'"""+lang[0]+"""' }}
{{ object|get_explanation:'"""+lang[0]+"""' }}
{{ object|get_source:'"""+lang[0]+"""' }}    """
        template_file = open(BASEDIR+'/partaidetza_templates/search/indexes/partaidetza_app/project_text_'+lang[0]+'.txt','w')
        template_file.write(file_content)
        template_file.close()
        print BASEDIR+"/partaidetza_templates/search/indexes/partaidetza_app/project_text_"+lang[0]+".txt created succesfully!"

class Command(BaseCommand):
    """Create search_indexes.py file and all needed templates in order to create Solr dynamic indexes"""
    help = 'Create search_indexes.py file and all needed templates in order to create Solr dynamic indexes'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        create_search_index_file()
        create_proposal_search_templates()
        create_project_search_templates()
        
