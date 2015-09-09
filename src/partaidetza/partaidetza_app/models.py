from django.db import models
from django.utils.translation import ugettext as _,get_language
from django.contrib.auth.models import User, Group
from settings import MEDIA_ROOT, ACCEPTED_IMAGE_FORMATS, MEDIA_URL, MAX_VOTES_PER_USER, MAX_FONDS_PER_USER, AT_ICON
import magic
from models_utils import translate_text_opentrad
    

# Create your models here.


class Genre(models.Model):
    genre= models.CharField(max_length=6)    
    
class Area(models.Model):
    area=models.CharField(max_length=100)

class ProfileManager(models.Manager):
    
    def create_profile(self,\
                    name,\
                    surname,\
                    genre,\
                    birth_date,\
                    NAN,\
                    email,\
                    institution,\
                    institution_name,\
                    country,\
                    password,\
                    info):
        """Creates a new profile"""      
        profile = Profile()        
        profile.genre = Genre.objects.get(id=int(genre))
        profile.birth_date = birth_date
        profile.NAN = NAN
        profile.institution = institution
        profile.institution_name = institution_name
        profile.country = country
        profile.info = info
        # Create a user object  
        user = User.objects.create_user(first_name = name,last_name = surname, username = NAN, email = email, password = password)
        group = Group.objects.get(name='citizen') 
        group.user_set.add(user)
        profile.user = user
        profile.save()
        return profile
        
    def update_profile(self,\
                    name,\
                    surname,\
                    genre,\
                    birth_date,\
                    NAN,\
                    email,\
                    institution,\
                    institution_name,\
                    country,\
                    info):
        """Update profile"""      
        profile = Profile.objects.get(user__username=NAN)        
        profile.genre = Genre.objects.get(id=int(genre))
        profile.birth_date = birth_date
        profile.NAN = NAN
        profile.institution = institution
        profile.institution_name = institution_name
        profile.country = country
        profile.info = info
        profile.user.first_name = name
        profile.user.last_name = surname
        profile.user.username = NAN
        profile.user.email = email  
        profile.user.save()
        profile.save()
        return profile

class Profile(models.Model):
    user = models.OneToOneField(User)
    genre = models.ForeignKey(Genre,null=True)
    birth_date = models.DateField(null=True)
    NAN = models.CharField(max_length=9)
    institution = models.NullBooleanField()
    institution_name = models.CharField(max_length=100,null=True)
    country = models.CharField(max_length=100,null=True)
    info = models.NullBooleanField()
    
    
    objects = ProfileManager()
    
    def is_admin(self):
        group = Group.objects.get(name="admin")
        return True if group in self.user.groups.all() else False
        
    def is_technician(self):
        group = Group.objects.get(name="technician")
        return True if group in self.user.groups.all() else False
        
    def is_manager(self):
        group = Group.objects.get(name="manager")
        return True if group in self.user.groups.all() else False
        
    def is_citizen(self):
        group = Group.objects.get(name="citizen")
        return True if group in self.user.groups.all() else False
        
    def has_advanced_permissions(self):
        return self.is_admin() or self.is_manager()
    
    
class ProposalManager(models.Manager):

   def create_proposal(self,\
                    recipient_number,\
                    cost,\
                    areas,\
                    profile):

       proposal = Proposal()
       proposal.recipient_number = int(recipient_number)
       proposal.cost = float(cost)       
       proposal.author = profile
       proposal.save()
       for each_area in areas:
        area = ProposalArea()
        area.area = Area.objects.get(id = int(each_area))
        area.proposal = proposal
        area.save()

       for criterion in Criterion.objects.all():
        ProposalCriterion.objects.create_proposal_criterion(proposal, criterion, False)
       return proposal
       
          
    
