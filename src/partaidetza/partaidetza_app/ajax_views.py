from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from partaidetza.partaidetza_app.models import Status, Area, Genre, Profile, Proposal, ProposalArea, ProposalDocument, Specification, SpecificationArea, ProjectCard, ProjectArea, ProjectComment, Criterion, ProposalCriterion, Vote, PresentialVotes
from partaidetza.partaidetza_app.forms import ModalCostForm, ModalAreaForm, ModalRecipientNumberForm, NewProposalTitleForm, \
NewProposalSummaryForm, NewProposalNecessityForm, NewProposalRecipientForm, NewProposalWhereForm,\
NewProposalSourceForm, NewProposalExplanationForm
from solr_utils import get_more_like_this_in_titles, get_more_like_this_in_summaries, get_more_like_this_in_necessities, get_more_like_this_in_recipients, get_more_like_this_in_wheres, get_more_like_this_in_sources, get_more_like_this_in_explanations
from utils import correct_language

@login_required
def ajax_vote(request):
    """Vote via ajax"""
    if request.GET:
        project_id = request.GET.get("project_id")
        project = ProjectCard.objects.get(id = int(project_id))
      
        response = project.vote(request.user)
        return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))
        
@login_required
def ajax_fond(request):
    """Fond via ajax"""
    if request.GET:
        proposal_id = request.GET.get("proposal_id")
        proposal = Proposal.objects.get(id = int(proposal_id))
      
        response = proposal.fond(request.user)
        return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))


def ajax_edit_proposal_cost(request):
    if request.GET:
        cost = request.GET.get('cost')
        form = ModalCostForm({"cost": cost})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_cost(cost)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("cost")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request)) 
            
 
def ajax_edit_proposal_area(request):
    response_proposal = None
    if request.GET:
        area = request.GET.getlist('area[]')
        form = ModalAreaForm({"area": area})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_area(area)
                response_proposal = proposal
            else:
                response = None
            return render_to_response("ajax/ajax_area_response.html",{"response": response,"proposal":response_proposal},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("area")
            return render_to_response("ajax/ajax_area_response.html",{"response": response,},context_instance=RequestContext(request))  
        
def ajax_edit_proposal_recipient_number(request):
    if request.GET:
        recipient_number = request.GET.get('recipient_number')
        form = ModalRecipientNumberForm({"recipient_number":recipient_number})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_recipient_number(recipient_number)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request)) 
            
