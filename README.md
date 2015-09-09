PartaidetzaOn -- *e-participation open-source platform*
=========================================================

Requirements: 

- Python 2.7 or 3.3, 
- MySQL

Installation
------------

Install partaidetzaOn

Create project's files:

$ python bootstrap.py
$ bin/buildout
$ bin/django create_search_indexes (creates seatch_indexes.py file in partaidetza_app folder. Configuration needed!)

Create project's MYSQL database:

$ mysql -u YOUR_MYSQL_USER -p -e "create database YOUR_DATABASE"
$ bin/django syncdb
        
Install Solr and create indexes:

- Download solr from [here] - (http://lucene.apache.org/solr/downloads.html)
- Decompress in /src/partaidetza/
- Create a collection
- Add Elhuyar's APIs to Solr libraries:
cp solr_apis/* solr_VERSION_NUMBER/examples/YOUR_COLLECTION
    - Launch Solr server
- Create YOUR_COLLECTION's conf file (Change project's setting.py file before execute this --> See Configuration section for more detail).
$ bin/django build_solr_schema > conf.xml . Use this conf file to configure solr collection (solr_VERSION_NUMBER/examples/YOUR_COLLECTION/conf). Configuration needed!
        - Edit configuration depending on your needs.     
        - Rebuild the index:
            > bin/django rebuild_index -v2
        
        
Configuration
-------------

Configure partaidetzaOn:


Running
-------

Running partaidetzaOn:
    

