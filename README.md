# PartaidetzaOn
e-participation open-source platform

.. image:: https://secure.travis-ci.org/yourlabs/django-cities-light.png?branch=master
    :target: http://travis-ci.org/yourlabs/django-cities-light
.. image:: https://pypip.in/d/django-cities-light/badge.png
    :target: https://crate.io/packages/django-cities-light
.. image:: https://pypip.in/v/django-cities-light/badge.png   
    :target: https://crate.io/packages/django-cities-light

PartaidetzaOn -- *e-participation open-source platform*
=========================================================


Requirements: 

- Python 2.7 or 3.3, 
- MySQL

Installation
------------

Install partaidetzaOn::

    Create project's files:
        > python bootstrap.py
        > bin/buildout

    Create project's MYSQL database:
        > mysql -u your_mysql_user -p -e "create database YOUR_DATABASE"
        > bin/django syncdb
        
    Install Solr and create indexes:
        - Download solr from http://lucene.apache.org/solr/downloads.html
        - Decompress in /src/partaidetza/
        - Create a collection
        - Add Elhuyar's APIs to Solr libraries:
            cp solr_apis/* solr_VERSION_NUMBER/examples/YOUR_COLLECTION
        - Launch Solr server
        - Create YOUR_COLLECTION's conf file (Change project's setting.py file before execute this --> See Configuration section for more detail). Edit configuration depending on your needs.     
            > bin/django create_search_indexes > conf.xml . Use this conf file to configure solr collection (solr_VERSION_NUMBER/examples/YOUR_COLLECTION/conf)
        - Rebuild the index:
            > bin/django rebuild_index -v2
        
        
Configuration
-------------

Configure partaidetzaOn:


Running
-------

Running partaidetzaOn:
    

