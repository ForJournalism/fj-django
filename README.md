Django for Journalism
===================================

## Chapter 1: Introduction; Overview of a Django app; Data analysis

We'll start off the course with a quick description of the Django project/app structure and we'll walk through the data, breaking up an inspections project into three basic real-world model buckets. We'll talk through some of the quirks of inspection data and set up the project. Finally, we'll talk a little bit about virtualenv and the Python environment. And we'll commit our basic code to a VCS.

### Deliverables:

* A Django project called "inspections"
* Multiple apps to let us designate inspection data types and sources. These apps will have the files necessary to support a Django application: api.py, admin.py, models.py, views.py and urls.py.
* A settings.py and a global urls.py file.
* A "hello world" moment running the Django admin on localhost.
* A repository somewhere with the code in it. 
* Link to Git for Journalists

## Chapter 2: Models and importing data

Chapter 2 focuses on writing code to support the real-world models we theorized in Chapter 1. As part of Chapter 2, we'll also discuss South and basic database migrations.

### Deliverables:

* Each of the three applications will have working models.py files.
* We'll configure South and prepare an initial migration.
* We'll make a change to a model, create a migration and execute it.

## Chapter 3: Importing data

We'll write an importer to parse the data source and insert it into our models. We'll also talk through the difference between creating and updating records and making sure that we don't have duplicate data.

### Deliverables:

* We'll have a working importer that pulls data from the data source.
* We'll verify that we have data by checking it out in the admin.

## Chapter 4: Application structure; Views, URLs and Templates for Phase 1

Chapter 4 starts off with a discussion of the two phases of our application: existing inspection data and live inspection data. We'll use this discussion to explain the model-view-template structure of Django and work backwards from URLs through views to models and templates. Finally, we'll start writing code for the existing-data phase of our Web application, since iterations are good.

### Deliverables:
* Some functions in views.py and urls.py to support an inspection type and source detail pages. We'll also have list templates.
* Stub templates for our pages.
* Link to Responsive Design for Journalism

## Chapter 5: Views, URLs and Templates for Phase 2

Chapter 5 dives into the live inspection results and builds a live dashboard page. We'll demonstrate the admin. Finally, we'll discuss some performance-related topics and how to make our application scale.

### Deliverables:

* The rest of the functions in views.py and urls.py to support a live dashboard for inspection data streams.
* Updated bits in the existing views.py for type and source detail to add in live results to those pages.

## Chapter 6: APIs, JSON and widgets

Every modern Web application needs to have an API as well as a Web interface. We'll discuss why this is true, talk about TastyPie and pluggable applications for Django, and then set up some sample widget code for a single-source data widget.

### Deliverables:

* An updated api.py with TastyPie to demonstrate a JSON API for inspect results.
* Basic widget code for inspection results.
* Link to JavaScript for Journalism

## Chapter 7: Putting it all together; Deployment; Maintenance

In Chapter 7, we'll talk about making our prototype official. We'll deploy it to a Web service-to-be-decided-soon (AWS? Heroku? S3 and flatfiles?) and discuss standard deployment tools like Fabric. We'll also talk about maintenance and a proper production-staging-development environment.

### Deliverables:

* An application deployed to the actual internet.
* Working cron jobs to update the app.
* A fabfile.py that deploys/updates/destroys our application.
* A multi-branch VCS for deploying to different environments.
