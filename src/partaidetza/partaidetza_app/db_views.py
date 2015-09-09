# This is where all the DB edit functions are gathered
from django.contrib.auth import authenticate
from partaidetza.partaidetza_app.models import Genre, Profile, Proposal, ProposalArea, ProposalDocument, Specification,\
 SpecificationArea, ProjectCard, ProjectArea, ProjectComment, Criterion, ProposalCriterion, Vote, PresentialVotes,\
 ProposalTitle, ProposalSummary, ProposalRecipient, ProposalNecessity, ProposalWhere, ProjectCardTitle,\
  ProjectCardSummary, ProjectCardRecipient, ProjectCardWhere, ProjectCardNecessity, ProjectCardSource,\
   ProjectCardExplanation, Proposal, ProposalCriterion, ProjectCardDocument, ProjectComment, Event, EventContent
   

from utils import *
from partaidetza.settings import LANGUAGES, OPENTRAD_CODE, AT_LANGUAGE_PRIORITY
import re
import time, datetime

def db_register(register_form):
    """Registers a user in the DB
    PARAMETERS:
    1. register_form
    RETURNS:
    (status_value,object)
    status_value -> 0: invalid form, 1: no errors, 2: other error
    object -> status_value==0: register_form, status_value==1: User object, status_value=2: error string
    """
    try:
        status_code = 1
        if register_form.is_valid():
            cd_register_form = register_form.cleaned_data
            profile = Profile.objects.create_profile(cd_register_form.get('first_name'),\
                                                cd_register_form.get('last_name'),\
                                                cd_register_form.get('genre'),\
                                                cd_register_form.get('birth_date'),\
                                                cd_register_form.get('NAN'),\
                                                cd_register_form.get('email'),\
                                                cd_register_form.get('institution'),\
                                                cd_register_form.get('institution_name'),\
                                                cd_register_form.get('country'),\
                                                cd_register_form.get('password1'),\
                                                cd_register_form.get('info'))      
            user = authenticate(username = cd_register_form.get('NAN'), password = cd_register_form.get('password1'))
            return (status_code,user) 
        else:
            status_code = 0
            return (status_code,register_form)
    except Exception as error:
        print error
        status_code = 2
        return (status_code,error)
        
        
def db_update_profile(profile_form):
    """Update a user in the DB
    PARAMETERS:
    1. profile_form
    RETURNS:
    (status_value,object)
    status_value -> 0: invalid form, 1: no errors, 2: other error
    object -> status_value==0: profile_form, status_value==1: Profile object, status_value=2: error string
    """
    try:
        status_code = 1
        if profile_form.is_valid():
            cd_profile_form = profile_form.cleaned_data
            profile = Profile.objects.update_profile(cd_profile_form.get('first_name'),\
                                                cd_profile_form.get('last_name'),\
                                                cd_profile_form.get('genre'),\
                                                cd_profile_form.get('birth_date'),\
                                                cd_profile_form.get('NAN'),\
                                                cd_profile_form.get('email'),\
                                                cd_profile_form.get('institution'),\
                                                cd_profile_form.get('institution_name'),\
                                                cd_profile_form.get('country'),\
                                                cd_profile_form.get('info'))                  
            return (status_code,profile) 
        else:
            status_code = 0
            return (status_code,profile_form)
    except Exception as error:
        print error
        status_code = 2
        return (status_code,error)        
        
     