class Proposal(models.Model):
    # TODO: hauek Solr-en?
    #title = models.CharField(max_length=300)
    #summary = models.TextField()
    #necessity = models.TextField(null=True)
    #recipient = models.TextField(null=True)
    recipient_number = models.IntegerField(null = True)
    #where = models.TextField(null=True)
    cost = models.FloatField(null = True)
    date = models.DateField(auto_now = True, null = True)
    author = models.ForeignKey(Profile)
    
    objects = ProposalManager()

    # get title
    def get_title(self,\
                lang):
        try:
            title = ProposalTitle.objects.get(proposal = self, language = lang)                 
            if title.auto:
                return "<img src='"+AT_ICON+"'> "+title.title
            else:
                return title.title
        except Exception as error:
            return ""
        
    # get summary
    def get_summary(self,\
                lang):
        try:
            summary = ProposalSummary.objects.get(proposal = self, language = lang)        
            if summary.auto:
                return "<img src='"+AT_ICON+"'> "+summary.summary
            else:
                return summary.summary
        except Exception as error:
            return ""
        
    # get necessity
    def get_necessity(self,\
                lang):
        try:
            necessity = ProposalNecessity.objects.get(proposal = self, language = lang)        
            if necessity.auto:
                return "<img src='"+AT_ICON+"'> "+necessity.necessity
            else:
                return necessity.necessity
        except Exception as error:
            return ""
        
    # get recipient
    def get_recipient(self,\
                lang):
        try:
            recipient = ProposalRecipient.objects.get(proposal = self, language = lang)        
            if recipient.auto:
                return "<img src='"+AT_ICON+"'> "+recipient.recipient
            else:
                return recipient.recipient
        except Exception as error:
            return ""
        
    
    # get where
    def get_where(self,\
                lang):
        try:
            where = ProposalWhere.objects.get(proposal = self, language=lang)        
            if where.auto:
                return "<img src='"+AT_ICON+"'> "+where.where
            else:
                return where.where
        except Exception as error:
            return ""
        
    # get areas
    def get_area(self):
        return map(lambda x: x.area.id, self.proposalarea_set.all())
        
    def get_area_names(self):
        return map(lambda x: _(x.area.area), self.proposalarea_set.all())
        
    # get documents
    def get_documents_object(self):
        return self.proposaldocument_set.all()
    
    def get_documents(self):
        return map(lambda x: x.doc.name,self.proposaldocument_set.all())
        
    # get images
    def get_images(self):
        accepted_images = []
        all_documents = self.get_documents()
        for each_doc in all_documents:
            extension = magic.from_file(MEDIA_ROOT+'/'+each_doc, mime=True).split('/')[1]
            if extension in ACCEPTED_IMAGE_FORMATS:
                accepted_images += [MEDIA_URL+each_doc] 
        if len(accepted_images) == 0:
            accepted_images += [MEDIA_URL+'../img/no_photo.jpg']
        return accepted_images
        
    # get criterion
    def get_criterion(self,\
                    criterion):
        try:
            return ProposalCriterion.objects.get(proposal=self,criterion=criterion).value
        except Exception as error:
            return False
        
    # get criterion stats
    def get_criterion_stats(self):
        criterions = filter(lambda x: x.value,ProposalCriterion.objects.filter(proposal = self))
        all_criterions = Criterion.objects.all()    
        return str(len(criterions))+"/"+str(len(all_criterions))
        
    # get fonds
    def get_fonds(self):
        fonds = Fond.objects.filter(proposal = self)
        fonds_count = len(fonds)
        
        return fonds_count
        
    # already fonded: returns true if the user has already fond the project
    def already_fonded(self,\
                     user):
        return len(Fond.objects.filter(proposal = self, author = user.profile))>0
        
    # fond
    def fond(self,\
            user):
        try:
            # user fond number
            user_fonds = Fond.objects.filter(author = user.profile)
            proposal_user_fonds = user_fonds.filter(proposal = self)
            # check user's max fonds and user's fonds in the project
            if len(user_fonds) < MAX_FONDS_PER_USER and len(proposal_user_fonds) == 0:
                fond = Fond()
                fond.proposal = self
                fond.author = user.profile
                fond.save()
                return True
            else:
                return False
        except Exception as error:
            print error
            return False    
        
    # is accepted
    def is_accepted(self):
        """Looks if proposal has been accepted"""
        return len(ProjectCard.objects.filter(proposal=self))>0
        
    # is author
    def is_author(self,\
                user):
        print user.profile.id, self.author.id
        return self.author == user.profile
    
    # set area
    def set_area(self,\
                areas):
        try:
            proposal_areas = ProposalArea.objects.filter(proposal = self)
            map(lambda x: x.delete(),proposal_areas)
            for area in areas:
                new_area = ProposalArea()
                new_area.proposal = self
                new_area.area = Area.objects.get(id=int(area))
                new_area.save()
            return True
        except Exception as error:
            print error
            return False
        
    # set title
    def set_title(self,\
                title,\
                language):
        try:
            proposal_title = ProposalTitle.objects.get(proposal=self,language=language)
            proposal_title.title = title
            proposal_title.save()
            return True
        except Exception as error:
            print error
            return False
            
    # set summary
    def set_summary(self,\
                summary,\
                language):
        try:
            proposal_summary = ProposalSummary.objects.get(proposal=self,language=language)
            proposal_summary.summary = summary
            proposal_summary.save()
            return True
        except Exception as error:
            print error
            return False
                    
    # set recipient
    def set_recipient(self,\
                recipient,\
                language):
        try:
            proposal_recipient = ProposalRecipient.objects.get(proposal=self,language=language)
            proposal_recipient.recipient = recipient
            proposal_recipient.save()
            return True
        except Exception as error:
            print error
            return False   
            
    # set necessity
    def set_necessity(self,\
                necessity,\
                language):
        try:
            proposal_necessity = ProposalNecessity.objects.get(proposal=self,language=language)
            proposal_necessity.necessity = necessity
            proposal_necessity.save()
            return True
        except Exception as error:
            print error
            return False        
            
    # set where
    def set_where(self,\
                where,\
                language):
        try:
            proposal_where = ProposalWhere.objects.get(proposal=self,language=language)
            proposal_where.where = where
            proposal_where.save()
            return True
        except Exception as error:
            print error
            return False
     
            
    # set cost
    def set_cost(self,\
                new_cost):
        try:
            self.cost = float(new_cost)
            self.save()
            return True
        except Exception as error:
            return False
    
    # set recipient number        
    def set_recipient_number(self,\
                            new_recipient_number):
        try:
            self.recipient_number = int(new_recipient_number)
            self.save()
            return True
        except Exception as error:
            return False
            
    def set_map_point(self,\
                     x,\
                     y):
        ProposalMapPoint.objects.create_point(self,round(x,10),round(y,10))
       
     
    def get_map_point(self,\
                     x,\
                     y):
        point = ProposalMapPoint.objects.filter(proposal = self, x=round(x,10), y=round(y,10))
        if len(point)==1:
            return point[0]
        else:
            return None
            
    def get_map_points(self):
        return ProposalMapPoint.objects.filter(proposal = self)
        
    
    def delete_map_point(self,\
                     x,\
                     y):
        point = ProposalMapPoint.objects.filter(proposal = self, x=round(x,10), y=round(y,10))
        if len(point)==1:
            point.delete()
        else:
            pass
            
    def delete_proposal(self):
        # delete titles
        map(lambda x: x.delete(),ProposalTitle.objects.filter(proposal = self))
        # delete summaries
        map(lambda x: x.delete(),ProposalSummary.objects.filter(proposal = self))
        # delete recipients
        map(lambda x: x.delete(),ProposalRecipient.objects.filter(proposal = self))
        # delete necessities
        map(lambda x: x.delete(),ProposalNecessity.objects.filter(proposal = self))
        # delete wheres
        map(lambda x: x.delete(),ProposalWhere.objects.filter(proposal = self))
        # delete areas
        map(lambda x: x.delete(),ProposalArea.objects.filter(proposal = self))
        # delete map points
        map(lambda x: x.delete(),ProposalMapPoint.objects.filter(proposal = self))
        # delete document
        map(lambda x: x.delete(),ProposalDocument.objects.filter(proposal = self))
        # delete criterios
        map(lambda x: x.delete(),ProposalCriterionDocument.objects.filter(proposal = self))
        # delete fonds
        map(lambda x: x.delete(),Fond.objects.filter(proposal = self))
        # delete proposal
        self.delete()
 