def ajax_edit_proposal_title(request):
    if request.GET:
        language = request.GET.get("language")
        title = request.GET.get("title")
        form = NewProposalTitleForm({"title":title})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_title(title,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
            
            
def ajax_edit_proposal_summary(request):
    if request.GET:
        language = request.GET.get("language")
        summary = request.GET.get("summary")
        form = NewProposalSummaryForm({"summary":summary})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_summary(summary,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_proposal_necessity(request):
    if request.GET:
        language = request.GET.get("language")
        necessity = request.GET.get("necessity")
        form = NewProposalNecessityForm({"necessity":necessity})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_necessity(necessity,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
         
            
def ajax_edit_proposal_recipient(request):
    if request.GET:
        language = request.GET.get("language")
        recipient = request.GET.get("recipient")
        form = NewProposalRecipientForm({"recipient":recipient})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_recipient(recipient,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_proposal_where(request):
    if request.GET:
        language = request.GET.get("language")
        where = request.GET.get("where")
        form = NewProposalWhereForm({"where":where})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(user)):
                response = proposal.set_where(where,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
            
def ajax_get_proposal_area(request):
    areas =[]
    if request.GET:
        area = map(lambda x: int(x),request.GET.getlist('area[]'))
        areas = Area.objects.filter(id__in=area)
    return render_to_response("ajax/ajax_get_area_response.html",{"areas": areas},context_instance=RequestContext(request))     

def ajax_get_proposal_state(request):
    if request.GET:
        state = request.GET.get('state')
        state = Status.objects.get(id=int(state))
    return render_to_response("ajax/ajax_get_state_response.html",{"state": state},context_instance=RequestContext(request)) 
 
def ajax_edit_project_cost(request):
    if request.GET:
        cost = request.GET.get('cost')
        form = ModalCostForm({"cost": cost})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_cost(cost)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("cost")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request)) 
            
  
def ajax_edit_project_area(request):
    response_project = None
    if request.GET:
        area = request.GET.getlist('area[]')
        form = ModalAreaForm({"area": area})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_area(area)
                response_project = project
            else:
                response = None
            return render_to_response("ajax/ajax_area_response.html",{"response": response,"proposal":response_project},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("area")
            return render_to_response("ajax/ajax_area_response.html",{"response": response,},context_instance=RequestContext(request))    
 

 
        
def ajax_edit_project_recipient_number(request):
    if request.GET:
        recipient_number = request.GET.get('recipient_number')
        form = ModalRecipientNumberForm({"recipient_number":recipient_number})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_recipient_number(recipient_number)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
 
            
def ajax_edit_project_title(request):
    if request.GET:
        language = request.GET.get("language")
        title = request.GET.get("title")
        form = NewProposalTitleForm({"title":title})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_title(title,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
            
            
def ajax_edit_project_summary(request):
    if request.GET:
        language = request.GET.get("language")
        summary = request.GET.get("summary")
        form = NewProposalSummaryForm({"summary":summary})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_summary(summary,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_project_necessity(request):
    if request.GET:
        language = request.GET.get("language")
        necessity = request.GET.get("necessity")
        form = NewProposalNecessityForm({"necessity":necessity})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_necessity(necessity,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
         
            
def ajax_edit_project_recipient(request):
    if request.GET:
        language = request.GET.get("language")
        recipient = request.GET.get("recipient")
        form = NewProposalRecipientForm({"recipient":recipient})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_recipient(recipient,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_project_where(request):
    if request.GET:
        language = request.GET.get("language")
        where = request.GET.get("where")
        form = NewProposalWhereForm({"where":where})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_where(where,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))                              

def ajax_edit_project_source(request):
    if request.GET:
        language = request.GET.get("language")
        source = request.GET.get("source")
        form = NewProposalSourceForm({"source":source})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_source(source,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
            
def ajax_edit_project_explanation(request):
    if request.GET:
        language = request.GET.get("language")
        explanation = request.GET.get("explanation")
        form = NewProposalExplanationForm({"explanation":explanation})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(user)):
                response = project.set_explanation(explanation,language)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient_number")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))                                                          
            
@login_required          
def ajax_more_like_this_in_titles(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_titles(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request)) 
        
@login_required           
def ajax_more_like_this_in_summaries(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_summaries(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))   
        
@login_required           
def ajax_more_like_this_in_recipients(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_recipients(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))  
        
@login_required           
def ajax_more_like_this_in_necessities(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_necessities(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))    
        
@login_required        
def ajax_more_like_this_in_wheres(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_wheres(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))           
        
@login_required        
def ajax_more_like_this_in_sources(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_sources(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))          
     
@login_required        
def ajax_more_like_this_in_explanations(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_explanations(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))          

     
@login_required          
def ajax_more_like_this_in_events(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        objects = get_more_like_this_in_events(query,language=language)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))      
     
@login_required
def ajax_correct_language(request):
    language = request.GET.get("language")
    text = request.GET.get("text")
    response = correct_language(text,language)
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
    
    
@login_required
def ajax_validate_language(request):
    response = True
    for element in request.GET.keys():
        text = request.GET.get(element)
        language = element.split('_')[1]
        if text != "":            
            response = response and correct_language(text,language)
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
    
    
@login_required
def ajax_add_point_to_map_proposal(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        proposal_id = request.GET.get("proposal_id")
        proposal = Proposal.objects.get(id=int(proposal_id))
        proposal.set_map_point(float(lat),float(lng))
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))    
    
    
@login_required
def ajax_add_point_to_map_project(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        project_id = request.GET.get("project_id")
        project = ProjectCard.objects.get(id=int(project_id))
        project.set_map_point(float(lat),float(lng))
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))    
    
    
@login_required
def ajax_delete_point_from_map_proposal(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        proposal_id = request.GET.get("proposal_id")
        proposal = Proposal.objects.get(id=int(proposal_id))
        proposal.delete_map_point(float(lat),float(lng))
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))   
    
    
@login_required
def ajax_delete_point_from_map_project(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        project_id = request.GET.get("project_id")
        project = ProjectCard.objects.get(id=int(project_id))
        project.delete_map_point(float(lat),float(lng))
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))    
     
    
