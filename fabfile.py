from fabric.api import *

import data

def scrape_inspections():
    data.scrape_inspections()

def parse_inspections():
    data.parse_inspections()