def db_add_proposal(new_proposal_form, title_dict, summary_dict, necessity_dict, recipient_dict, where_dict, upload_form, coordinates_form, profile):
    """Insert a proposal in the DB
    PARAMETERS:
    1. profile_form
    2. title_dict
    3. summary_dict
    4. necessity_dict
    5. recipient_dict
    6. where_dict
    7. upload_form
    8. coordinates_form
    9. profile object
    RETURNS:
    (status_value,object)
    status_value -> 0: invalid form, 1: no errors, 2: other error
    object -> status_value==0: all_forms, status_value==1: Proposal object, status_value=2: error string
    """
    try:
        status_code = 1
        validated=validate_new_proposal_form(new_proposal_form,\
                                         title_dict,\
                                         summary_dict,\
                                         necessity_dict,\
                                         recipient_dict,\
                                         where_dict,\
                                         upload_form,\
                                         coordinates_form)
        if validated:
            # save proposal
            cd_new_proposal_form = new_proposal_form.cleaned_data
            proposal = Proposal.objects.create_proposal(cd_new_proposal_form.get('recipient_number'),\
                                                    cd_new_proposal_form.get('cost'),\
                                                    cd_new_proposal_form.get('area'),\
                                                    profile)
                                                    

            # save coordinates
            cd_coordinates_form = coordinates_form.cleaned_data
            coordinates = cd_coordinates_form.get("coordinates")
            coordinates = coordinates.split("|")
            for coordinate in coordinates:
                coords = re.search("\[(.*?),(.*?)\]",coordinate)
                if coords is not None:
                    proposal.set_map_point(float(coords.group(1)),float(coords.group(2)))
            
            # save documents
            # TODO: Denbora trazak kendu dena amaitzean
            import time
            start_time = time.time()
                      
            for doc_form in upload_form:
                cd_doc_form = doc_form.cleaned_data
                # Discar empty uploads
                if cd_doc_form.get('file') is not None:
                    # Add timestamp to filename!
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    filename =st + '_' + cd_doc_form.get('file').name
                    handle_uploaded_file(filename,cd_doc_form.get('file'))
                    ProposalDocument.objects.create_document(proposal,filename)
                    
            print("DOKUMENTUAK GORDE --- %s seconds ---" % (time.time() - start_time))   
               
            for lang in LANGUAGES:
                # save title
                start_time = time.time()
                cd_title = title_dict[lang[0]].cleaned_data
                title_to_save = cd_title.get('title')
                if title_to_save != '':
                    ProposalTitle.objects.create_title(proposal,title_to_save,lang[0],False)
                else:
                    title_to_save = get_best_translation_source(title_dict,lang[0])
                    ProposalTitle.objects.create_title(proposal,title_to_save,lang[0],True)
                print("TITLE GORDE --- %s seconds ---" % (time.time() - start_time)) 
                # save summary
                start_time = time.time()
                cd_summary = summary_dict[lang[0]].cleaned_data
                summary_to_save = cd_summary.get('summary')
                if summary_to_save != '':
                    ProposalSummary.objects.create_summary(proposal,summary_to_save,lang[0],False)
                else:
                    summary_to_save = get_best_translation_source(summary_dict,lang[0])
                    ProposalSummary.objects.create_summary(proposal,summary_to_save,lang[0],True)
                print("SUMMARY GORDE --- %s seconds ---" % (time.time() - start_time)) 
                # save necessity
                start_time = time.time()
                cd_necessity = necessity_dict[lang[0]].cleaned_data
                necessity_to_save = cd_necessity.get('necessity')
                if necessity_to_save != '':
                    ProposalNecessity.objects.create_necessity(proposal,necessity_to_save,lang[0],False)
                else:
                    necessity_to_save = get_best_translation_source(necessity_dict,lang[0])
                    ProposalNecessity.objects.create_necessity(proposal,necessity_to_save,lang[0],True)     
                print("NECESSITY GORDE --- %s seconds ---" % (time.time() - start_time))            
                # save recipient
                start_time = time.time()
                cd_recipient = recipient_dict[lang[0]].cleaned_data
                recipient_to_save = cd_recipient.get('recipient')
                if recipient_to_save != '':
                    ProposalRecipient.objects.create_recipient(proposal,recipient_to_save,lang[0],False)
                else:
                    recipient_to_save = get_best_translation_source(recipient_dict,lang[0])
                    ProposalRecipient.objects.create_recipient(proposal,recipient_to_save,lang[0],True)                
                print("RECIPIENT GORDE --- %s seconds ---" % (time.time() - start_time)) 
                # save where
                start_time = time.time()
                cd_where = where_dict[lang[0]].cleaned_data
                where_to_save = cd_where.get('where')
                if where_to_save != '':
                    ProposalWhere.objects.create_where(proposal,where_to_save,lang[0],False)
                else:
                    where_to_save = get_best_translation_source(where_dict,lang[0])
                    ProposalWhere.objects.create_where(proposal,where_to_save,lang[0],True)
                
                print("WHERE GORDE --- %s seconds ---" % (time.time() - start_time)) 
            # Save again to reindex in Solr
            proposal.save()
            return (status_code,proposal)
        else:
            status_code = 0
            return (status_code,\
                    new_proposal_form,\
                    title_dict,\
                    summary_dict,\
                    necessity_dict,\
                    recipient_dict,\
                    where_dict,\
                    upload_form)
        
    except Exception as error:
        print error
        status_code = 2
        return (status_code,error)     
        
        