class ProposalMapPointManager(models.Manager):
    
    def create_point(self,\
                    proposal,\
                    x,\
                    y):
       proposal_map_point = ProposalMapPoint()
       proposal_map_point.proposal = proposal
       proposal_map_point.x = x
       proposal_map_point.y = y
       proposal_map_point.save()
       
 
class ProposalMapPoint(models.Model):
    proposal = models.ForeignKey(Proposal)
    x = models.FloatField()
    y = models.FloatField()
    
    objects = ProposalMapPointManager()
    
class ProposalTitleManager(models.Manager):

    def create_title(self,\
                    proposal,\
                    title,\
                    language,\
                    auto):
        proposal_title = ProposalTitle()
        proposal_title.proposal = proposal
        '''if title.strip() == '':
            title = translate_text_opentrad(title,language)'''
        proposal_title.title = title
        proposal_title.language = language
        proposal_title.auto = auto
        proposal_title.save()
        return proposal_title
        
    
class ProposalTitle(models.Model):
    title = models.CharField(max_length=300)
    language = models.CharField(max_length=2)
    proposal = models.ForeignKey(Proposal)
    auto = models.BooleanField(default=False)
    
    objects = ProposalTitleManager()
    

class ProposalSummaryManager(models.Manager):

    def create_summary(self,\
                    proposal,\
                    summary,\
                    language,\
                    auto):
        proposal_summary = ProposalSummary()
        proposal_summary.proposal = proposal
        proposal_summary.summary = summary
        proposal_summary.language = language        
        proposal_summary.auto = auto
        proposal_summary.save()
        return proposal_summary    
    
