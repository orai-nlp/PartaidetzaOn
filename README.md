PartaidetzaOn 
=========================================================
*e-participation open-source platform*
=========================================================

Requirements: 

- Python 2.7 or 3.3, 
- MySQL

Installation
------------

*Create project's files:

        $ python bootstrap.py
        $ bin/buildout
        $ bin/django create_search_indexes
                - (creates search_indexes.py file in partaidetza_app folder. Configuration needed!)

*Create project's MYSQL database:

        $ mysql -u YOUR_MYSQL_USER -p -e "create database YOUR_DATABASE"
        $ bin/django syncdb
        
*Install Solr and create indexes:

        - Download solr from http://lucene.apache.org/solr/downloads.html
        - Decompress in /src/partaidetza/
        - Create a collection
        - Add Elhuyar's APIs to Solr libraries:
                $ cp solr_apis/* solr_VERSION_NUMBER/examples/YOUR_COLLECTION 
        - Launch Solr server
        - Create YOUR_COLLECTION's conf file 
                -- (See Configuration section for more detail)
        - Use this conf file to configure solr collection:
                $ bin/django build_solr_schema > conf.xml
                -- (solr_VERSION_NUMBER/examples/YOUR_COLLECTION/conf). Configuration needed!
        - Edit configuration depending on your needs.     
        - Use this to rebuild the index
                $ bin/django rebuild_index -v2
        
        
Configuration
-------------

        - LANGUAGES: Set the languages that will be present on the project.
                Example: LANGUAGES=(('eu','Basque'),('es','Spanish'),('en','English'),('fr','French'),)
        - DATABASES: Database configs.
                Example: DATABASES={'default':{'ENGINE':'django.db.backends.mysql','NAME':'partaidetza_db','USER': 'root''PASSWORD': 'manterola','HOST': '','PORT': '',}}
        - ACCEPTED_IMAGE_FORMATS: Defines the allowed image formats.
                Example: ACCEPTED_IMAGE_FORMATS=['jpg','png','jpeg']
        - MAX_VOTES_PER_USER: Set the maximum votes per user:
                Example: MAX_VOTES_PER_USER=3
        - MAX_FONDS_PER_USER: Set the maximum fonds per user:
                Example: MAX_FONDS_PER_USER=3
        - AT_LANGUAGE_PRIORITY: Configures the automatic translation's language priority (source language priority)
                Example: ['es','eu','en','fr']
        - OPENTRAD_CODE = Sets the Opentrad key
                Example: OPENTRAD_CODE='XXXX'
        - AT_ICON: Sets the icon to be shown when automaticly translated texts are shown
                Example: AT_ICON="YOUR_ICON_PATH"
        - HAYSTACK_CONNECTIONS: Configures Haystack connection (Solr)
                Example: HAYSTACK_CONNECTIONS={'default':{'ENGINE':'haystack.backends.solr_backend.SolrEngine','URL': 'http://YOUR_HOST/solr/YOUR_COLLECTION'},}
        - HAYSTACK_SIGNAL_PROCESSOR: Configures Haystack signal processor
                Example: HAYSTACK_SIGNAL_PROCESSOR='haystack.signals.RealtimeSignalProcessor'
        - MORE_LIKE_THIS_RESULTS_NUMBER: Set the number of "more like this" results
                Example: MORE_LIKE_THIS_RESULTS_NUMBER=10
        - TEXT_CAT_PATH: Sets Text_cat executable path
                Example: TEXT_CAT_PATH="YOUR_TEXTCAT_PATH"
        - TEXT_CAT_MODELS_PATH: Sets Text_cat model's path
                Example: TEXT_CAT_MODELS_PATH="YOUR_TEXTCAT_MODEL_PATH"
        - TEXT_CAT_LANGUAGE_CONVERTOR: Configures the convertions of the language names that Text_cat uses
                Example: TEXT_CAT_LANGUAGE_CONVERTOR: {"basque":"eu","spanish":"es","english":"en","french":"fr"}
        - LEAFLET_CONFIG: Configures Leaflet (Maps)
                Example: LEAFLET_CONFIG = {'DEFAULT_CENTER': (43.2714582916227,-2.0481375743),'DEFAULT_ZOOM': 18,'MIN_ZOOM': 3,'MAX_ZOOM': 18,'ATTRIBUTION_PREFIX': ''}
        
        
        

    

