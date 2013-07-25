#!/usr/bin/env python

import json

from bs4 import BeautifulSoup
import requests

def clean_text(string):
    """
    Remove breaks and tabs.
    Add other characters as necessary.
    """
    for char in ['\r', '\n', '\t']:
        string = string.replace(char, '')
    return string

def scrape_restaurants():
    """
    Scrapes list of restaurant inspections to a file.
    Index page is very slow to load.
    """
    data = {}
    data['a'] = 'Inspections'
    data['inputEstabName'] = ''
    data['inputPermitType'] = 'ANY'
    data['inputInspType'] = 'ANY'
    data['inputWard'] = 'ANY'
    data['inputQuad'] = 'ANY'
    data['btnSearch'] = 'Search'

    url = 'http://washington.dc.gegov.com/webadmin/dhd_431/web/index.cfm'

    r = requests.post(url, data=data)

    with open('data/restaurant_list.html', 'w') as htmlfile:
        htmlfile.write(r.content)


def parse_restaurants():
    """
    Parses the DC restaurant inspections list page.
    Will read from local file instead of fetching via requests.
    """
    with open('data/restaurant_list.html', 'r') as htmlfile:
        soup = BeautifulSoup(htmlfile.read())

    restaurants = []
    restaurant_list = soup.select('#divInspectionSearchResults > ul > li')

    for i, restaurant in enumerate(restaurant_list):
        try:
            if restaurant.select('h3 a')[0].text.title().replace("'S", "'s").strip() != '':
                restaurant_dict = {}

                restaurant_dict['title'] = restaurant.select('h3 a')[0].text.strip()
                restaurant_dict['permit_id'] = int(restaurant.select('h3 a')[0]['href'].split('permitID=')[1].strip())
                restaurant_dict['inspection_url'] = 'http://washington.dc.gegov.com/webadmin/dhd_431/web/index.cfm?a=inspections&permitID=%s' % restaurant_dict['permit_id']
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

                if restaurant_dict['type'] in ['Restaurant Total', 'Delicatessen']:
                    restaurants.append(restaurant_dict)
                    print '%s\t%s' % (i, restaurant_dict['title'])

            else:
                pass

        except IndexError:
            pass

    with open('data/restaurant_list.json', 'wb') as jsonfile:
        jsonfile.write(json.dumps(restaurants))

def scrape_inspections():
    """
    Reads from the restaurant list.
    Gets links to individual inspection pages.
    """
    inspections = []
    errors = []

    with open('data/restaurant_list.json', 'rb') as jsonfile:
        restaurants = json.loads(jsonfile.read())

    for i, restaurant in enumerate(restaurants):
        r = requests.get(restaurant['inspection_url'])
        soup = BeautifulSoup(r.content)
        for link in soup.select('#divInspectionSearchResultsListing a'):
            try:
                inspection_dict = {}
                inspection_dict['restaurant'] = restaurant
                inspection_dict['inspection_id'] = link['href'].split('../lib/mod/inspection/paper/_paper_food_inspection_report.cfm?inspectionID=')[1].split('&')[0]
                inspection_dict['inspection_url'] = "http://washington.dc.gegov.com/webadmin/dhd_431/lib/mod/inspection/paper/_paper_food_inspection_report.cfm?wguid=1367&wgunm=sysact&wgdmn=431&inspectionID=%s" % inspection_dict['inspection_id']
                print '%s\t%s: %s' % (i, inspection_dict['restaurant']['title'], inspection_dict['inspection_id'])
                inspections.append(inspection_dict)

            except IndexError:
                errors.append({'link_url': link['href'], 'restaurant': restaurant})

    with open('data/inspection_scrape_list.json', 'wb') as jsonfile:
        jsonfile.write(json.dumps(inspections))

    if len(errors) > 0:
        with open('data/inspection_scrape_errors.json', 'wb') as jsonfile:
            jsonfile.write(json.dumps(errors))

def scrape_inspection_html():
    """
    Reads from the inspection_scrape_list.
    Grabs inspection detail page.
    Writes it to HTML file in data/inspections.
    """
    with open('data/inspection_scrape_list.json', 'rb') as jsonfile:
        inspections = json.loads(jsonfile.read())

    for i, inspection in enumerate(inspections):
        r = requests.get(inspection['inspection_url'])

        with open('data/inspections/%s-%s.html' % (inspection['restaurant']['permit_id'], inspection['inspection_id']), 'wb') as htmlfile:
            htmlfile.write(r.content)
        
        print i, inspection['inspection_id']

def parse_inspection_html():
    """
    Reads from the inspection_scrape_list.
    Reads each inspection detail page in data/inspections.
    Parses the HTML.
    Writes to inspection_list.html.
    """
    with open('data/inspection_scrape_list.json', 'rb') as jsonfile:
        inspections = json.loads(jsonfile.read())

    updated_inspections = []

    for i, inspection in enumerate(inspections):
        with open('data/inspections/%s-%s.html' % (inspection['restaurant']['permit_id'], inspection['inspection_id']), 'rb') as htmlfile:
            soup = BeautifulSoup(htmlfile.read())
        inspection_dict = {}
        inspection_dict['type'] = soup.select('div.container > div')[16].text.strip()

        for j, z in enumerate(soup.select('div.checkboxRedN')):
            if z['style'].split('height:5px;width:5px;background-color:')[1].split(';')[0] == '#FF0000':
                inspection_dict['risk_category'] = j + 1

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

        inspection_dict['critical'] = crit
        inspection_dict['critical_corrected_on_site'] = cos
        inspection_dict['noncritical'] = ncrit
        inspection_dict['noncritical_corrected_on_site'] = ncos
        inspection_dict['observations'] = []

        if len(soup.select('table.fs_10px tr')) > 1:
            for z in soup.select('table.fs_10px tr')[1:]:
                if len(z.select('td')[0].text.split()) > 0:
                    try:
                        observations_dict = {}
                        observations_dict['observation'] = clean_text(z.select('td')[0].text.strip())
                        observations_dict['dcmr'] = clean_text(z.select('td')[1].text.strip())
                        observations_dict['correction'] = clean_text(z.select('td')[2].text.strip())
                        inspection_dict['observations'].append(observations_dict)
                    except IndexError:
                        # There's an exception where they describe the type of sanitizer.
                        # There's nothing more unholy than government tables.
                        pass

        inspection = dict(inspection, **inspection_dict)
        updated_inspections.append(inspection)

        print i, inspection['inspection_id']

    with open('data/inspection_list.json', 'wb') as jsonfile:
        jsonfile.write(json.dumps(updated_inspections))

def insert_restaurants():
    """
    Reads restaurant_list.json.
    Inserts restaurants into the database.
    """
    with open('data/restaurant_list.json', 'rb') as jsonfile:
        restaurants = json.loads(jsonfile.read())

    for i, restaurant in enumerate(restaurants):
        print i, restaurant['title']

def insert_inspections():
    """
    Reads inspection_list.json.
    Inserts inspections, observations into the database.
    """
    with open('data/inspection_list.json', 'rb') as jsonfile:
        inspections = json.loads(jsonfile.read())

    for i, inspection in enumerate(inspections):
        print i, inspection['inspection_id']
