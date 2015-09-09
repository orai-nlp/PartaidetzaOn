from django import forms
from partaidetza.partaidetza_app.models import Area, Genre, Profile, Proposal, ProposalArea, ProposalDocument, Specification, SpecificationArea, ProjectCard, ProjectArea, ProjectComment, Criterion, ProposalCriterion, Vote, PresentialVotes, Status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm \
        as ContribAuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re
from partaidetza.settings import LANGUAGES


##################
##  LOGIN FORM  ##
##################
class LoginForm(forms.Form):

    NAN = forms.CharField(
        label = _("NAN"),
        required = True,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("NAN")
                                })
    )
    
    password = forms.CharField(
        label = _("password"),
        required = True,
        widget = forms.PasswordInput(attrs={"type":"password",
                                            "class":"form-control",
                                            "placeholder":_("Password"),        
                                           })
    )
    
    def clean_NAN(self):
        NAN = self.cleaned_data.get('NAN')
        try:
            User.objects.get(username = NAN)
        except User.DoesNotExist:
            raise forms.ValidationError("The NAN you have entered does not exist.")
        return NAN
    
    def clean(self):
        username = self.cleaned_data.get('NAN')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct NAN and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        """
        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))
        """
        return self.cleaned_data
        
        

####################
##  PROFILE FORM  ##
####################

class ProfileForm(forms.Form):

    first_name = forms.CharField(
        label = _("Name"),
        required = True,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Name")
                                })
    )
    
    last_name = forms.CharField(
        label = _("Surname"),
        required = True,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Surname")
                                })
    )
    
    email = forms.EmailField(
        label = _("Surname"),
        required = True,
        widget=forms.EmailInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Email")
                                })
    )
    
    genre = forms.ChoiceField(
        label = _("Genre"),
        required = True,
        choices = map(lambda x: (x.id,x.genre),Genre.objects.all()),
        widget=forms.Select(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Genre")
                                })
    )

    birth_date = forms.DateField(
        label = _("Genre"),
        required = False,
        help_text = _("Example: 1954-03-21"),
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Birth date")
                                })
    )
    
    NAN = forms.CharField(
        label = _("NAN"),
        required = True,
        help_text = _("Example: 12345678J"),
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("NAN")
                                })
    )

    institution = forms.BooleanField(
        label = _("institution"),
        required = False,
        widget=forms.CheckboxInput(attrs={"type":"check", 
                                "placeholder":_("Institution")
                                })
    )
    
    
    institution_name = forms.CharField(
        label = _("Institution name"),
        required = False,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Institution name")
                                })
    )
    
    country = forms.CharField(
        label = _("Country"),
        required = False,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Country")
                                })
    )
    
    info = forms.CharField(
        label = _("Info"),
        required = False,
        widget=forms.CheckboxInput(attrs={"type":"check", 
                                "placeholder":_("Info")
                                })
    )
    
    def clean_NAN(self):
        NAN = self.cleaned_data.get('NAN')
        if re.search("[0-9]{8}[a-zA-Z]{1}",NAN) is None:
            raise forms.ValidationError(_("The NAN you have entered is not correct"))
        elif len(User.objects.filter(username=NAN))>1:
            raise forms.ValidationError(_("The NAN you have entered is registered."))
        else:
            return NAN
            
            
    
#####################
##  REGISTER FORM  ##
#####################
class RegisterForm(forms.Form):

    first_name = forms.CharField(
        label = _("Name"),
        required = True,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Name")
                                })
    )
    
    last_name = forms.CharField(
        label = _("Surname"),
        required = True,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Surname")
                                })
    )
    
    email = forms.EmailField(
        label = _("Surname"),
        required = True,
        widget=forms.EmailInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Email")
                                })
    )
    
    genre = forms.ChoiceField(
        label = _("Genre"),
        required = True,
        choices = map(lambda x: (x.id,x.genre),Genre.objects.all()),
        widget=forms.Select(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Genre")
                                })
    )

    birth_date = forms.DateField(
        label = _("Genre"),
        required = False,
        help_text = _("Example: 1954-03-21"),
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Birth date")
                                })
    )
    
    NAN = forms.CharField(
        label = _("NAN"),
        required = True,
        help_text = _("Example: 12345678J"),
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("NAN")
                                })
    )

    institution = forms.BooleanField(
        label = _("institution"),
        required = False,
        widget=forms.CheckboxInput(attrs={"type":"check", 
                                "placeholder":_("Institution")
                                })
    )
    
    
    institution_name = forms.CharField(
        label = _("Institution name"),
        required = False,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Institution name")
                                })
    )
    
    country = forms.CharField(
        label = _("Country"),
        required = False,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Country")
                                })
    )
    
    info = forms.CharField(
        label = _("Info"),
        required = False,
        widget=forms.CheckboxInput(attrs={"type":"check", 
                                "placeholder":_("Info")
                                })
    )
    
    
    password1 = forms.CharField(
        label = _("password1"),
        required = True,
        widget = forms.PasswordInput(attrs={"type":"password",
                                            "class":"form-control",
                                            "placeholder":_("Password1"),        
                                           })
    )
    
    password2 = forms.CharField(
        label = _("password2"),
        required = True,
        widget = forms.PasswordInput(attrs={"type":"password",
                                            "class":"form-control",
                                            "placeholder":_("Password2"),        
                                           })
    )


    def clean_NAN(self):
        NAN = self.cleaned_data.get('NAN')
        if re.search("[0-9]{8}[a-zA-Z]{1}",NAN) is None:
            raise forms.ValidationError(_("The NAN you have entered is not correct"))
        elif len(User.objects.filter(username=NAN))>0:
            raise forms.ValidationError(_("The NAN you have entered is registered."))
        else:
            return NAN
   
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return self.cleaned_data
    