def db_add_accepted_proposals(upload_form, profile):
    """Insert accepted proposal from a file in the DB
    PARAMETERS:
    1. upload_form
    RETURNS:
    (status_value,object)
    status_value -> 0: invalid form, 1: no errors, 2: other error
    object -> status_value==0: upload_form, status_value==1: None, status_value=2: error string
    """
    status_code = 1
    if upload_form.is_valid():
        cd = upload_form.cleaned_data
        if cd.get('file') is not None:
            # Add timestamp to filename!
            import time, datetime
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            filename =st + '_' + cd.get('file').name
            handle_uploaded_file(filename,cd.get('file'),type='xls')
            projects_info = extract_project_info_from_file(filename)  
            # TODO: projects_info[0]-ko status kodearen arabera erabakiak hartu: ERRORE templatea sortu?
            projects_status = projects_info[0]
            project_list =  projects_info[1]
            # for each accepted project
            # TODO: Beharrezko zutabe minimoak bete direla ziurtatzen duen balidazioa burutu: id, area, recipient_number, cost eta testu minimoak
            
            for each_project in project_list:
                original_proposal_id = int(each_project.get('id'))
                project = ProjectCard.objects.create_projectCard(each_project.get('recipient_number'),\
                                                    each_project.get('cost'),\
                                                    each_project.get('area').split(','),\
                                                    1,
                                                    original_proposal_id,\
                                                    profile)

                for lang in LANGUAGES:
                    # save title
                    # Search the language key
                    if "title_"+lang[0] in each_project.keys():
                        title_to_save = each_project.get("title_"+lang[0],False)
                    else: # The value doesn't exists -> it will be translated automatically later
                        title_to_save = ""
                    ProjectCardTitle.objects.create_title(project,title_to_save,lang[0],False)
                    
                    # save summary
                    # Search the language key
                    if "summary_"+lang[0] in each_project.keys():
                        summary_to_save = each_project.get("summary_"+lang[0])
                    else: # The value doesn't exists -> it will be translated automatically later
                        summary_to_save = ""
                    ProjectCardSummary.objects.create_summary(project,summary_to_save,lang[0],False)
                                        
                    # save recipient
                    # Search the language key
                    if "recipient_"+lang[0] in each_project.keys():
                        recipient_to_save = each_project.get("recipient_"+lang[0])
                    else: # The value doesn't exists -> it will be translated automatically later
                        recipient_to_save = ""
                    ProjectCardRecipient.objects.create_recipient(project,recipient_to_save,lang[0],False)
                    
                    # save necessity
                    # Search the language key
                    if "necessity_"+lang[0] in each_project.keys():
                        necessity_to_save = each_project.get("necessity_"+lang[0])
                    else: # The value doesn't exists -> it will be translated automatically later
                        necessity_to_save = ""
                    ProjectCardNecessity.objects.create_necessity(project,necessity_to_save,lang[0],False)
                    
                    # save where
                    # Search the language key
                    if "where_"+lang[0] in each_project.keys():
                        where_to_save = each_project.get("where_"+lang[0])
                    else: # The value doesn't exists -> it will be translated automatically later
                        where_to_save = ""
                    ProjectCardWhere.objects.create_where(project,where_to_save,lang[0],False)
                    
                    # save explanation
                    # Search the language key
                    if "explanation_"+lang[0] in each_project.keys():
                        explanation_to_save = each_project.get("explanation_"+lang[0])
                    else: # The value doesn't exists -> it will be translated automatically later
                        explanation_to_save = ""
                    ProjectCardExplanation.objects.create_explanation(project,explanation_to_save,lang[0],False)
                    
                    # save source
                    # Search the language key
                    if "source_"+lang[0] in each_project.keys():
                        source_to_save = each_project.get("source_"+lang[0])
                    else: # The value doesn't exists -> it will be translated automatically later
                        source_to_save = ""
                    ProjectCardSource.objects.create_source(project,source_to_save,lang[0],False)
                    
                #ProposalDocument.objects.create_document(proposal,filename) 
                # Save again to reindex in Solr
                project.save()   
    else:
        status_code = 0
        return (status_code,upload_form)
        