class ProposalSummary(models.Model):
    summary = models.TextField()
    language = models.CharField(max_length=2)
    proposal = models.ForeignKey(Proposal)
    auto = models.BooleanField(default=False)
    
    objects = ProposalSummaryManager()
    
class ProposalNecessityManager(models.Manager):

    def create_necessity(self,\
                    proposal,\
                    necessity,\
                    language,\
                    auto):
        proposal_necessity = ProposalNecessity()
        proposal_necessity.proposal = proposal
        proposal_necessity.necessity = necessity
        proposal_necessity.language = language
        proposal_necessity.auto = auto
        proposal_necessity.save()
        return proposal_necessity    
    
class ProposalNecessity(models.Model):
    necessity = models.TextField()
    language = models.CharField(max_length=2)
    proposal = models.ForeignKey(Proposal)
    auto = models.BooleanField(default=False)
    
    objects = ProposalNecessityManager()
    
class ProposalRecipientManager(models.Manager):

    def create_recipient(self,\
                    proposal,\
                    recipient,\
                    language,\
                    auto):
        proposal_recipient = ProposalRecipient()
        proposal_recipient.proposal = proposal
        proposal_recipient.recipient = recipient
        proposal_recipient.language = language
        proposal_recipient.auto = auto
        proposal_recipient.save()
        return proposal_recipient        
    
class ProposalRecipient(models.Model):
    recipient = models.TextField()
    language = models.CharField(max_length=2)
    proposal = models.ForeignKey(Proposal)
    auto = models.BooleanField(default=False)
    
    objects = ProposalRecipientManager()
    
class ProposalWhereManager(models.Manager):

    def create_where(self,\
                    proposal,\
                    where,\
                    language,\
                    auto):
        proposal_where = ProposalWhere()
        proposal_where.proposal = proposal
        proposal_where.where = where
        proposal_where.language = language
        proposal_where.auto = auto
        proposal_where.save()
        return proposal_where        
    
class ProposalWhere(models.Model):
    where = models.TextField()
    language = models.CharField(max_length=2)
    proposal = models.ForeignKey(Proposal)
    auto = models.BooleanField(default=False)
    
    objects = ProposalWhereManager()
    
    
class ProposalAreaManager(models.Manager):

    def get_proposals_by_area(self,\
                            area):
        try:
            proposal_list = ProposalArea.objects.filter(area=area)
            if len(proposal_list)>0:
                return map(lambda x: x.proposal, proposal_list)
            else:
                return []
        except Exception as error:
            
            return []
    
class ProposalArea(models.Model):
    area = models.ForeignKey(Area)
    proposal = models.ForeignKey(Proposal)
    
    objects = ProposalAreaManager()
    
class ProposalDocumentManager(models.Manager):

    def create_document(self,\
                    proposal,\
                    filename):
        
        proposal_document = ProposalDocument()
        proposal_document.proposal = proposal
        proposal_document.doc = filename
        proposal_document.save()
        return proposal_document            
    
class ProposalDocument(models.Model):
    proposal = models.ForeignKey(Proposal)
    doc = models.FileField(upload_to=MEDIA_ROOT)
    
    objects = ProposalDocumentManager()
    
    
class Status(models.Model):
    status = models.CharField(max_length=100)
    
    
class ProjectCardManager(models.Manager):

   def create_projectCard(self,\
                    recipient_number,\
                    cost,\
                    areas,\
                    status,\
                    proposal_id,\
                    profile):

        if proposal_id == '': # create a proposal object
            proposal = Proposal.objects.create_proposal(recipient_number,cost,areas,profile)
        else:       
            proposal = Proposal.objects.get(id=proposal_id)    
        project = ProjectCard()
        project.proposal = proposal
        project.recipient_number = int(recipient_number)
        project.cost = float(cost) 
        # TODO: Hau zuzendu status egokia aukeratzeko      
        project.status = Status.objects.get(id=status)
        project.save()
        for each_area in areas:
            area = ProjectArea()
            area.area = Area.objects.get(id = int(each_area))
            area.project = project
            area.save()
        
        return project    
    
