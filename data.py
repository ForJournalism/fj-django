import json

from bs4 import BeautifulSoup
import requests

from dateutil.parser import *
from inspections.inspection.models import Inspection
from inspections.restaurant.models import Restaurant
from pytz import timezone
import pytz

def clean_text(string):
    """
    Remove breaks and tabs.
    Add other characters as necessary.
    Need this for cleaning up those
    disgusting government descriptions.
    """

    # Loop over this list of characters to remove.
    for char in ['\r', '\n', '\t']:

        # Remove them from the string.
        string = string.replace(char, '')

    # Return the now clean string.
    return string

def scrape_restaurants():
    """
    Scrapes list of restaurant inspections to a file.
    Index page is very slow to load.
    """

    # Set up an intermediate data storage.
    # In this case, a python dictionary.
    # Dictionaries are like JSON objects.
    # Keys and values.
    data = {}

    # This is the data we need to POST
    # to the form in order to get a response.
    data['a'] = 'Inspections'
    data['inputEstabName'] = ''
    data['inputPermitType'] = 'ANY'
    data['inputInspType'] = 'ANY'
    data['inputWard'] = 'ANY'
    data['inputQuad'] = 'ANY'
    data['btnSearch'] = 'Search'

    # Set the URL to the inspections list page.
    # It lists restaurants.
    url = 'http://washington.dc.gegov.com/webadmin/dhd_431/web/index.cfm'

    # POST our data to the inspections list page.
    r = requests.post(url, data=data)

    # Write the result to a file, because it takes FOREVER to scrape.
    with open('data/restaurant_list.html', 'w') as htmlfile:
        htmlfile.write(r.content)

def parse_restaurants():
    """
    Parses the DC restaurant inspections list page.
    Will read from local file instead of fetching via requests.
    """

    # Open the file we just wrote.
    with open('data/restaurant_list.html', 'r') as htmlfile:
        soup = BeautifulSoup(htmlfile.read())

    # Set up a blank list to hold our resulting restaurants.
    # We'll represent each restaurant as a dictionary.
    restaurants = []

    # Let's get a list of all of the restaurants on that page.
    # Hint: They're inside a div with the ID divInspectionSearchResults
    # and then the UL/LIs inside there.
    restaurant_list = soup.select('#divInspectionSearchResults > ul > li')

    # Loop over this list of restaurant HTML.
    # Uses enumerate because it's nice to know where you are in the loop.
    # In this case, i is our spot in the loop, and restaurant is this
    # particular restaurant in the list we're looping over.
    for i, restaurant in enumerate(restaurant_list):

        # We can get index errors for restaurants without all of the
        # correct data. We don't want to scrape those anyway.
        # So let's try/except those. The exception is an IndexError.
        try:

            # We want to check to make sure the restaurant's name is
            # hyperlinked. If not, it's not an important restaurant
            # and it doesn't have any inspections.
            if restaurant.select('h3 a')[0].text.strip() != '':

                # Okay, set up a dictionary to represent this individual
                # restaurant. Remember from above? Keys and values.
                restaurant_dict = {}

                # Set up a key "title" with the value of the restaurant's title.
                restaurant_dict['title'] = restaurant.select('h3 a')[0].text.strip()

                # Set up a key "permit_id" and fill it with an integer that is the permit ID.
                restaurant_dict['permit_id'] = int(restaurant.select('h3 a')[0]['href'].split('permitID=')[1].strip())

                # Construct an inspection URL for future digging.
                restaurant_dict['inspection_url'] = 'http://washington.dc.gegov.com/webadmin/dhd_431/web/index.cfm?a=inspections&permitID=%s' % restaurant_dict['permit_id']
                
                # Can't use enumerate because we have to skip
                # over some trips through the loop.
                index = 0
                for string in restaurant.strings:
                    string = string.strip()

                    if string != '':
                        if index == 1:
                            restaurant_dict['address'] = string.strip()

                        if index == 2:
                            try:
                                restaurant_dict['quadrant'] = string.split('Quad:')[1].strip()
                            except IndexError:
                                restaurant_dict['quardrant'] = None

                            try:
                                restaurant_dict['ward'] = int(string.split('Ward: Ward')[1].split('|')[0].strip())
                            except IndexError:
                                restaurant_dict['ward'] = None

                        if index == 3:
                            restaurant_dict['type'] = string.split('Type:')[1].strip()

                        index += 1

                # Skip restaurants that aren't restaurants or delis.
                # Focusing for now on restaurants over ice cream trucks or
                # other things.
                if restaurant_dict['type'] in ['Restaurant Total', 'Delicatessen']:
                    restaurants.append(restaurant_dict)

                    # Always send something to the stdout.
                    print '%s\t%s' % (i, restaurant_dict['title'])

            else:

                # This means "give up and go to the next one."
                pass

        except IndexError:

            # This means "give up and go to the next one."
            pass

    with open('data/restaurant_list.json', 'wb') as jsonfile:
        jsonfile.write(json.dumps(restaurants))

