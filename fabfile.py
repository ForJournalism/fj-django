from fabric.api import *

import data

def scrape_restaurants():
    data.scrape_restaurants()

def parse_restaurants():
    data.parse_restaurants()

def scrape_inspections():
	data.scrape_inspections()

def scrape_inspection_html():
	data.scrape_inspection_html()