class ProjectCard(models.Model):
    proposal = models.ForeignKey(Proposal)
    #explanation = models.TextField()
    #recipient = models.TextField()
    recipient_number = models.IntegerField()
    #where = models.TextField()
    cost = models.FloatField()
    #source = models.TextField()
    status = models.ForeignKey(Status)
    date = models.DateField(auto_now = True, null = True)
    
    objects = ProjectCardManager()
    
    # get title
    def get_title(self,\
                lang):
        try:
            title = ProjectCardTitle.objects.get(projectCard = self, language = lang)        
            if title.auto:
                return "<img src='"+AT_ICON+"'> "+title.title
            else:
                return title.title
        except Exception as error:
            return ""
        
    # get summary
    def get_summary(self,\
                lang):
        try:
            summary = ProjectCardSummary.objects.get(projectCard = self, language = lang)        
            if summary.auto:
                return "<img src='"+AT_ICON+"'> "+summary.summary
            else:
                return summary.summary
        except Exception as error:
            return ""
        
    # get necessity
    def get_necessity(self,\
                lang):
        try:
            necessity = ProjectCardNecessity.objects.get(projectCard = self, language = lang)        
            if necessity.auto:
                return "<img src='"+AT_ICON+"'> "+necessity.necessity
            else:
                return necessity.necessity
        except Exception as error:
            return ""
        
    # get recipient
    def get_recipient(self,\
                lang):
        try:
            recipient = ProjectCardRecipient.objects.get(projectCard = self, language = lang)        
            if recipient.auto:
                return "<img src='"+AT_ICON+"'> "+recipient.recipient
            else:
                return recipient.recipient
        except Exception as error:
            return ""
            
    # get where
    def get_where(self,\
                lang):
        try:
            where = ProjectCardWhere.objects.get(projectCard = self, language = lang)        
            if where.auto:
                return "<img src='"+AT_ICON+"'> "+title.title
            else:
                return where.where
        except Exception as error:
            return ""
        
    # get explanation
    def get_explanation(self,\
                lang):
        try:
            explanation = ProjectCardExplanation.objects.get(projectCard = self, language = lang)        
            if explanation.auto:
                return "<img src='"+AT_ICON+"'> "+explanation.explanation
            else:
                return explanation.explanation
        except Exception as error:
            return ""
        
    # get source
    def get_source(self,\
                lang):
        try:
            source = ProjectCardSource.objects.get(projectCard = self, language = lang)        
            if source.auto:
                return "<img src='"+AT_ICON+"'> "+source.source
            else:
                return source.source
        except Exception as error:
            return ""
        
    # get areas
    def get_area(self):
        return map(lambda x: x.area.id, self.projectarea_set.all())
        
    def get_area_names(self):
        return map(lambda x: _(x.area.area), self.projectarea_set.all())            
        
    # get documents
    def get_documents_object(self):
        return self.projectcarddocument_set.all()
    
    def get_documents(self):
        return map(lambda x: x.doc.name,self.projectcarddocument_set.all())
        
    # get images
    def get_images(self):
        accepted_images = []
        all_documents = self.get_documents()
        for each_doc in all_documents:
            extension = magic.from_file(MEDIA_ROOT+'/'+each_doc, mime=True).split('/')[1]
            if extension in ACCEPTED_IMAGE_FORMATS:
                accepted_images += [MEDIA_URL+each_doc] 
        if len(accepted_images) == 0:
            accepted_images += [MEDIA_URL+'../img/no_photo.jpg']
        return accepted_images
        
    # get comments
    def get_comments(self):
        return ProjectComment.objects.filter(project=self,parent_comment=None).order_by('-id')
        
    def get_all_comments(self):
        return ProjectComment.objects.filter(project=self).order_by('-id')
        
    # get votes
    def get_votes(self):
        votes = Vote.objects.filter(project = self)
        votes_count = len(votes)
        presential_votes = PresentialVotes.objects.filter(project = self)
        if len(presential_votes) == 0:
            presential_votes_count = 0
        else:
            presential_votes_count = reduce(lambda x,y: x+y, map(lambda x: x.number ,presential_votes))
        return votes_count + presential_votes_count
        
    # already voted: returns true if the user has already vote the project
    def already_voted(self,\
                     user):
        return len(Vote.objects.filter(project = self, elector = user.profile))>0
        
    # vote
    def vote(self,\
            user):
        try:
            # user vote number
            user_votes = Vote.objects.filter(elector = user.profile)
            project_user_votes = user_votes.filter(project = self)
            # check user's max votes and user's votes in the project
            if len(user_votes) < MAX_VOTES_PER_USER and len(project_user_votes) == 0:
                vote = Vote()
                vote.project = self
                vote.elector = user.profile
                vote.save()
                return True
            else:
                return False
        except Exception as error:
            print error
            return False
                
    
    # set area
    def set_area(self,\
                areas):
        try:
            project_areas = ProjectArea.objects.filter(project = self)
            map(lambda x: x.delete(),project_areas)
            for area in areas:
                new_area = ProjectArea()
                new_area.project = self
                new_area.area = Area.objects.get(id=int(area))
                new_area.save()
            return True
        except Exception as error:
            print error
            return False
    
    # set title
    def set_title(self,\
                title,\
                language):
        try:
            project_title = ProjectCardTitle.objects.get(projectCard=self,language=language)
            project_title.title = title
            project_title.save()
            return True
        except Exception as error:
            print error
            return False
            
    # set summary
    def set_summary(self,\
                summary,\
                language):
        try:
            project_summary = ProjectCardSummary.objects.get(projectCard=self,language=language)
            project_summary.summary = summary
            project_summary.save()
            return True
        except Exception as error:
            print error
            return False
                    
    # set recipient
    def set_recipient(self,\
                recipient,\
                language):
        try:
            project_recipient = ProjectCardRecipient.objects.get(projectCard=self,language=language)
            project_recipient.recipient = recipient
            project_recipient.save()
            return True
        except Exception as error:
            print error
            return False   
            
    # set necessity
    def set_necessity(self,\
                necessity,\
                language):
        try:
            project_necessity = ProjectCardNecessity.objects.get(projectCard=self,language=language)
            project_necessity.necessity = necessity
            project_necessity.save()
            return True
        except Exception as error:
            print error
            return False        
            
    # set where
    def set_where(self,\
                where,\
                language):
        try:
            project_where = ProjectCardWhere.objects.get(projectCard=self,language=language)
            project_where.where = where
            project_where.save()
            return True
        except Exception as error:
            print error
            return False
            
    # set source
    def set_source(self,\
                source,\
                language):
        try:
            project_source = ProjectCardSource.objects.get(projectCard=self,language=language)
            project_source.source = source
            project_source.save()
            return True
        except Exception as error:
            print error
            return False
     
    # set explanation
    def set_explanation(self,\
                explanation,\
                language):
        try:            
            project_explanation = ProjectCardExplanation.objects.get(projectCard=self,language=language)
            project_explanation.explanation = explanation
            project_explanation.save()
            return True
        except Exception as error:
            print error
            return False
           
    # set cost
    def set_cost(self,\
                new_cost):
        try:
            self.cost = float(new_cost)
            self.save()
            return True
        except Exception as error:
            return False
    
    # set recipient number        
    def set_recipient_number(self,\
                            new_recipient_number):
        try:
            self.recipient_number = int(new_recipient_number)
            self.save()
            return True
        except Exception as error:
            return False
 

    def set_map_point(self,\
                     x,\
                     y):
        ProjectCardMapPoint.objects.create_point(self,round(x,10),round(y,10))
       
     
    def get_map_point(self,\
                     x,\
                     y):
        point = ProjectCardMapPoint.objects.filter(project = self, x=round(x,10), y=round(y,10))
        if len(point)==1:
            return point[0]
        else:
            return None
            
    def get_map_points(self):
        return ProjectCardMapPoint.objects.filter(project = self)
        
    
    def delete_map_point(self,\
                     x,\
                     y):
        point = ProjectCardMapPoint.objects.filter(project = self, x=round(x,10), y=round(y,10))
        if len(point)==1:
            point.delete()
        else:
            pass
 
    def delete_project(self):
        # delete titles
        map(lambda x: x.delete(),ProjectsCardTitle.objects.filter(project = self))
        # delete summaries
        map(lambda x: x.delete(),ProjectsCardSummary.objects.filter(project = self))
        # delete recipients
        map(lambda x: x.delete(),ProjectsCardRecipient.objects.filter(project = self))
        # delete necessities
        map(lambda x: x.delete(),ProjectsCardNecessity.objects.filter(project = self))
        # delete wheres
        map(lambda x: x.delete(),ProjectsCardWhere.objects.filter(project = self))
        # delete areas
        map(lambda x: x.delete(),ProjectsCardArea.objects.filter(project = self))
        # delete map points
        map(lambda x: x.delete(),ProjectsCardMapPoint.objects.filter(project = self))
        # delete document
        map(lambda x: x.delete(),ProjectsCardDocument.objects.filter(project = self))
        # delete votes
        map(lambda x: x.delete(),Vote.objects.filter(project = self))
        map(lambda x: x.delete(),PresentialVotes.objects.filter(project = self))
        # delete comments
        map(lambda x: x.delete(),ProjectComment.objects.filter(project = self))
        # delete project
        self.delete()
 