def scrape_inspections():
    """
    Reads from the restaurant list.
    Gets links to individual inspection pages.
    """

    # Two possible outcomes from this:
    # 1. An inspection.
    # 2. An error.
    # If it's an inspection, write the data to this list.
    # If it's an error, write data to the error list.
    inspections = []
    errors = []

    # Open and read from our restaurant list file.
    with open('data/restaurant_list.json', 'rb') as jsonfile:
        restaurants = json.loads(jsonfile.read())

    # Loop over the restaurants in the restaurant list file.
    for i, restaurant in enumerate(restaurants):

        # Follow the inspection_url we set up.
        r = requests.get(restaurant['inspection_url'])

        # Parse the resulting HTML with BeautifulSoup.
        soup = BeautifulSoup(r.content)

        # Get all of the links inside the div ID'ed divInspectionSearchResultsListing.
        for link in soup.select('#divInspectionSearchResultsListing a'):    
    
            # Sometimes, we get an error when trying to index into this list.
            # Perhaps a restaurant with no inspections?
            # Also restaurants with poor HTML below.
            try:

                # If we succeed, set up a dictionary to hold the inspection data.
                inspection_dict = {}

                # It's a dictionary WITHIN a dictionary!
                # Writes all of the keys/values we know about this restaurant
                # inside of this inspection's data.
                # How handy for later!
                inspection_dict['restaurant'] = restaurant

                # Get the inspection_id. These are (possibly?) unique.
                inspection_dict['inspection_id'] = link['href'].split('../lib/mod/inspection/paper/_paper_food_inspection_report.cfm?inspectionID=')[1].split('&')[0]

                # Construct the inspection detail URL from the inspection_id.
                inspection_dict['inspection_url'] = "http://washington.dc.gegov.com/webadmin/dhd_431/lib/mod/inspection/paper/_paper_food_inspection_report.cfm?wguid=1367&wgunm=sysact&wgdmn=431&inspectionID=%s" % inspection_dict['inspection_id']

                # Print something to stdout so we can see progress.
                print '%s\t%s: %s' % (i, inspection_dict['restaurant']['title'], inspection_dict['inspection_id'])

                # Append this item to the successful list.
                inspections.append(inspection_dict)

            except IndexError:

                # Oops, there was an error. Append some debugging info to the error list.
                print 'ERROR: %s\t%s' % (i, restaurant['title'])
                errors.append({'link_url': link['href'], 'restaurant': restaurant})

    # When we're done, write both the inspections AND the errors to files.
    with open('data/inspection_scrape_list.json', 'wb') as jsonfile:
        jsonfile.write(json.dumps(inspections))

    # Check to be sure we have errors before writing an error file.
    if len(errors) > 0:
        with open('data/inspection_scrape_errors.json', 'wb') as jsonfile:
            jsonfile.write(json.dumps(errors))

def scrape_inspection_html():
    """
    Reads from the inspection_scrape_list.
    Grabs inspection detail page.
    Writes it to HTML file in data/inspections.
    """

    # Open the scrape_list JSON file.
    with open('data/inspection_scrape_list.json', 'rb') as jsonfile:
        inspections = json.loads(jsonfile.read())

    # Loop over the inspections.
    for i, inspection in enumerate(inspections):

        # For each one, get the inspection detail URL.
        r = requests.get(inspection['inspection_url'])

        # Don't even try to parse these live.
        # Just write 'em to local files.
        with open('data/inspections/%s-%s.html' % (inspection['restaurant']['permit_id'], inspection['inspection_id']), 'wb') as htmlfile:
            htmlfile.write(r.content)
        
        # Print something to stdout.
        print i, inspection['inspection_id']