#########################
##  NEW PROPOSAL FORM  ##
#########################
class NewProposalForm(forms.Form):

    area = forms.MultipleChoiceField(
        label = _("Area"),
        required = True,
        choices = map(lambda x: (x.id,x.area),Area.objects.all()),
        widget=forms.SelectMultiple(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Area")
                                })
    )

    recipient_number = forms.CharField(
            label = _("Recipient number"),
            required = True,
            widget=forms.TextInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Recipient number")
                                 })
    )

    cost = forms.CharField(
            label = _("Cost"),
            required = True,
            widget=forms.TextInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Cost")
                                 })
    )
    
    
    def clean_recipient_number(self):
        recipient_number = self.cleaned_data.get('recipient_number')
        if re.search("^[0-9]+?$",str(recipient_number)) is None:
            raise forms.ValidationError(_("This value must be a number"))        
        else:
            return recipient_number
            
    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if re.search("^[0-9]+?[\.\,]?[0-9]*?$",str(cost)) is None:
            raise forms.ValidationError(_("This value must be a number"))        
        else:
            return cost.replace(",",".")


class NewAcceptedProposalForm(NewProposalForm):
    
    proposal = forms.CharField(
            label = _("Proposal"),
            required = False,
            widget=forms.TextInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Proposal")
                                 })
    )

    
    state = forms.ChoiceField(
        label = _("State"),
        required = True,
        choices = map(lambda x: (x.id,x.status),Status.objects.all()),
        widget=forms.Select(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("State")
                                })
    )

    def clean_proposal(self):
        proposal_id = self.cleaned_data.get("proposal")
        if proposal_id != '':
            proposal = Proposal.objects.filter(id=int(proposal_id))
            if len(proposal) == 0:
                raise forms.ValidationError(_("There is no proposal with this ID"))    
            else:
                return proposal_id
        else:
            return proposal_id

class NewProposalTitleForm(forms.Form):

    title = forms.CharField(
            label = _("Title"),
            required = False,
            widget=forms.TextInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Title")
                                    })
    )
    

class NewProposalSummaryForm(forms.Form):

    summary = forms.CharField(
        label = _("Summary"),
        required = False,
        widget=forms.Textarea(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Summary")
                                })
    )


class NewProposalNecessityForm(forms.Form):
    
    necessity = forms.CharField(
            label = _("Necessity"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Necessity")
                                 })
    )

class NewProposalRecipientForm(forms.Form):
    
    recipient = forms.CharField(
            label = _("Recipient"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Recipient")
                                 })
    )

class NewProposalWhereForm(forms.Form):

    where = forms.CharField(
            label = _("Where"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Where")
                                 })
    )
    
class NewProposalSourceForm(forms.Form):

    source = forms.CharField(
            label = _("Source"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Source")
                                 })
    )
    
class NewProposalExplanationForm(forms.Form):

    explanation = forms.CharField(
            label = _("Explanation"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Explanation")
                                 })
    )


class CoordinatesForm(forms.Form):

    coordinates = forms.CharField(
            label = _("coodinates"),
            required = False,
            widget=forms.HiddenInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Coordinates")
                                 })
    )
    
    
    
class NewEventForm(forms.Form):

    event = forms.CharField(
            label = _("Event"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Event")
                                    })
    )    

class NewEventDateForm(forms.Form):
    
    date = forms.DateField(
        label = _("Date"),
        required = True,
        help_text = _("Example: 1954-03-21"),
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Date")
                                })
    )    
        