def db_add_accepted_proposal_manually(new_accepted_proposal_form, title_dict, summary_dict, necessity_dict, recipient_dict, where_dict, source_dict, explanation_dict, upload_form, coordinates_form, profile):
    """Insert a accepted proposal in the DB
    PARAMETERS:
    1. profile_form
    2. title_dict
    3. summary_dict
    4. necessity_dict
    5. recipient_dict
    6. where_dict
    7. source_dict
    8. explanation_dict
    9. upload_form
    10. coordinates form
    11. profile object
    RETURNS:
    (status_value,object)
    status_value -> 0: invalid form, 1: no errors, 2: other error
    object -> status_value==0: all_forms, status_value==1: Proposal object, status_value=2: error string
    """
    try:
        status_code = 1
        validated=validate_new_accepted_proposal_form(new_accepted_proposal_form,\
                                         title_dict,\
                                         summary_dict,\
                                         necessity_dict,\
                                         recipient_dict,\
                                         where_dict,\
                                         source_dict,\
                                         explanation_dict,\
                                         upload_form,\
                                         coordinates_form)
        if validated:
            # save proposal
            cd_new_accepted_proposal_form = new_accepted_proposal_form.cleaned_data
            accepted_proposal = ProjectCard.objects.create_projectCard(cd_new_accepted_proposal_form.get('recipient_number'),\
                                                    cd_new_accepted_proposal_form.get('cost'),\
                                                    cd_new_accepted_proposal_form.get('area'),\
                                                    cd_new_accepted_proposal_form.get('state'),\
                                                    cd_new_accepted_proposal_form.get('proposal'),
                                                    profile)
                                                    


            # save coordinates
            cd_coordinates_form = coordinates_form.cleaned_data
            coordinates = cd_coordinates_form.get("coordinates")
            coordinates = coordinates.split("|")
            for coordinate in coordinates:
                coords = re.search("\[(.*?),(.*?)\]",coordinate)
                if coords is not None:
                    accepted_proposal.set_map_point(float(coords.group(1)),float(coords.group(2)))
            
            # save documents
            # TODO: Denbora trazak kendu dena amaitzean
            import time
            start_time = time.time()
                      
            for doc_form in upload_form:
                cd_doc_form = doc_form.cleaned_data
                # Discar empty uploads
                if cd_doc_form.get('file') is not None:
                    # Add timestamp to filename!
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    filename =st + '_' + cd_doc_form.get('file').name
                    handle_uploaded_file(filename,cd_doc_form.get('file'))
                    ProjectCardDocument.objects.create_document(accepted_proposal,filename)
                    
            print("DOKUMENTUAK GORDE --- %s seconds ---" % (time.time() - start_time))   
               
            for lang in LANGUAGES:
                # save title
                start_time = time.time()
                cd_title = title_dict[lang[0]].cleaned_data
                title_to_save = cd_title.get('title')
                if title_to_save != '':
                    ProjectCardTitle.objects.create_title(accepted_proposal,title_to_save,lang[0],False)
                else:
                    title_to_save = get_best_translation_source(title_dict,lang[0])
                    ProjectCardTitle.objects.create_title(accepted_proposal,title_to_save,lang[0],True)
                print("TITLE GORDE --- %s seconds ---" % (time.time() - start_time)) 
                # save summary
                start_time = time.time()
                cd_summary = summary_dict[lang[0]].cleaned_data
                summary_to_save = cd_summary.get('summary')
                if summary_to_save != '':
                    ProjectCardSummary.objects.create_summary(accepted_proposal,summary_to_save,lang[0],False)
                else:
                    summary_to_save = get_best_translation_source(summary_dict,lang[0])
                    ProjectCardSummary.objects.create_summary(accepted_proposal,summary_to_save,lang[0],True)
                print("SUMMARY GORDE --- %s seconds ---" % (time.time() - start_time)) 
                # save necessity
                start_time = time.time()
                cd_necessity = necessity_dict[lang[0]].cleaned_data
                necessity_to_save = cd_necessity.get('necessity')
                if necessity_to_save != '':
                    ProjectCardNecessity.objects.create_necessity(accepted_proposal,necessity_to_save,lang[0],False)
                else:
                    necessity_to_save = get_best_translation_source(necessity_dict,lang[0])
                    ProjectCardNecessity.objects.create_necessity(accepted_proposal,necessity_to_save,lang[0],True)     
                print("NECESSITY GORDE --- %s seconds ---" % (time.time() - start_time))            
                # save recipient
                start_time = time.time()
                cd_recipient = recipient_dict[lang[0]].cleaned_data
                recipient_to_save = cd_recipient.get('recipient')
                if recipient_to_save != '':
                    ProjectCardRecipient.objects.create_recipient(accepted_proposal,recipient_to_save,lang[0],False)
                else:
                    recipient_to_save = get_best_translation_source(recipient_dict,lang[0])
                    ProjectCardRecipient.objects.create_recipient(accepted_proposal,recipient_to_save,lang[0],True)                
                print("RECIPIENT GORDE --- %s seconds ---" % (time.time() - start_time)) 
                # save where
                start_time = time.time()
                cd_where = where_dict[lang[0]].cleaned_data
                where_to_save = cd_where.get('where')
                if where_to_save != '':
                    ProjectCardWhere.objects.create_where(accepted_proposal,where_to_save,lang[0],False)
                else:
                    where_to_save = get_best_translation_source(where_dict,lang[0])
                    ProjectCardWhere.objects.create_where(accepted_proposal,where_to_save,lang[0],True)
                
                print("WHERE GORDE --- %s seconds ---" % (time.time() - start_time)) 
                
                # save source
                start_time = time.time()
                cd_source = source_dict[lang[0]].cleaned_data
                source_to_save = cd_source.get('source')
                if source_to_save != '':
                    ProjectCardSource.objects.create_source(accepted_proposal,source_to_save,lang[0],False)
                else:
                    source_to_save = get_best_translation_source(source_dict,lang[0])
                    ProjectCardSource.objects.create_source(accepted_proposal,source_to_save,lang[0],True)
                
                print("SOURCE GORDE --- %s seconds ---" % (time.time() - start_time)) 
                
                # save explanation
                start_time = time.time()
                cd_explanation = explanation_dict[lang[0]].cleaned_data
                explanation_to_save = cd_explanation.get('explanation')
                if explanation_to_save != '':
                    ProjectCardExplanation.objects.create_explanation(accepted_proposal,explanation_to_save,lang[0],False)
                else:
                    explanation_to_save = get_best_translation_source(explanation_dict,lang[0])
                    ProjectCardExplanation.objects.create_explanation(accepted_proposal,explanation_to_save,lang[0],True)
                
                print("EXPLANATION GORDE --- %s seconds ---" % (time.time() - start_time)) 
            # Save again to reindex in Solr
            accepted_proposal.save()
            return (status_code,accepted_proposal)
        else:
            status_code = 0
            return (status_code,\
                    new_accepted_proposal_form,\
                    title_dict,\
                    summary_dict,\
                    necessity_dict,\
                    recipient_dict,\
                    where_dict,\
                    upload_form)
        
    except Exception as error:
        print error
        status_code = 2
        return (status_code,error)             
        