def parse_inspection_html(inspection_list=None):
    """
    Reads from the inspection_scrape_list.
    Reads each inspection detail page in data/inspections.
    Parses the HTML.
    Writes to inspection_list.html.
    """
    # Open the scrape_list. We need to loop over each of the inspections
    # and get the local HTML file for them.
    # Then, we need to parse that file.
    # Unless we pass it a list of inspections, of course.
    if inspection_list == None:
        with open('data/inspection_scrape_list.json', 'rb') as jsonfile:
            inspections = json.loads(jsonfile.read())
    else:
        inspections = inspection_list

    # Okay, here's the list where we'll store the updated
    # inspection data.
    updated_inspections = []

    # Loop over the inspections with enumerate() so we can have an index.
    for i, inspection in enumerate(inspections):

        # Open the individual inspection detail report for this inspection.
        # Unless we pass an inspection list.
        # In that case, do something else.
        if inspection_list == None:
            with open('data/inspections/%s-%s.html' % (inspection['restaurant']['permit_id'], inspection['inspection_id']), 'rb') as htmlfile:
                soup = BeautifulSoup(htmlfile.read())

        else:
            # If we pass an inspection list, get the URL to scrape from that.
            r = requests.get(inspection['inspection_url'])
            soup = BeautifulSoup(r.content)
        
        # Create an intermediate data store.
        # It's a dictionary again! Always with the dictionaries.
        inspection_dict = {}

        # Grab the inspection type, e.g., routine, followup, complaint.
        inspection_dict['type'] = soup.select('div.container > div')[16].text.strip()

        # Time is hard. Let's talk this over.
        # In the page, there's a date, and then two times.
        # Let's grab ALL the pieces and chop 'em up by newlines.
        # BeautifulSoup's .text will render newlines for new elements.
        time_part = soup.select('html > body > table')[1].select('table')[0].select('tr')[3].text.split('\n')

        # Okay, so the time_in is the date + the bits from the time_in fields.
        inspection_dict['time_in'] = '%s/%s/%s %s:%s %s' % (
            time_part[4].strip(),
            time_part[6].strip(),
            time_part[8].strip(),
            time_part[10].strip(),
            time_part[12].strip(),
            time_part[13].strip()
        )

        # Same deal with time_out.
        inspection_dict['time_out'] = '%s/%s/%s %s:%s %s' % (
            time_part[4].strip(),
            time_part[6].strip(),
            time_part[8].strip(),
            time_part[15].strip(),
            time_part[17].strip(),
            time_part[18].strip()
        )

        # Next up, the risk category.
        # Basic plan: Loop over those checkboxes.
        # Find the one that's red.
        # Check our position in the loop.
        # Add one, and that's our risk category.
        for j, z in enumerate(soup.select('div.checkboxRedN')):
            if z['style'].split('height:5px;width:5px;background-color:')[1].split(';')[0] == '#FF0000':
                inspection_dict['risk_category'] = j + 1

        # Okay, now for the critical/noncritical violations and
        # the number fixed on site.
        # Unfortunately, these are just blank, rather than 0 when
        # empty. So we have to try/except on a ValueError.
        try:
            crit = int(soup.select('html > body > table')[1].select('table')[1].select('tr')[1].select('td')[1].text.strip())
        except ValueError:
            crit = 0

        try:
            cos = int(soup.select('html > body > table')[1].select('table')[1].select('tr')[1].select('td')[3].text.strip())
        except ValueError:
            cos = 0

        try:
            ncrit = int(soup.select('html > body > table')[1].select('table')[1].select('tr')[2].select('td')[1].text.strip())
        except ValueError:
            ncrit = 0

        try:
            ncos = int(soup.select('html > body > table')[1].select('table')[1].select('tr')[2].select('td')[3].text.strip())
        except ValueError:
            ncos = 0

        # Save these counts to the dictionary.
        inspection_dict['critical'] = crit
        inspection_dict['critical_corrected_on_site'] = cos
        inspection_dict['noncritical'] = ncrit
        inspection_dict['noncritical_corrected_on_site'] = ncos

        # Okay, next up: The actual violations, termed "observations."
        # In the same way a restaurant can have many inspections,
        # an inspection can have many observations.
        # Let's set up a list to deal with these.
        inspection_dict['observations'] = []

        # Okay. So, the way we check for observations is by first
        # checking to see if there's more than one table row with
        # these specs. If yes, there are violations. Otherwise,
        # there aren't.
        if len(soup.select('table.fs_10px tr')) > 1:

            # Okay, so since there's more than one row,
            # loop over them. And while were at it, check
            # to make sure that the first cell has something
            # in it. Otherwise, it's this weird formatting
            # thing they do.
            for z in soup.select('table.fs_10px tr')[1:]:
                if len(z.select('td')[0].text.split()) > 0:
                    try:

                        # For each observation, make a little
                        # dictionary containing the three keys.
                        observations_dict = {}
                        observations_dict['observation'] = clean_text(z.select('td')[0].text.strip())
                        observations_dict['dcmr'] = clean_text(z.select('td')[1].text.strip())
                        observations_dict['correction'] = clean_text(z.select('td')[2].text.strip())
                        inspection_dict['observations'].append(observations_dict)

                    except IndexError:
                        # There's an exception where they describe the type of sanitizer.
                        # There's nothing more unholy than government tables.
                        pass

        # Okay, this is a sneaky trick.
        # Let's say we have two dictionaries.
        # dict1 and dict2.
        # I want a single dictionary containing
        # both of their keys/values.
        # The one-step method for combining them
        # is dict(dict1, **dict2), since the **
        # just unpacks the second dictionary as 
        # keys and values.
        inspection = dict(inspection, **inspection_dict)

        # Append this newly updated inspection dict to
        # our list of updated inspections.
        updated_inspections.append(inspection)

        # Print something to the stdout.
        print i, inspection['time_in']

    # Write the results to inspection_list.json.
    # We'll write a management command to parse this
    # and save inspections in chapter 3.
    with open('data/inspection_list.json', 'wb') as jsonfile:
        jsonfile.write(json.dumps(updated_inspections))