class ProjectCardMapPointManager(models.Manager):
    
    def create_point(self,\
                    project,\
                    x,\
                    y):
       project_map_point = ProjectCardMapPoint()
       project_map_point.project = project
       project_map_point.x = x
       project_map_point.y = y
       project_map_point.save()


class ProjectCardMapPoint(models.Model):
    project = models.ForeignKey(ProjectCard)
    x = models.FloatField()
    y = models.FloatField() 
    
    objects = ProjectCardMapPointManager()
 
    
class ProjectCardSourceManager(models.Manager):

    def create_source(self,\
                    project,\
                    source,\
                    language,\
                    auto):
        project_source = ProjectCardSource()
        project_source.projectCard = project
        project_source.source = source
        project_source.language = language
        project_source.auto = auto
        project_source.save()
        return project_source     
    
    
class ProjectCardSource(models.Model):
    source = models.TextField()
    language = models.CharField(max_length=2)
    projectCard = models.ForeignKey(ProjectCard)   
    auto = models.BooleanField(default=False)
    
    objects = ProjectCardSourceManager()
    
class ProjectCardExplanationManager(models.Manager):

    def create_explanation(self,\
                    project,\
                    explanation,\
                    language,\
                    auto):
        project_explanation = ProjectCardExplanation()
        project_explanation.projectCard = project
        project_explanation.explanation = explanation
        project_explanation.language = language
        project_explanation.auto = auto
        project_explanation.save()
        return project_explanation        
    