###################
##  UPLOAD FORM  ##
###################
class UploadForm(forms.Form):
    
    file=forms.FileField(
         required=False,
         widget=forms.FileInput(attrs={"class":"form-control",
                                    "type":"file"
                                  }))
                                  


    
    
###################
##  SEARCH FORM  ##
###################

class SearchBoxForm(forms.Form):
    search_query = forms.CharField(
            label = _("Query"),
            required = False,
            widget=forms.HiddenInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Query")
                                 })
    )
    search_type = forms.ChoiceField(
            label = _("Type"),
            required = False,
            choices = [('all',''),('proposal',_('proposal')),('project',_('project'))],
            widget=forms.Select(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Type")
                                    })
        )
    search_where = forms.ChoiceField(
            label = _("Where"),
            required = False,
            choices = [('all',''),('title',_('title')),('summary',_('summary')),('necessity',_('necessity')),('recipient',_('recipient')),('where',_('where'))],
            widget=forms.Select(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Where")
                                    })
        )
    search_area = forms.ChoiceField(
            label = _("Area"),
            required = False,
            choices = [('all','')]+map(lambda x: (x.id,x.area),Area.objects.all()),
            widget=forms.Select(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Area")
                                    })
        )
        
    search_lang = forms.ChoiceField(
            label = _("Language"),
            required = False,
            choices = [('all','')]+map(lambda x: (x[0],x[1]),LANGUAGES),
            widget=forms.Select(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Language")
                                    })
        )
        
        
###################
### MODAL FORMS ###
###################

class ModalAreaForm(forms.Form):
    
    area = forms.MultipleChoiceField(
        label = _("Area"),
        required = True,
        choices = map(lambda x: (x.id,x.area),Area.objects.all()),
        widget=forms.SelectMultiple(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Area"),
                                "id":"id_modal_area"
                                })
    )



class ModalCostForm(forms.Form):

    cost = forms.CharField(
            label = _("Cost"),
            required = True,
            widget=forms.TextInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Cost"),
                                    "id": "id_modal_cost"
                                 })
    )
    
    
    def clean_recipient_number(self):
        recipient_number = self.cleaned_data.get('recipient_number')
        if re.search("[0-9]+?",str(recipient_number)) is None:
            raise forms.ValidationError(_("This value must be a number"))        
        else:
            return recipient_number
            
    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if re.search("^[0-9]+?[\.\,]?[0-9]*?$",str(cost)) is None:
            raise forms.ValidationError(_("This value must be a number"))        
        else:
            return cost.replace(",",".")


class ModalRecipientNumberForm(forms.Form):

    recipient_number = forms.CharField(
            label = _("Recipient number"),
            required = True,
            widget=forms.TextInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Recipient number"),
                                    "id": "id_modal_recipient_number"
                                 })
    )

    
    
    def clean_recipient_number(self):
        recipient_number = self.cleaned_data.get('recipient_number')
        if re.search("[0-9]+?",str(recipient_number)) is None:
            raise forms.ValidationError(_("This value must be a number"))
        else:
            return recipient_number
            
            
class CriterionForm(forms.Form):
    
    criterion = forms.BooleanField(
        label = _("Criterion"),
        required = False,
        widget=forms.CheckboxInput(attrs={"type":"check", 
                                "placeholder":_("Criterion"),
                                "class": "criterion_checkbox_criterion"
                                })
    )
    
    changed = forms.BooleanField(
        label = _("Criterion"),
        required = False,
        widget=forms.HiddenInput(attrs={"type":"check", 
                                "placeholder":_("Changed"),
                                "class": "criterion_checkbox_changed"
                                })
    )
    
class ModalUploadForm(forms.Form):
    
    file=forms.FileField(
         required=False,
         widget=forms.FileInput(attrs={"class":"form-control",
                                    "type":"file"
                                  })
    ) 
    
    id=forms.CharField(
            label = _("id"),
            required = False,
            widget=forms.HiddenInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("id"),                                    
                                 })
    )
    
    name = forms.CharField(
            label = _("File"),
            required = False,
            widget=forms.TextInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("File"),
                                 })
    )
    
    
#####################
### COMMENT FORMS ###
#####################

class CommentForm(forms.Form):
    comment = forms.CharField(
            label = _("Comment"),
            required = True,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Comment"),
                                    "rows":"3",
                                 })
    )
    


class CommentParentForm(forms.Form):
    comment = forms.CharField(
            label = _("Comment"),
            required = True,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Comment"),
                                    "rows":"3",
                                 })
    )
    
    parent_id =forms.CharField(
            label = _("parent_id"),
            required = False,
            widget=forms.HiddenInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("parent_id"),                                    
                                 })
    )
