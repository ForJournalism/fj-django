Django for Journalism
===================================

## Chapter 1

#### Introduction; Overview of a Django app; Data analysis

We'll start off the course with a quick description of the Django project/app structure and we'll walk through the data, breaking up an inspections project into three basic real-world model buckets. We'll talk through some of the quirks of inspection data and set up the project. Finally, we'll talk a little bit about virtualenv and the Python environment. And we'll commit our basic code to a VCS.

#### 00:53:16

* Sets up virtualenv.
* Checks out repository.
* Creates project.
* Creates apps; restaurant and inspection.
* Sets up postgres db and user.
* Changes settings file to add configuration.
* Sets up and installs requirements.
* Adds admin and south to settings file.
* Adds admin to urls.py.
* Demonstrates working runserver.
* Sets up virtualenv hooks for postactivate.
* Adds model classes for Restaurant, Inspection, Observation.
* Adds restaurant and inspection to installed_apps in settings.py.
* Runs initial south migration.
* Changes a field in Inspection.
* Runs updated south migration for inspection.
* Adds admin.py for restaurant, inspection.
* Sees add form in admin for Restaurant, Inspection, Observation.

## Chapter 2

#### Models and importing data

Chapter 2 focuses on writing code to support the real-world models we theorized in Chapter 1. As part of Chapter 2, we'll also discuss South and basic database migrations.

#### 01:22:35

* Walks through the process of scraping data from the Web.
* Introduces requests.
* Introduces beautifulsoup.
* Writes scraper for restaurants.
* Writes scraper for inspections.
* Writes and reads from JSON on the local filesystem.
* Demonstrates git branch and git merge.

## Chapter 3

#### Importing data

We'll write an importer to parse the data source and insert it into our models. This parsing will involve some light web scraping and discussion of scraping framework BeautifulSoup. We'll also talk through the difference between creating and updating records and making sure that we don't have duplicate data.

#### 01:30:20

* Introduces management commands.
* Writes an importer for Restaurant from JSON in previous chapter.
* Writes an importer for Inspection, Observation from JSON in previous chapter.
* Saves a model instance -- several, actually.
* Updates the admin.py for our restaurant and inspection to make forms look nice.
* Performs another south migration to add a column to the database/field to a model.

## Chapter 4

#### Application structure; Views, URLs and Templates Phase 1

Chapter 4 starts off with a discussion of the two phases of our application: existing inspection data and live inspection data. We'll use this discussion to explain the model-view-template structure of Django and work backwards from URLs through views to models and templates. Finally, we'll start writing code for the existing-data phase of our Web application, since iterations are good.

#### 01:58:38

* Introduces class-based views.
* Writes a restaurant list URL, view and template.
* Writes a restaurant detail URL, view and template.
* Writes an inspection detail URL, view and template.
* Geocodes restaurants using geocoder.py and Google V3.
* Adds geographic fields to the model using south.
* Adds a list of "nearby" restaurants on the restaurant detail page.
* Orders the list of "nearby" restaurants by distance.
* Updates the admin to show points on maps.

## Chapter 5

#### Views, URLs and Templates Phase 2

Chapter 5 dives into the live inspection results and builds an interesting homepage. We'll demonstrate the admin. Finally, we'll discuss some performance-related topics and how to make our application scale.

#### 01:40:32

* Writes top 10 restaurants by inspections.
* Writes top 10 restaurants by violations (observations).
* Identifies and solves a problem with duplicate inspections.
* Performs a database backup/reload with Postgres commands.
* Writes most recent 10 inspections.
* Writes restaurant chart by quadrant.
* Writes a view for restaurants by quadrant.
* Installs django-debug-toolbar, a debugging and performance-testing tool.
* Speeds up views with .values() queries, among other changes.

## Chapter 6

#### APIs and Search

If you're working on a dynamic web site, you're probably interested in APIs and/or search. We'll use django-tastypie to set up a full RESTful API for our restaurants site and django-haystack to build a search index. We'll even do some mildly advanced things like set up a search backend and enable faceted search!

#### 1:56:54

* Introduces django-tastypie, an API wrapper for Django.
* Writes an api.py for restaurants.
* Includes restaurant info in returned data.
* Includes inspections info in returned data.
* Includes observations info in returned data.
* Demonstrates URL filtering, ordering.
* Introduces django-haystack, a search engine wrapper for Django.
* Writes search index for restaurant names.
* Returns results from index and not from the database.
* Installs Apache Solr, a search engine backend.
* Demonstrates reindexing of a search engine.
* Updates the Solr schema, changing which fields are indexed.
* Creates facets and a template to allow searching by facet.

## Chapter 7

#### Putting it all together; Deployment; Maintenance

In Chapter 7, we'll talk about making our prototype official. We'll deploy it to a Web service-to-be-decided-soon (AWS? Heroku? S3 and flatfiles?) and discuss standard deployment tools like Fabric. We'll also talk about maintenance and a proper production-staging-development environment.

### Deliverables:

* An application deployed to the actual internet.
* Working cron jobs to update the app.
* A fabfile.py that deploys/updates/destroys our application.
* A multi-branch VCS for deploying to different environments.