class ProjectCardExplanation(models.Model):
    explanation = models.TextField()
    language = models.CharField(max_length=2)
    projectCard = models.ForeignKey(ProjectCard)
    auto = models.BooleanField(default=False)
    
    objects = ProjectCardExplanationManager()
    
class ProjectCardRecipientManager(models.Manager):

    def create_recipient(self,\
                    project,\
                    recipient,\
                    language,\
                    auto):
        project_recipient = ProjectCardRecipient()
        project_recipient.projectCard = project
        project_recipient.recipient = recipient
        project_recipient.language = language
        project_recipient.auto = auto
        project_recipient.save()
        return project_recipient        
    
class ProjectCardRecipient(models.Model):
    recipient = models.TextField()
    language = models.CharField(max_length=2)
    projectCard = models.ForeignKey(ProjectCard)
    auto = models.BooleanField(default=False)
    
    objects = ProjectCardRecipientManager()
    
class ProjectCardWhereManager(models.Manager):

    def create_where(self,\
                    project,\
                    where,\
                    language,\
                    auto):
        project_where = ProjectCardWhere()
        project_where.projectCard = project
        project_where.where = where
        project_where.language = language
        project_where.auto = auto
        project_where.save()
        return project_where        
    
class ProjectCardWhere(models.Model):
    where = models.TextField()
    language = models.CharField(max_length=2)
    projectCard = models.ForeignKey(ProjectCard)
    auto = models.BooleanField(default=False)
    
    objects = ProjectCardWhereManager()
    
class ProjectCardTitleManager(models.Manager):

    def create_title(self,\
                    project,\
                    title,\
                    language,\
                    auto):
        project_title = ProjectCardTitle()
        project_title.projectCard = project
        project_title.title = title
        project_title.language = language
        project_title.auto = auto
        project_title.save()
        return project_title    
    
class ProjectCardTitle(models.Model):
    title = models.TextField()
    language = models.CharField(max_length=2)
    projectCard = models.ForeignKey(ProjectCard)
    auto = models.BooleanField(default=False)
    
    objects = ProjectCardTitleManager()
    
class ProjectCardSummaryManager(models.Manager):

    def create_summary(self,\
                    project,\
                    summary,\
                    language,\
                    auto):
        project_summary = ProjectCardSummary()
        project_summary.projectCard = project
        project_summary.summary = summary
        project_summary.language = language
        project_summary.auto = auto
        project_summary.save()
        return project_summary        
    
class ProjectCardSummary(models.Model):
    summary = models.TextField()
    language = models.CharField(max_length=2)
    projectCard = models.ForeignKey(ProjectCard)
    auto = models.BooleanField(default=False)
    
    objects = ProjectCardSummaryManager()
    
class ProjectCardNecessityManager(models.Manager):

    def create_necessity(self,\
                    project,\
                    necessity,\
                    language,\
                    auto):
        project_necessity = ProjectCardNecessity()
        project_necessity.projectCard = project
        project_necessity.necessity = necessity
        project_necessity.language = language
        project_necessity.auto = auto
        project_necessity.save()
        return project_necessity      
    
class ProjectCardNecessity(models.Model):
    necessity = models.TextField()
    language = models.CharField(max_length=2)
    projectCard = models.ForeignKey(ProjectCard)
    auto = models.BooleanField(default=False)
    
    objects = ProjectCardNecessityManager()
    
class ProjectAreaManager(models.Manager):

    def get_proposals_by_area(self,\
                            area):
        try:
            proposal_list = ProjectArea.objects.filter(area=area)
            if len(proposal_list)>0:
                return map(lambda x: x.project, proposal_list)
            else:
                return []
        except Exception as error:
            
            return []    
    
    
