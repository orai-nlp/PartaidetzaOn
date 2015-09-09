from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _,get_language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext, loader
from partaidetza.partaidetza_app.models import Area, Genre, Profile, Proposal, ProposalArea, ProposalDocument, Specification, SpecificationArea, ProjectCard, ProjectArea, ProjectComment, Criterion, ProposalCriterion, Vote, PresentialVotes, Event
from partaidetza.partaidetza_app.forms import LoginForm, ProfileForm, RegisterForm, NewProposalForm, NewProposalTitleForm, NewProposalSummaryForm, NewProposalNecessityForm, NewProposalRecipientForm, NewProposalWhereForm,\
NewProposalSourceForm, NewProposalExplanationForm, UploadForm, SearchBoxForm, ModalCostForm,\
ModalRecipientNumberForm, CriterionForm, ModalUploadForm, CommentForm, CommentParentForm, NewAcceptedProposalForm,\
ModalAreaForm, CoordinatesForm, NewEventForm, NewEventDateForm
from db_views import db_register, db_update_profile, db_add_proposal, db_add_accepted_proposals, db_add_accepted_proposal_manually, db_add_proposal_criterions, db_edit_attached_documents_to_proposal, db_edit_attached_documents_to_project, db_add_comment, db_add_event
from utils import *
from solr_utils import *
from partaidetza.settings import LANGUAGES, OPENTRAD_CODE, AT_LANGUAGE_PRIORITY, ACCEPTED_IMAGE_FORMATS
from django.http.response import HttpResponse
from django.contrib.auth.decorators import user_passes_test



