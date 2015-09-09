# project wide urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()
import settings

# import your urls from each app here, as needed
#import partaidetza_app.urls

urlpatterns = patterns('',

    url(r'^$', 'partaidetza_app.views.home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # logout
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    # profile
    url(r'^profile/$', 'partaidetza_app.views.profile'),
    #register
    url(r'^register/$', 'partaidetza_app.views.register'),
    # new proposal
    url(r'^new_proposal/$', 'partaidetza_app.views.new_proposal'),
    # new accepted proposal
    url(r'^new_accepted_proposal/$', 'partaidetza_app.views.new_accepted_proposal'),
    url(r'^new_accepted_proposal_manually/$', 'partaidetza_app.views.new_accepted_proposal_manually'),
    # manage accepted proposal
    url(r'^manage_accepted_proposals/$', 'partaidetza_app.views.manage_accepted_proposals'),
    # manage accepted proposal
    #url(r'^manage_accepted_proposal/(?P<proposal_id>.*)$', 'partaidetza_app.views.manage_accepted_proposal'),
    # manage proposals
    url(r'^manage_proposals/$', 'partaidetza_app.views.manage_proposals'),
    # manage my proposals
    url(r'^manage_my_proposals/$', 'partaidetza_app.views.manage_my_proposals'),
    # manage criterions
    url(r'^manage_criterions/$', 'partaidetza_app.views.manage_criterions'),
    # get xml files
    url(r'^get_xlsx/(?P<proposal_id>.*)$', 'partaidetza_app.views.get_xlsx'),
    url(r'^get_multiple_xlsx/(?P<proposal_id_list>.*)$', 'partaidetza_app.views.get_multiple_xlsx'),
    # delete proposals
    url(r'^delete_proposals/(?P<proposal_id_list>.*)$', 'partaidetza_app.views.delete_proposals'),
    # delete projects
    url(r'^delete_projects/(?P<project_id_list>.*)$', 'partaidetza_app.views.delete_projects'),
    # proposals
    url(r'^proposals/$', 'partaidetza_app.views.proposals'),
    url(r'^proposals_by_area/$', 'partaidetza_app.views.proposals_by_area'),
    # accepted proposals
    url(r'^accepted_proposals/$', 'partaidetza_app.views.accepted_proposals'),
    url(r'^accepted_proposals_by_area/$', 'partaidetza_app.views.accepted_proposals_by_area'),
    # proposal
    url(r'^proposal/(?P<proposal_id>.*)$', 'partaidetza_app.views.proposal'),
    # accepted proposal
    url(r'^accepted_proposal/(?P<proposal_id>.*)$', 'partaidetza_app.views.accepted_proposal'),
    # search result
    url(r'^search_results/$', 'partaidetza_app.views.search_results'),
    # agenda
    url(r'^add_event/$', 'partaidetza_app.views.add_event'),
    url(r'^agenda/$', 'partaidetza_app.views.agenda'),
    # AJAX urls
    url(r'^ajax_vote$', 'partaidetza_app.ajax_views.ajax_vote'),
    url(r'^ajax_fond$', 'partaidetza_app.ajax_views.ajax_fond'),
    url(r'^ajax_edit_proposal_cost$', 'partaidetza_app.ajax_views.ajax_edit_proposal_cost'),
    url(r'^ajax_edit_proposal_recipient_number$', 'partaidetza_app.ajax_views.ajax_edit_proposal_recipient_number'),
    url(r'^ajax_edit_proposal_area$', 'partaidetza_app.ajax_views.ajax_edit_proposal_area'),
    url(r'^ajax_get_proposal_area$', 'partaidetza_app.ajax_views.ajax_get_proposal_area'),
    url(r'^ajax_get_proposal_state$', 'partaidetza_app.ajax_views.ajax_get_proposal_state'),
    url(r'^ajax_edit_proposal_title$', 'partaidetza_app.ajax_views.ajax_edit_proposal_title'),
    url(r'^ajax_edit_proposal_summary$', 'partaidetza_app.ajax_views.ajax_edit_proposal_summary'),
    url(r'^ajax_edit_proposal_recipient$', 'partaidetza_app.ajax_views.ajax_edit_proposal_recipient'),
    url(r'^ajax_edit_proposal_necessity$', 'partaidetza_app.ajax_views.ajax_edit_proposal_necessity'),
    url(r'^ajax_edit_proposal_where$', 'partaidetza_app.ajax_views.ajax_edit_proposal_where'),
    url(r'^ajax_edit_project_cost$', 'partaidetza_app.ajax_views.ajax_edit_project_cost'),
    url(r'^ajax_edit_project_recipient_number$', 'partaidetza_app.ajax_views.ajax_edit_project_recipient_number'),
    url(r'^ajax_edit_project_area$', 'partaidetza_app.ajax_views.ajax_edit_project_area'),
    url(r'^ajax_edit_project_title$', 'partaidetza_app.ajax_views.ajax_edit_project_title'),
    url(r'^ajax_edit_project_summary$', 'partaidetza_app.ajax_views.ajax_edit_project_summary'),
    url(r'^ajax_edit_project_recipient$', 'partaidetza_app.ajax_views.ajax_edit_project_recipient'),
    url(r'^ajax_edit_project_necessity$', 'partaidetza_app.ajax_views.ajax_edit_project_necessity'),
    url(r'^ajax_edit_project_where$', 'partaidetza_app.ajax_views.ajax_edit_project_where'),
    url(r'^ajax_edit_project_source$', 'partaidetza_app.ajax_views.ajax_edit_project_source'),
    url(r'^ajax_edit_project_explanation$', 'partaidetza_app.ajax_views.ajax_edit_project_explanation'),
    url(r'^ajax_more_like_this_in_title$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_titles'),
    url(r'^ajax_more_like_this_in_summary$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_summaries'),
    url(r'^ajax_more_like_this_in_recipient$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_recipients'),
    url(r'^ajax_more_like_this_in_necessity$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_necessities'),
    url(r'^ajax_more_like_this_in_where$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_wheres'),
    url(r'^ajax_more_like_this_in_source$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_sources'),
    url(r'^ajax_more_like_this_in_explanation$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_explanations'),
    url(r'^ajax_more_like_this_in_event$', 'partaidetza_app.ajax_views.ajax_more_like_this_in_events'),
    url(r'^ajax_correct_language$', 'partaidetza_app.ajax_views.ajax_correct_language'),
    url(r'^ajax_validate_language$', 'partaidetza_app.ajax_views.ajax_validate_language'),
    url(r'^ajax_add_point_to_map_proposal$', 'partaidetza_app.ajax_views.ajax_add_point_to_map_proposal'),
    url(r'^ajax_add_point_to_map_project$', 'partaidetza_app.ajax_views.ajax_add_point_to_map_project'),
    url(r'^ajax_delete_point_from_map_proposal$', 'partaidetza_app.ajax_views.ajax_delete_point_from_map_proposal'),
    url(r'^ajax_delete_point_from_map_project$', 'partaidetza_app.ajax_views.ajax_delete_point_from_map_project'),
    #(r'^search/', include('haystack.urls')),
    #url(r'^bonbardeoa', 'partaidetza_app.views.bonbardeoa'),
    #url('^', include('django.contrib.auth.urls')),
    # catch all, redirect to myfirstapp home view
    #url(r'.*', 'partaidetza_app.views.home'),
    
    )
