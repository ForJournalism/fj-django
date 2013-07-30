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

def parse_inspection_html():
	data.parse_inspection_html(inspection_list=None)

def scrape_latest_inspections():
	inspection_list = data.scrape_latest_inspections()
	data.parse_inspection_html(inspection_list=inspection_list)