def home(request):
    """Render main template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    if request.POST:
        # User tries to log in
        if "login_button" in request.POST:
            profile = log_in(request)
            if profile is None:
                login_form = LoginForm(request.POST)
                login_form.is_valid()
               
    # TODO: Hau mugatu beharko da
    project_list = ProjectCard.objects.all()
    events = Event.objects.all().order_by('date')
    
    d = {"login_form":login_form, "search_form":search_form, "project_list":project_list, "events": events}
    if login_needed(request):
        d["login_needed"]=True
        
    
    return render_to_response('home.html', d, context_instance = RequestContext(request))
    
    
@login_required
def profile(request):
    """Render profile template
    """
    # action status
    profile_status = 1
    login_status = 1
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    profile_form = ProfileForm()
    
    if request.POST:
        if "profile_button" in request.POST:
            profile_form=ProfileForm(request.POST)
            profile_value = db_update_profile(profile_form)
            profile_status = profile_value[0]
            if profile_status == 0: # validation error
                profile_form = profile_value[1]
                d = {"profile_form":profile_form , "login_form":login_form, "search_form":search_form}
                return render_to_response('profile.html', d, context_instance = RequestContext(request))
            elif profile_status == 1: # update OK!              
                return redirect('/')
                
            elif profile_status == 2: # error
                pass
                # TODO! Errore template bat!
    else:
        # load profile information
        profile = Profile.objects.get(user=request.user)
        profile_initial={'first_name':profile.user.first_name,\
                        'last_name':profile.user.last_name,\
                        'genre':profile.genre.id,\
                        'birth_date': profile.birth_date,\
                        'NAN': profile.NAN,\
                        'email':profile.user.email,\
                        'institution': profile.institution,\
                        'institution_name':profile.institution_name,\
                        'country': profile.country,\
                        'info': profile.info}
        profile_form = ProfileForm(initial=profile_initial)
        
    
    
    d = {"login_form":login_form, "search_form":search_form, "profile_form":profile_form}
    
    return render_to_response('profile.html', d, context_instance = RequestContext(request))
    
    
def register(request):
    """Render register template
    """    
    # action status
    register_status = 1
    login_status = 1
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    if request.POST:
        if "register_button" in request.POST:
            register_form=RegisterForm(request.POST)
            register_value = db_register(register_form)
            register_status = register_value[0]
            if register_status == 0: # validation error
                register_form = register_value[1]
                d = {"register_form":register_form , "login_form":login_form, "search_form":search_form}
                return render_to_response('register.html', d, context_instance = RequestContext(request))
            elif register_status == 1: # login OK!
                # Log in user:
                user = register_value[1]              
                auth_login(request,user)                
                return redirect('/')
                
            elif register_status == 2: # error
                pass
                # TODO! Errore template bat!
                
        else:
            register_form = RegisterForm()
            
        if "login_button" in request.POST:
            profile = log_in(request)
            if profile is None:
                login_form = LoginForm(request.POST)
                login_form.is_valid()
                login_status = 0
                d = {"register_form":register_form , "login_form":login_form, "search_form":search_form}
                return render_to_response('register.html', d, context_instance = RequestContext(request))
    else:
        # Initialize specific forms
        register_form = RegisterForm()
        
    d = {"register_form":register_form, "login_form":login_form, "search_form":search_form}
    
    return render_to_response('register.html', d, context_instance = RequestContext(request))
    
    
@login_required
def new_proposal(request):
    """Render new proposal template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)    
    print request.POST
    if request.POST:
        if "new_proposal_button" in request.POST:
            new_proposal_form = NewProposalForm(request.POST)
            upload_formset = formset_factory(UploadForm)            
            upload_form = upload_formset(request.POST,request.FILES,prefix='form')
            coordinates_form = CoordinatesForm(request.POST)
            title_dict = {}
            summary_dict = {}
            necessity_dict = {}
            recipient_dict = {}
            where_dict = {}
            # Generate forms for each language
            for lang in LANGUAGES:
                title = NewProposalTitleForm(request.POST, prefix="title_"+lang[0])
                title_dict[lang[0]]=title
                summary = NewProposalSummaryForm(request.POST, prefix="summary_"+lang[0])
                summary_dict[lang[0]]=summary    
                necessity = NewProposalNecessityForm(request.POST, prefix="necessity_"+lang[0])
                necessity_dict[lang[0]]=necessity
                recipient = NewProposalRecipientForm(request.POST, prefix="recipient_"+lang[0])
                recipient_dict[lang[0]]=recipient
                where = NewProposalWhereForm(request.POST, prefix="where_"+lang[0])
                where_dict[lang[0]]=where

            proposal_value=db_add_proposal(new_proposal_form,\
                                        title_dict,\
                                        summary_dict,\
                                        necessity_dict,\
                                        recipient_dict,\
                                        where_dict,\
                                        upload_form,\
                                        coordinates_form,\
                                        request.user.profile)
            proposal_status = proposal_value[0]
            if proposal_status == 0: # validation error
                d = {"accepted_image_formats": ACCEPTED_IMAGE_FORMATS, "at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE, "new_proposal_form":new_proposal_form, "upload_forms": upload_form,"login_form":login_form, "search_form":search_form, "title_dict":title_dict, "summary_dict": summary_dict, "necessity_dict": necessity_dict, "recipient_dict": recipient_dict, "where_dict": where_dict,"upload_forms":upload_form}
    
                return render_to_response('new_proposal.html', d, context_instance = RequestContext(request))
            
            elif proposal_status == 1: # save OK!
                proposal = proposal_value[1]           
                return redirect('/proposal/'+str(proposal.id))
                
            elif proposal_status == 2: # error
                pass
                # TODO! Errore template bat!
    else:
        new_proposal_form = NewProposalForm()
        coordinates_form = CoordinatesForm()
        upload_formset = formset_factory(UploadForm,extra=1)            
        upload_form = upload_formset(prefix='form')
        title_dict = {}
        summary_dict = {}
        necessity_dict = {}
        recipient_dict = {}
        where_dict = {}
        # Generate forms for each language
        for lang in LANGUAGES:
            title = NewProposalTitleForm(prefix="title_"+lang[0])
            title_dict[lang[0]]=title
            summary = NewProposalSummaryForm(prefix="summary_"+lang[0])
            summary_dict[lang[0]]=summary    
            necessity = NewProposalNecessityForm(prefix="necessity_"+lang[0])
            necessity_dict[lang[0]]=necessity
            recipient = NewProposalRecipientForm(prefix="recipient_"+lang[0])
            recipient_dict[lang[0]]=recipient
            where = NewProposalWhereForm(prefix="where_"+lang[0])
            where_dict[lang[0]]=where
            
        
    
    d = {"accepted_image_formats": ACCEPTED_IMAGE_FORMATS, "at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE, "new_proposal_form":new_proposal_form, "upload_forms": upload_form, "login_form":login_form, "search_form":search_form, "title_dict":title_dict, "summary_dict": summary_dict, "necessity_dict": necessity_dict, "recipient_dict": recipient_dict, "where_dict": where_dict, "upload_forms":upload_form, "coordinates_form": coordinates_form}
    
    return render_to_response('new_proposal.html', d, context_instance = RequestContext(request))
 
 
@login_required
def new_accepted_proposal_manually(request):
    """Render new accepted proposal template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)    
    if request.POST:
        if "new_accepted_proposal_button" in request.POST:
            new_accepted_proposal_form = NewAcceptedProposalForm(request.POST)
            coordinates_form = CoordinatesForm(request.POST)
            upload_formset = formset_factory(UploadForm)            
            upload_form = upload_formset(request.POST,request.FILES,prefix='form')
            title_dict = {}
            summary_dict = {}
            necessity_dict = {}
            recipient_dict = {}
            where_dict = {}
            source_dict = {}
            explanation_dict = {}
            # Generate forms for each language
            for lang in LANGUAGES:
                title = NewProposalTitleForm(request.POST, prefix="title_"+lang[0])
                title_dict[lang[0]]=title
                summary = NewProposalSummaryForm(request.POST, prefix="summary_"+lang[0])
                summary_dict[lang[0]]=summary    
                necessity = NewProposalNecessityForm(request.POST, prefix="necessity_"+lang[0])
                necessity_dict[lang[0]]=necessity
                recipient = NewProposalRecipientForm(request.POST, prefix="recipient_"+lang[0])
                recipient_dict[lang[0]]=recipient
                where = NewProposalWhereForm(request.POST, prefix="where_"+lang[0])
                where_dict[lang[0]]=where
                source = NewProposalSourceForm(request.POST, prefix="source_"+lang[0])
                source_dict[lang[0]]=source
                explanation = NewProposalExplanationForm(request.POST, prefix="explanation_"+lang[0])
                explanation_dict[lang[0]]=explanation

            accepted_proposal_value=db_add_accepted_proposal_manually(new_accepted_proposal_form,\
                                        title_dict,\
                                        summary_dict,\
                                        necessity_dict,\
                                        recipient_dict,\
                                        where_dict,\
                                        source_dict,\
                                        explanation_dict,\
                                        upload_form,\
                                        coordinates_form,\
                                        request.user.profile)
            accepted_proposal_status = accepted_proposal_value[0]
            if accepted_proposal_status == 0: # validation error
                d = {"accepted_image_formats": ACCEPTED_IMAGE_FORMATS,"at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE, "new_accepted_proposal_form":new_accepted_proposal_form, "upload_forms": upload_form,"login_form":login_form, "search_form":search_form, "title_dict":title_dict, "summary_dict": summary_dict, "necessity_dict": necessity_dict, "recipient_dict": recipient_dict, "where_dict": where_dict, "source_dict": source_dict, "explanation_dict": explanation_dict, "upload_forms":upload_form, "coordinates_form": coordinates_form}
    
                return render_to_response('new_accepted_proposal_manually.html', d, context_instance = RequestContext(request))
            
            elif accepted_proposal_status == 1: # save OK!
                accepted_proposal = accepted_proposal_value[1]           
                return redirect('/accepted_proposal/'+str(accepted_proposal.id))
                
            elif accepted_proposal_status == 2: # error
                pass
                # TODO! Errore template bat!
    else:
        new_accepted_proposal_form = NewAcceptedProposalForm()
        upload_formset = formset_factory(UploadForm,extra=1)            
        upload_form = upload_formset(prefix='form')
        coordinates_form = CoordinatesForm()
        title_dict = {}
        summary_dict = {}
        necessity_dict = {}
        recipient_dict = {}
        where_dict = {}
        source_dict = {}
        explanation_dict = {}
        # Generate forms for each language
        for lang in LANGUAGES:
            title = NewProposalTitleForm(prefix="title_"+lang[0])
            title_dict[lang[0]]=title
            summary = NewProposalSummaryForm(prefix="summary_"+lang[0])
            summary_dict[lang[0]]=summary    
            necessity = NewProposalNecessityForm(prefix="necessity_"+lang[0])
            necessity_dict[lang[0]]=necessity
            recipient = NewProposalRecipientForm(prefix="recipient_"+lang[0])
            recipient_dict[lang[0]]=recipient
            where = NewProposalWhereForm(prefix="where_"+lang[0])
            where_dict[lang[0]]=where
            source = NewProposalSourceForm(request.POST, prefix="source_"+lang[0])
            source_dict[lang[0]]=source
            explanation = NewProposalExplanationForm(request.POST, prefix="explanation_"+lang[0])
            explanation_dict[lang[0]]=explanation
            
        
    
    d = {"accepted_image_formats": ACCEPTED_IMAGE_FORMATS,"at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE, "new_accepted_proposal_form":new_accepted_proposal_form, "upload_forms": upload_form, "login_form":login_form, "search_form":search_form, "title_dict":title_dict, "summary_dict": summary_dict, "necessity_dict": necessity_dict, "recipient_dict": recipient_dict, "where_dict": where_dict, "source_dict": source_dict, "explanation_dict": explanation_dict, "upload_forms":upload_form, "coordinates_form": coordinates_form}
    
    return render_to_response('new_accepted_proposal_manually.html', d, context_instance = RequestContext(request))   
    
@user_passes_test(lambda u: not u.is_anonymous() and u.profile.has_advanced_permissions(),login_url='/')
def new_accepted_proposal(request):
    """Render new accepted proposal template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)    
    
    if request.POST:
        if "new_accepted_proposal_button" in request.POST:           
            upload_form = UploadForm(request.POST,request.FILES)   
            db_add_accepted_proposals(upload_form, request.user.profile)        
    else:
        
        upload_form = UploadForm() 
        
    d = {"upload_form": upload_form, "login_form":login_form, "search_form":search_form}
    
    return render_to_response('new_accepted_proposal.html', d, context_instance = RequestContext(request))    


@user_passes_test(lambda u: not u.is_anonymous() and u.profile.has_advanced_permissions(),login_url='/')
def manage_proposals(request):
    """Render manage proposals template"""
    login_form, search_form = base_forms_initialization(request)
    
    proposal_list = Proposal.objects.all()
    # TODO: Zerrenda hau nolabait mugatu
    proposal_list = proposal_list[max(len(proposal_list)-500,0):]
    
    d = {"login_form":login_form, "search_form":search_form, "proposal_list":proposal_list}
    
    return render_to_response('manage_proposals.html', d, context_instance = RequestContext(request))   
    
@login_required   
def manage_my_proposals(request):
    """Render manage my proposals template"""
    login_form, search_form = base_forms_initialization(request)
    
    proposal_list=Proposal.objects.filter(author = request.user.profile)
    
    d = {"login_form":login_form, "search_form":search_form, "proposal_list":proposal_list}
    
    return render_to_response('manage_my_proposals.html', d, context_instance = RequestContext(request))     
      

@user_passes_test(lambda u: not u.is_anonymous() and (u.profile.is_admin() or u.profile.is_manager() or u.profile.is_technician()),login_url='/')
def get_xlsx(request, proposal_id):
    
    file = create_project_info_file(proposal_id)
    response = HttpResponse(open(file).read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=proposal_"+str(proposal_id)+".xlsx"

    return response

@user_passes_test(lambda u: not u.is_anonymous() and (u.profile.is_admin() or u.profile.is_manager() or u.profile.is_technician()),login_url='/')    
def get_multiple_xlsx(request, proposal_id_list):
    
    id_list = proposal_id_list[1:].split(',')
    file = create_multiple_project_info_file(id_list)
    response = HttpResponse(open(file).read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=proposal_"+"_".join(id_list)+".xlsx"

    return response
    
@user_passes_test(lambda u: not u.is_anonymous() and (u.profile.is_admin() or u.profile.is_manager()),login_url='/')
def delete_proposals(request,proposal_id_list):
    id_list = proposal_id_list[1:].split(',')
    for proposal_id in id_list:
        if proposal_id != '':
            proposal = Proposal.objects.get(id=int(proposal_id))
            proposal.delete_proposal()
        
    return redirect('/manage_proposals/')

@user_passes_test(lambda u: not u.is_anonymous() and (u.profile.is_admin() or u.profile.is_manager()),login_url='/')
def delete_projects(request,project_id_list):
    id_list = project_id_list[1:].split(',')
    for project_id in id_list:
        if project_id != '':
            project = ProjectCard.objects.get(id=int(project_id))
            project.delete_project()
        
    return redirect('/manage_proposals/')

@user_passes_test(lambda u: not u.is_anonymous() and u.profile.has_advanced_permissions(),login_url='/')
def manage_criterions(request):
    """Render manage criterions template"""
    login_form, search_form = base_forms_initialization(request)
    proposal_list = Proposal.objects.all()
    criterion_list = Criterion.objects.all().order_by('id')
    print request.POST
    if request.POST:
        if "manage_criterions_button" in request.POST:
            changed_proposal_criterions = [key for key, value in request.POST.iteritems() if key.startswith("criterion") and key.endswith("changed") and value == "changed"]                 
            
            db_add_proposal_criterions(changed_proposal_criterions, criterion_list, request)
       
    proposal_criterions = {}
    for proposal in proposal_list:
        Criterion_Form = formset_factory(CriterionForm, extra=0)
        initial=[]
        for criterion in criterion_list:
            initial+=[{"criterion":proposal.get_criterion(criterion)}]
        
        proposal_criterions[proposal.id]=Criterion_Form(initial=initial, prefix="criterion_"+str(proposal.id))
    d = {"login_form":login_form, "search_form":search_form, "proposal_list":proposal_list, "criterion_list":criterion_list, "proposal_criterions":proposal_criterions}
    
    return render_to_response('manage_criterions.html', d, context_instance = RequestContext(request))     

'''@user_passes_test(lambda u: not u.is_anonymous() and u.profile.has_advanced_permissions(),login_url='/')
def manage_accepted_proposals(request):
    """Render manage accepted proposal template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    accepted_proposal_list=ProjectCard.objects.all()
    
    # Pagination:
    paginator = Paginator(accepted_proposal_list, 10)
    page = request.GET.get('page')
    try:
        accepted_proposal_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        accepted_proposal_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        accepted_proposal_list = paginator.page(paginator.num_pages)
    
    d = {"login_form":login_form, "search_form":search_form, "accepted_proposal_list":accepted_proposal_list}
    
    return render_to_response('manage_accepted_proposals.html', d, context_instance = RequestContext(request))   '''
    
@user_passes_test(lambda u: not u.is_anonymous() and u.profile.has_advanced_permissions(),login_url='/')
def manage_accepted_proposals(request):
    """Render manage proposals template"""
    login_form, search_form = base_forms_initialization(request)
    
    accepted_proposal_list=ProjectCard.objects.all()
    # TODO: Zerrenda hau nolabait mugatu
    accepted_proposal_list = accepted_proposal_list[max(len(accepted_proposal_list)-500,0):]
    
    d = {"login_form":login_form, "search_form":search_form, "accepted_proposal_list":accepted_proposal_list}
    
    return render_to_response('manage_accepted_proposals.html', d, context_instance = RequestContext(request))        

    
def proposals(request):
    """Render proposals template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    if request.GET:
        if "area" in request.GET:
            area = request.GET.get("area")
            by_area = Area.objects.get(id=int(area))
            proposal_list = ProposalArea.objects.get_proposals_by_area(area)
        else:
            by_area = False
            proposal_list=Proposal.objects.all()
    else:
        by_area = False
        proposal_list=Proposal.objects.all()
    
    # Pagination:
    paginator = Paginator(proposal_list, 10)
    page = request.GET.get('page')
    try:
        proposal_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        proposal_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        proposal_list = paginator.page(paginator.num_pages)
    
    d = {"login_form":login_form, "search_form":search_form, "proposal_list":proposal_list, "by_area": by_area}
    
    return render_to_response('proposals.html', d, context_instance = RequestContext(request))
    

def proposals_by_area(request):
    """Render proposals template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    proposals_by_area = {}
    for area in Area.objects.all():
        proposals_by_area[area]=ProposalArea.objects.filter(area=area)
        
        
    
    
    d = {"login_form":login_form, "search_form":search_form, "proposals_by_area":proposals_by_area}
    
    return render_to_response('proposals_by_area.html', d, context_instance = RequestContext(request))
 
    
def accepted_proposals(request):
    """Render accepted proposals template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    if request.GET:
        if "area" in request.GET:
            area = request.GET.get("area")
            by_area = Area.objects.get(id=int(area))
            proposal_list = ProjectArea.objects.get_proposals_by_area(area)
        else:
            by_area = False
            proposal_list=ProjectCard.objects.all()
    else:
        by_area = False
        proposal_list=ProjectCard.objects.all()
    
    
    
    # Pagination:
    paginator = Paginator(proposal_list, 10)
    page = request.GET.get('page')
    try:
        proposal_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        proposal_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        proposal_list = paginator.page(paginator.num_pages)
    d = {"login_form":login_form, "search_form":search_form, "accepted_proposal_list":proposal_list, "by_area": by_area}
    
    return render_to_response('accepted_proposals.html', d, context_instance = RequestContext(request))

'''@login_required    
def vote(request):
    """Render vote list template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    proposal_list=Proposal.objects.all()
    d = {"login_form":login_form, "search_form":search_form, "proposal_list":proposal_list}
    
    return render_to_response('vote.html', d, context_instance = RequestContext(request))    '''
    
def accepted_proposals_by_area(request):
    """Render proposals template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    accepted_proposals_by_area = {}
    for area in Area.objects.all():
        accepted_proposals_by_area[area]=ProjectArea.objects.filter(area=area)
        
        
    
    
    d = {"login_form":login_form, "search_form":search_form, "accepted_proposals_by_area":accepted_proposals_by_area}
    
    return render_to_response('accepted_proposals_by_area.html', d, context_instance = RequestContext(request))
     
    
    
def proposal(request,proposal_id):
    """Render new proposal template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    proposal=Proposal.objects.get(id=int(proposal_id))
    related = get_more_like_this(proposal,"proposal")
    
    # Modal editions:
    if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
        cost_form = ModalCostForm(initial = {"cost":proposal.cost})
        recipient_number_form = ModalRecipientNumberForm(initial = {"recipient_number":proposal.recipient_number})
        area_form = ModalAreaForm(initial = {"area":proposal.get_area})
        title_dict = {}
        summary_dict = {}
        necessity_dict = {}
        recipient_dict = {}
        where_dict = {}
        for lang in LANGUAGES:
            title = NewProposalTitleForm(initial = {"title":proposal.get_title(lang[0])}, prefix="title_"+lang[0])
            title_dict[lang[0]]=title
            summary = NewProposalSummaryForm(initial = {"summary":proposal.get_summary(lang[0])}, prefix="summary_"+lang[0])
            summary_dict[lang[0]]=summary
            necessity = NewProposalNecessityForm(initial = {"necessity":proposal.get_necessity(lang[0])}, prefix="necessity_"+lang[0])
            necessity_dict[lang[0]]=necessity
            recipient = NewProposalRecipientForm(initial = {"recipient":proposal.get_recipient(lang[0])}, prefix="recipient_"+lang[0])
            recipient_dict[lang[0]]=recipient
            where = NewProposalWhereForm(initial = {"where":proposal.get_where(lang[0])}, prefix="where_"+lang[0])
            where_dict[lang[0]]=where
        upload_formset = formset_factory(ModalUploadForm, extra=1)
        upload_initial = []
        for doc in proposal.get_documents_object():      
            upload_initial += [{"id":doc.id, "name":doc.doc}]        
        upload_form = upload_formset(initial=upload_initial, prefix='form')
    else:
        cost_form = None
        recipient_number_form =None
        area_form = None
        title_dict = None
        summary_dict = None
        necessity_dict = None
        recipient_dict = None
        where_dict = None
        upload_form = None
    
    
    # Criterion treadment ############################################################################
    if not request.user.is_anonymous() and request.user.profile.has_advanced_permissions():
        criterion_list = Criterion.objects.all().order_by('id')
        if request.POST:
            if "manage_criterions_button" in request.POST:
                changed_proposal_criterions = [key for key, value in request.POST.iteritems() if key.startswith("criterion") and key.endswith("changed") and value == "changed"]      
                                
                db_add_proposal_criterions(changed_proposal_criterions, criterion_list, request)
    
        
        Criterion_Form = formset_factory(CriterionForm, extra=0)
        initial=[]
        for criterion in criterion_list:
            initial+=[{"criterion":proposal.get_criterion(criterion)}]            
            proposal_criterions=Criterion_Form(initial=initial, prefix="criterion_"+str(proposal.id)) 
    else:
        criterion_list = None
        proposal_criterions = None
       
    ###################################################################################################
    if request.POST:
        if "attached_documents_button" in request.POST:
            upload_formset = formset_factory(ModalUploadForm, extra=1)                 
            upload_form = upload_formset(request.POST,request.FILES, prefix='form')
            if upload_form.is_valid():
                db_edit_attached_documents_to_proposal(upload_form,proposal)
        
    
    
    d = {"login_form":login_form, "search_form":search_form, "proposal":proposal, "related": related, \
        "at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE,\
        "cost_form": cost_form, "recipient_number_form": recipient_number_form,\
         "title_dict": title_dict, "summary_dict": summary_dict, "necessity_dict": necessity_dict,\
         "recipient_dict": recipient_dict, "where_dict": where_dict, "upload_forms": upload_form, "area_form": area_form,\
        "criterion_list":criterion_list, "proposal_criterions":proposal_criterions}

    return render_to_response('proposal.html', d, context_instance = RequestContext(request))

    
def accepted_proposal(request,proposal_id):
    """Render accepted proposal template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    proposal=ProjectCard.objects.get(id=int(proposal_id))
    related = get_more_like_this(proposal, "project")
    comments = proposal.get_comments()
    
    # Modal editions:
    if not request.user.is_anonymous() and request.user.profile.has_advanced_permissions():
        cost_form = ModalCostForm(initial = {"cost":proposal.cost})
        recipient_number_form = ModalRecipientNumberForm(initial = {"recipient_number":proposal.recipient_number})
        area_form = ModalAreaForm(initial = {"area":proposal.get_area})
        title_dict = {}
        summary_dict = {}
        necessity_dict = {}
        recipient_dict = {}
        where_dict = {}
        source_dict = {}
        explanation_dict = {}
        for lang in LANGUAGES:
            title = NewProposalTitleForm(initial = {"title":proposal.get_title(lang[0])}, prefix="title_"+lang[0])
            title_dict[lang[0]]=title
            summary = NewProposalSummaryForm(initial = {"summary":proposal.get_summary(lang[0])}, prefix="summary_"+lang[0])
            summary_dict[lang[0]]=summary
            necessity = NewProposalNecessityForm(initial = {"necessity":proposal.get_necessity(lang[0])}, prefix="necessity_"+lang[0])
            necessity_dict[lang[0]]=necessity
            recipient = NewProposalRecipientForm(initial = {"recipient":proposal.get_recipient(lang[0])}, prefix="recipient_"+lang[0])
            recipient_dict[lang[0]]=recipient
            where = NewProposalWhereForm(initial = {"where":proposal.get_where(lang[0])}, prefix="where_"+lang[0])
            where_dict[lang[0]]=where
            source = NewProposalSourceForm(initial = {"source":proposal.get_source(lang[0])}, prefix="source_"+lang[0])
            source_dict[lang[0]]=source
            explanation = NewProposalExplanationForm(initial = {"explanation":proposal.get_explanation(lang[0])}, prefix="explanation_"+lang[0])
            explanation_dict[lang[0]]=explanation
            
        upload_formset = formset_factory(ModalUploadForm, extra=1)
        upload_initial = []
        for doc in proposal.get_documents_object():      
            upload_initial += [{"id":doc.id, "name":doc.doc}]        
        upload_form = upload_formset(initial=upload_initial, prefix='form')
    else:
        cost_form = None
        recipient_number_form =None
        area_form = None
        title_dict = None
        summary_dict = None
        necessity_dict = None
        recipient_dict = None
        where_dict = None
        source_dict = None
        explanation_dict = None
        upload_form = None
        
    comment_form = CommentForm() 
    comment_parent_form = CommentParentForm()
                  
        
    if request.POST:
        if "attached_documents_button" in request.POST:
            upload_formset = formset_factory(ModalUploadForm, extra=1)                 
            upload_form = upload_formset(request.POST,request.FILES, prefix='form')
            if upload_form.is_valid():
                db_edit_attached_documents_to_project(upload_form,proposal)
        if not request.user.is_anonymous() and "submit_comment" in request.POST: # make a comment
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                db_add_comment(comment_form, proposal, request.user.profile)
                comment_form = CommentForm()
        if not request.user.is_anonymous() and "submit_comment_parent" in request.POST: # make a comment
            comment_parent_form = CommentParentForm(request.POST)
            if comment_parent_form.is_valid():
                db_add_comment(comment_parent_form, proposal, request.user.profile)
                comment_parent_form = CommentParentForm()
    
    d = {"login_form":login_form, "search_form":search_form, "accepted_proposal":proposal, "related": related, "comments": comments,\
        "at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE,\
        "cost_form": cost_form, "recipient_number_form": recipient_number_form, "area_form": area_form,\
        "title_dict": title_dict, "summary_dict": summary_dict, "necessity_dict": necessity_dict,\
         "recipient_dict": recipient_dict, "where_dict": where_dict,\
         "source_dict": source_dict,"explanation_dict": explanation_dict, "upload_forms": upload_form, "comment_form": comment_form, "comment_parent_form": comment_parent_form}
    
    return render_to_response('accepted_proposal.html', d, context_instance = RequestContext(request))
    
'''@user_passes_test(lambda u: not u.is_anonymous() and u.profile.has_advanced_permissions(),login_url='/')    
def manage_accepted_proposal(request,proposal_id):
    """Render accepted proposal template
    """
    # Initializations
    login_form, search_form = base_forms_initialization(request)
    
    project=ProjectCard.objects.get(id=int(proposal_id))
    d = {"login_form":login_form, "search_form":search_form, "project":project}
    
    return render_to_response('manage_accepted_proposal.html', d, context_instance = RequestContext(request))'''
    
    
def search_results(request):
    """Render search results"""
    
    login_form, search_form = base_forms_initialization(request)
    # Language switch control:
    if 'lang' in request.GET:
        language_code=request.GET.get('lang')
    else:
        language_code=get_language()
  
    if request.POST: 
        # Do the search
        # TODO: HAU EGIN!!     
        result_list = search(search_form)
        if result_list is False:
            result_list = []
    else:
        result_list = []
    print "RESULTS2: ",result_list
    
    # Pagination:
    paginator = Paginator(result_list, 10)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    except Exception as error:
        results = result_list
    

    d = {"login_form":login_form, "search_form":search_form, "results":results, "result_list":result_list, "LANGUAGE_CODE":language_code}
    
    return render_to_response('search_results.html', d, context_instance = RequestContext(request))
    

@user_passes_test(lambda u: not u.is_anonymous() and u.profile.has_advanced_permissions(),login_url='/')
def add_event(request):
    """Renders add event template"""
       
    login_form, search_form = base_forms_initialization(request)
    
    if request.POST:
        if 'new_event_button' in request.POST:
            event_date_form = NewEventDateForm(request.POST)
            event_dict = {}
            # Generate forms for each language
            for lang in LANGUAGES:
                event = NewEventForm(request.POST, prefix="event_"+lang[0])
                event_dict[lang[0]]=event
            event_value = db_add_event(event_dict,\
                                    event_date_form)
            event_status = event_value[0]
            if event_status == 0: # validation error
                d = {"at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE, "login_form":login_form, "event_dict": event_dict, "event_date_form": event_date_form}
    
                return render_to_response('new_event.html', d, context_instance = RequestContext(request))
            
            elif event_status == 1: # save OK!
                event = event_value[1]           
                return redirect('/agenda/')
                
            elif event_status == 2: # error
                pass
                # TODO! Errore template bat!
            
            
    else:
        event_dict = {}
        for lang in LANGUAGES:
            event = NewEventForm(prefix="event_"+lang[0])
            event_dict[lang[0]]=event
        event_date_form = NewEventDateForm()
        
        
    d = {"at_language_priority": AT_LANGUAGE_PRIORITY, "opentrad_code": OPENTRAD_CODE, "login_form":login_form, "search_form":search_form, "event_dict": event_dict, "event_date_form": event_date_form}
    
    return render_to_response('add_event.html', d, context_instance = RequestContext(request))    
       
       
def agenda(request):
    """Renders agenda template"""
       
    login_form, search_form = base_forms_initialization(request)
    
    events = Event.objects.all().order_by('date')
        
        
    d = {"events": events, "login_form":login_form, "search_form":search_form}
    
    return render_to_response('agenda.html', d, context_instance = RequestContext(request))           
       
    
'''def bonbardeoa(request):
	import random
	from partaidetza.partaidetza_app.models import *
	text = open('efeCorpus94_95NoEtik.sgml').read().split('.')
	index = 0
	for i in range (1,10000): 
		print str(i)+'/10000'
		proposal = Proposal.objects.create_proposal(random.randint(0,100000),random.randint(0,100000),[random.randint(1,12)],Profile.objects.get(id=1))
		for lang in LANGUAGES:
			title_to_save = text[index]
			index+=1
			if title_to_save != '':
				ProposalTitle.objects.create_title(proposal,title_to_save,lang[0])
			summary_to_save = "".join(text[index:index+3])
			index+=3
			if summary_to_save != '':
				ProposalSummary.objects.create_summary(proposal,summary_to_save,lang[0])
			necessity_to_save = "".join(text[index:index+3])
			index+=3
			if necessity_to_save != '':
				ProposalNecessity.objects.create_necessity(proposal,necessity_to_save,lang[0])
			recipient_to_save = "".join(text[index:index+3])
			index+=3
			if recipient_to_save != '':
				ProposalRecipient.objects.create_recipient(proposal,recipient_to_save,lang[0])
			where_to_save = text[index]
			index+=1
			if where_to_save != '':
				ProposalWhere.objects.create_where(proposal,where_to_save,lang[0])
		proposal.save()'''