def db_add_proposal_criterions(changed_proposal_criterions, criterion_list, request):
    """Update proposal criterions in the DB
    PARAMETERS:
    1. changed proposal criterions from request: the criterions that has been touched
    2. criterion list
    3. proposal list
    4. request
    """

    changed_proposals = map(lambda x: x.replace("changed","criterion"),changed_proposal_criterions)
    for changed_proposal in changed_proposals:
        match_object = re.search(r"criterion_(\d+)-(\d+)-criterion",changed_proposal)
        proposal_id = match_object.group(1)
        criterion_index = match_object.group(2)
        proposal = Proposal.objects.get(id=int(proposal_id))
        proposalcriterion = ProposalCriterion.objects.filter(proposal__id=int(proposal_id), criterion = criterion_list[int(criterion_index)])

        if changed_proposal in request.POST:
            # is checked
            if len(proposalcriterion)==0:
                # create criterion
                ProposalCriterion.objects.create_proposal_criterion(proposal,criterion_list[int(criterion_index)],True)
            else:
                ProposalCriterion.objects.edit_proposal_criterion(proposal,criterion_list[int(criterion_index)],True)
        else:
            # is not checked
            if len(proposalcriterion)==0:
                # create criterion
                ProposalCriterion.objects.create_proposal_criterion(proposal,criterion_list[int(criterion_index)],False)              
            else:
                ProposalCriterion.objects.edit_proposal_criterion(proposal,criterion_list[int(criterion_index)],False)
        