def scrape_latest_inspections():
    """
    Grabs the latest inspection date from the database.
    Gets all inspections newer than that.
    Technically, just returns a list very similar to
    inspection_scrape_list.json.
    """

    latest_inspection = Inspection.objects.all().order_by('-time_in')[50]

    inspection_scrape_list = []

    # Set up an intermediate data storage.
    # In this case, a python dictionary.
    # Dictionaries are like JSON objects.
    # Keys and values.
    data = {}

    # This is the data we need to POST
    # to the form in order to get a response.
    data['a'] = 'Inspections'
    data['inputEstabName'] = ''
    data['inputPermitType'] = 'ANY'
    data['inputInspType'] = 'ANY'
    data['inputWard'] = 'ANY'
    data['inputQuad'] = 'ANY'
    data['btnSearch'] = 'Search'

    # Set the URL to the inspections list page.
    # It lists restaurants.
    url = 'http://washington.dc.gegov.com/webadmin/dhd_431/web/index.cfm'

    # POST our data to the inspections list page.
    r = requests.post(url, data=data)

    # Parse the resulting HTML with BeautifulSoup.
    soup = BeautifulSoup(r.content)

    # Get all of the links inside the div ID'ed divInspectionSearchResultsListing.
    for restaurant in soup.select('#divInspectionSearchResults li'):    

        try:
            # Get the restaurant from the DB.
            obj = Restaurant.objects.filter(title=restaurant.select('h3')[0].text.strip()).values()[0]

            # Get the links under the restaurant title.
            # Re-using an ID. Claaaaasssy.
            links = restaurant.select('#divInspectionSearchResultsListing a')

            # If there are more than 0 links, let's do this.
            if len(links) > 0:

                # Loop over them.
                for link in links:
                    this_date = parse(link.text.split(':')[1].strip(), ignoretz=True)

                    eastern = timezone('US/Eastern')
                    this_date = eastern.localize(this_date)

                    if this_date > latest_inspection.time_in:

                        inspection_dict = {}
                        inspection_dict['restaurant'] = obj

                        # Get the inspection_id. These are (possibly?) unique.
                        inspection_dict['inspection_id'] = link['href'].split('../lib/mod/inspection/paper/_paper_food_inspection_report.cfm?inspectionID=')[1].split('&')[0]

                        # Construct the inspection detail URL from the inspection_id.
                        inspection_dict['inspection_url'] = "http://washington.dc.gegov.com/webadmin/dhd_431/lib/mod/inspection/paper/_paper_food_inspection_report.cfm?wguid=1367&wgunm=sysact&wgdmn=431&inspectionID=%s" % inspection_dict['inspection_id']

                        inspection_scrape_list.append(inspection_dict)

        except IndexError:
            # Some don't even have titles.
            # They don't count.
            pass

        except Restaurant.DoesNotExist:
            # A restaurant not in the DB yet.
            # We'll come back to this.
            print '!'

    return inspection_scrape_list
