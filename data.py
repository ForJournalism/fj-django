#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests


def scrape_inspections():
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

    with open('data/inspection_list.html', 'w') as htmlfile:
        htmlfile.write(r.content)


def parse_inspections():
    """
    Parses the DC restaurant inspections list page.
    Will read from local file instead of fetching via requests.
    """
    with open('data/inspection_list.html', 'r') as htmlfile:
        soup = BeautifulSoup(htmlfile.read())

    restaurant_list = soup.select('#divInspectionSearchResults > ul > li')

    for restaurant in restaurant_list:
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

                print restaurant_dict

            else:
                pass

        except IndexError:
            pass