def db_edit_attached_documents_to_proposal(upload_forms,proposal):
    """Update attached documents in the DB
    PARAMETERS:
    1. upload_fors
    2. proposal
    """       
    old_docs = proposal.get_documents_object()
    new_documents = upload_forms.forms
    new_documents_to_add = []
    old_documents_untouched = []
    for new_document in new_documents:
        cd_doc = new_document.cleaned_data
        if cd_doc.get("id") == "": # New document
            if cd_doc.get("file") is not None:
                new_documents_to_add += [cd_doc.get("file")]
        else: # The document already exists
            old_documents_untouched += [int(cd_doc.get("id"))]
         
    # Delete old docs:
    for doc in old_docs:
        if doc.id not in old_documents_untouched:
            doc.delete()   
            
    # Add new docs:
    for doc in new_documents_to_add:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        filename =st + '_' + doc.name
        handle_uploaded_file(filename,doc)
        ProposalDocument.objects.create_document(proposal,filename)
        
    
def db_edit_attached_documents_to_project(upload_forms,project):
    """Update attached documents in the DB
    PARAMETERS:
    1. upload_forms
    2. project
    """       
    old_docs = project.get_documents_object()
    new_documents = upload_forms.forms
    new_documents_to_add = []
    old_documents_untouched = []
    for new_document in new_documents:
        cd_doc = new_document.cleaned_data
        if cd_doc.get("id") == "": # New document
            if cd_doc.get("file") is not None:
                new_documents_to_add += [cd_doc.get("file")]
        else: # The document already exists
            old_documents_untouched += [int(cd_doc.get("id"))]
         
    # Delete old docs:
    for doc in old_docs:
        if doc.id not in old_documents_untouched:
            doc.delete()   
            
    # Add new docs:
    for doc in new_documents_to_add:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        filename =st + '_' + doc.name
        handle_uploaded_file(filename,doc)
        ProjectCardDocument.objects.create_document(project,filename)        
            
         
def db_add_comment(comment_form, project, profile):
    """Update attached documents in the DB
    PARAMETERS:
    1. comment_form
    2. project
    3. profile
    """     

    cd = comment_form.cleaned_data
    parent = cd.get("parent_id", None)  
    if parent:
        parent = ProjectComment.objects.get(id=int(parent))
    
    ProjectComment.objects.create_comment(cd.get("comment"),project,profile, parent)
    
    
def db_add_event(event_dict, event_date_form):
    """Update events in the DB
    PARAMETERS:
    1. event forms
    2. event date form
    """     
    try:
        status_code = 1
        validated=validate_new_event_form(event_dict,\
                                        event_date_form)
        if validated:
            cd_event_date_form = event_date_form.cleaned_data
            event = Event.objects.create_event(cd_event_date_form.get("date"))
            for lang in LANGUAGES:
                # save event
                start_time = time.time()
                cd_event = event_dict[lang[0]].cleaned_data
                event_to_save = cd_event.get('event')
                if event_to_save != '':
                    EventContent.objects.create_event(event,event_to_save,lang[0],False)
                else:
                    event_to_save = get_best_translation_source(event_dict,lang[0])
                    EventContent.objects.create_event(event,event_to_save,lang[0],True)
            return (status_code,event)
        else:
            status_code = 0
            return (status_code,\
                    new_event_form,\
                    event_dict)
    except Exception as error:
        print error
        status_code = 2
        return (status_code,error)             
        
