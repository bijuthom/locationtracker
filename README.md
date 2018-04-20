# Location Tracker

**To run the application install the following software:**

postgresql 9.6.8, default user and db (postgres, postgres, postgres)

Install python version 3.6.5\
$ pip install django\
$ pip install djangorestframework\
$ pip install psycopg2\
$ pip install sphinxapi-py3\
$ pip install djangorestframework-jwt\
$ pip install django-sphinxql

**From the project subdirectory run the following commands:**

$ python manage.py migrate\
$ python manage.py createsuperuser (specify username and password for superuser)\
$ python manaye.py runserver

**The REST APIs should be available in the following urls:**

From localhost:8000

/admin/ (login to the admin UI)\
/api/locations/ (To upload &list locations)\
/api/location/{locationId}/ -view/modify a single location\
/api/user/search?q= -search user\
/api/location/search?q -search location\
/api/users/{userid}/locations/ -locations of a specific user\
/api/users/{userid}/routes/ - To view the routes of a user in date range                           
                              with date as optional query params start_date=yyyy/mm/dd ,end_date=yyyy/mm/dd                             
/api/search- freetext search with sphinx. Pass query as q=<some_keyword_to_search>'\
/api-token-auth/,/api-token-verify/,/api-token-refresh/ - jwt tokens                       

**Sphinx was configured using the following settings in sphinx.conf to create the indexes**\
source loc_source\
{\
    type      = pgsql\
    sql_host  = localhost\
    sql_user  = postgres\
    sql_pass  = postgres\
    sql_db    = postgres\
    sql_port  = 5433\
    sql_query = SELECT loc.id, loc.location , loc.loctime, loc.latitude, loc.longitude, u.username, u.email from trackerapp_userlocation loc\
                left join auth_user u on u.id=loc.user_id\
}

index loc_index\
{
    source        = loc_source\
    path          = C://sphinx/sphinx-3.0.3/abc.sph\
}

indexer\
{
    mem_limit    = 256M\
    write_buffer = 8M\
}

searchd\
{\
    listen                  = 9312\
    pid_file                = C://sphinx/searchd.pid\
    log         = C://sphinx/sphinx-3.0.3/log/searchd.log\
    query_log = C://sphinx/sphinx-3.0.3/log/query.log\
}