class ProjectArea(models.Model):
    area = models.ForeignKey(Area)
    project = models.ForeignKey(ProjectCard)
    
    objects = ProjectAreaManager()
    
class ProjectCardDocumentManager(models.Manager):

    def create_document(self,\
                    project,\
                    filename):
        
        project_document = ProjectCardDocument()
        project_document.projectCard = project
        project_document.doc = filename
        project_document.save()
        return project_document            
    
class ProjectCardDocument(models.Model):
    projectCard = models.ForeignKey(ProjectCard)
    doc = models.FileField(upload_to=MEDIA_ROOT)
    
    objects = ProjectCardDocumentManager()
    
    
class ProjectCommentManager(models.Manager):

    def create_comment(self,\
                    comment,\
                    project,\
                    profile,\
                    parent):
        project_comment = ProjectComment()
        project_comment.comment = comment
        project_comment.author = profile
        project_comment.project = project
        project_comment.parent_comment = parent
        project_comment.save()
        return project_comment
        
        
    
class ProjectComment(models.Model):
    project = models.ForeignKey(ProjectCard)
    comment = models.TextField()
    parent_comment = models.ForeignKey("self",null=True)
    author = models.ForeignKey(Profile)
    date = models.DateField(auto_now = True, null = True)
    
    objects = ProjectCommentManager()
    
    def get_subcomments(self):
        return self.projectcomment_set.all()
    
class Specification(models.Model):
    project = models.ForeignKey(ProjectCard)
    area = models.ForeignKey(Area)
    #recipient = models.TextField()
    recipient_number = models.IntegerField()
    economic_prediction = models.FloatField()
    execution_term = models.CharField(max_length=300)
    #technical_valuation = models.TextField()
    
class SpecificationRecipient(models.Model):
    recipient = models.TextField()
    language = models.CharField(max_length=2)
    specification = models.ForeignKey(Specification)
    
class SpecificationValuation(models.Model):
    valuation = models.TextField()
    language = models.CharField(max_length=2)
    specification = models.ForeignKey(Specification)
    
class SpecificationArea(models.Model):
    area = models.ForeignKey(Area)
    specification = models.ForeignKey(Specification)      
    
    
class Criterion(models.Model):
    criterion = models.CharField(max_length=300)
    
class ProposalCriterionManager(models.Manager):

    def create_proposal_criterion(self,\
                                proposal,\
                                criterion,\
                                value):
        proposal_criterion = ProposalCriterion()
        proposal_criterion.proposal = proposal
        proposal_criterion.criterion = criterion
        proposal_criterion.value = value
        proposal_criterion.save()
        
    def edit_proposal_criterion(self,\
                                proposal,\
                                criterion,\
                                value):
        try:
            proposal_criterion = ProposalCriterion.objects.get(proposal = proposal,\
                                                 criterion = criterion)
            proposal_criterion.value = value
            proposal_criterion.save()
        except Exception as error:
            print error
    
class ProposalCriterion(models.Model):
    proposal = models.ForeignKey(Proposal)
    criterion = models.ForeignKey(Criterion)
    value = models.BooleanField()
    
    objects = ProposalCriterionManager()
    
class Vote(models.Model):
    project = models.ForeignKey(ProjectCard)
    elector = models.ForeignKey(Profile)
    
class PresentialVotes(models.Model):
    project = models.ForeignKey(ProjectCard)
    number = models.IntegerField()
    
class Fond(models.Model):
    proposal = models.ForeignKey(Proposal)
    author = models.ForeignKey(Profile)
    

class EventManager(models.Manager):

    def create_event(self,\
                    date):
        event = Event()
        event.date = date
        event.save()
        return event

class Event(models.Model):
    date = date = models.DateField(null = True)
    
    def get_content(self,\
                    lang):
        try:
            content = EventContent.objects.get(event = self, language = lang)                 
            if content.auto:
                return "<img src='"+AT_ICON+"'> "+content.content
            else:
                return content.content
        except Exception as error:
            return ""
    
    objects = EventManager()
    
class EventContentManager(models.Manager):
    
    def create_event(self,\
                    event,\
                    content,\
                    language,\
                    auto):
        event_content = EventContent()
        event_content.auto = auto
        event_content.content = content
        event_content.language = language
        event_content.event = event
        event_content.save()
        return event_content 
    
class EventContent(models.Model):
    language = models.CharField(max_length=2)
    content = models.TextField()
    event = models.ForeignKey(Event)
    auto = models.BooleanField(default=False)
    
    objects = EventContentManager()


    
