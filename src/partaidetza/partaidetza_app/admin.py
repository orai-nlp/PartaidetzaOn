from django.contrib import admin
from partaidetza.partaidetza_app.models import Genre, Profile, Proposal, ProposalArea, ProposalDocument, Specification, SpecificationArea, ProjectCard, ProjectArea, ProjectComment, Criterion, ProposalCriterion, Vote, PresentialVotes, Status

class AdminGenre(admin.ModelAdmin):
    pass
admin.site.register(Genre, AdminGenre)

class AdminProfile(admin.ModelAdmin):
    pass
admin.site.register(Profile, AdminProfile)

class AdminProposal(admin.ModelAdmin):
    pass
admin.site.register(Proposal, AdminProposal)

class AdminProposalArea(admin.ModelAdmin):
    pass
admin.site.register(ProposalArea, AdminProposalArea)

class AdminProposalDocument(admin.ModelAdmin):
    pass
admin.site.register(ProposalDocument, AdminProposalDocument)

class AdminSpecification(admin.ModelAdmin):
    pass
admin.site.register(Specification, AdminSpecification)

class AdminSpecificationArea(admin.ModelAdmin):
    pass
admin.site.register(SpecificationArea, AdminSpecificationArea)

class AdminProjectCard(admin.ModelAdmin):
    pass
admin.site.register(ProjectCard, AdminProjectCard)

class AdminProjectArea(admin.ModelAdmin):
    pass
admin.site.register(ProjectArea, AdminProjectArea)

class AdminProjectComment(admin.ModelAdmin):
    pass
admin.site.register(ProjectComment, AdminProjectComment)

class AdminCriterion(admin.ModelAdmin):
    pass
admin.site.register(Criterion, AdminCriterion)

class AdminProposalCriterion(admin.ModelAdmin):
    pass
admin.site.register(ProposalCriterion, AdminProposalCriterion)

class AdminVote(admin.ModelAdmin):
    pass
admin.site.register(Vote, AdminVote)

class AdminPresentialVotes(admin.ModelAdmin):
    pass
admin.site.register(PresentialVotes, AdminPresentialVotes)

class AdminStatus(admin.ModelAdmin):
    pass
admin.site.register(Status, AdminStatus)

