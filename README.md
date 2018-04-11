# Location Tracker

**To run the application install the following software:**

postgresql 9.6.8, default user and db (postgres, postgres, postgres)

Install python version 3.6.5\
$ pip install django\
$ pip install djangorestframework\
$ pip install psycopg2

**From the project subdirectory run the following commands:**

$ python manage.py migrate\
$ python manage.py createsuperuser (specify username and password for superuser)\
$ python manaye.py runserver

**The REST APIs should be available in the following urls:**

From localhost:8000

/admin/ (login to the admin UI)\
/api/locations/ (To upload &list locations)\
/api/location/{locationId}/ -view/modify a single location\
/api/users/{userid}/locations/ -locations of a specific user\
/api/users/{userid}/routes/ - To view the routes of a user in date range                           
                             as with date as optional query params
                             start_date=yyyy/mm/dd ,end_date=yyyy/mm/dd


                             
**Following additional changes are pending:**

1) Search API with Sphinx
2) Authentication & Permissions
3) To show the last known routes(locations) of a user when no date range is specified(
   currently displays all locations)

                             
                             
                             
                             
                             
                             
                             
                             
                             



    