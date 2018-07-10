# -*- coding: utf-8 -*-
"""
Created on Wed May 23 20:56:54 2018

@author: vostok
"""

import skylines
import turnpoint
import requests
from pathlib import Path
import json
import shutil

script_dir = Path(__file__).resolve().parent
cupname = 'finland_2014.cup'
cupfile = script_dir / cupname
year = 2018
flights_file = script_dir / f'flights_{year}.txt'
existing_flights = dict()

if flights_file.exists():
    with flights_file.open() as f:
        existing_flights = json.loads(f.read())
        

all_turnpoints = turnpoint.read_cup(cupfile)

print("getting flights")
skylines_flights = skylines.get_flights(year)
print("got flights")

new_flights = dict()

for flight in skylines_flights:
    if str(flight['id']) in existing_flights:
        print('skipping', flight['id'])
        continue
    
    print(f"flight {flight['id']}")
    flight_data = dict()
    
    flight_data['date'] = flight['scoreDate']
    
    try:
        flight_data['pilot'] = flight['pilot']['id']
    except TypeError:
        flight_data['pilot'] = None
    
    try:
        flight_data['copilot'] = flight['copilot']['id']
    except TypeError:
        flight_data['copilot'] = None
    
    flight_data['plane'] = flight['registration']
    
    igc_filename = flight['igcFile']['filename']
    url = skylines.skylines_igc_url(igc_filename)
    r = requests.get(url)
    
    track = turnpoint.read_igc(content=r.text)
    visited = turnpoint.turnpoints_in_track(track, all_turnpoints)
    
    flight_data['visited'] = visited
    
    new_flights[str(flight['id'])] = flight_data

combined_flights = {**existing_flights, **new_flights}
with flights_file.open('w') as f:
    json.dump(combined_flights, f)

contest_dir = Path.home() / 'www' / 'kaannepistekisa2018'

js_string = f"flights = {json.dumps(combined_flights)};"

(contest_dir / flights_file.with_suffix('.js').name).write_text(js_string)

