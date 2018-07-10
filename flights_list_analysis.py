# -*- coding: utf-8 -*-
"""
Created on Mon May 28 10:00:38 2018

@author: lauri.kangas
"""

from pathlib import Path
import datetime
import json
import skylines
import shutil

PIK_planes = ['OH-952','OH-733','OH-883','OH-787','OH-650']

def get_pilots(flights):
    a = set(flights[flight]['pilot'] for flight in flights if flights[flight]['pilot'] is not None)
    b = set(flights[flight]['copilot'] for flight in flights if flights[flight]['copilot'] is not None)
    return list(a.union(b))

def flights_by_pilot(flights, pilot):
    return {k: v for k, v in flights.items() if ((v['pilot'] == pilot or v['copilot'] == pilot) and v['plane'] in PIK_planes)}

def earliest_visited(pilot_flights, turnpoint):
    return min([pilot_flights[flight_id]['date'] for flight_id in pilot_flights if turnpoint in pilot_flights[flight_id]['visited']])

def visited_by_pilot(flights):
    pilots = get_pilots(flights)
    turned_with_dates = {}
    for pilot in pilots:
        all_points = []
        pilot_flights = flights_by_pilot(flights, pilot)
        for flight in pilot_flights:
            visited = pilot_flights[flight]['visited']
            all_points += visited
                
        unique_points = sorted(list(set(all_points)))
        turned_with_dates[pilot] = {point: earliest_visited(pilot_flights, point) for point in unique_points}
    return turned_with_dates

script_dir = Path(__file__).resolve().parent
year = datetime.datetime.now().year
flights_file = script_dir / f'flights_{year}.txt'

with flights_file.open() as f:
    flights = json.load(f)
    
visited_with_dates = visited_by_pilot(flights)

visits_filename = f'pilot_turnpoint_visits_{year}.txt'
visits_file = script_dir / visits_filename

json_string = json.dumps(visited_with_dates)
visits_file.write_text(json_string)


contest_dir = Path.home() / 'www' / 'kaannepistekisa2018'
shutil.copy(visits_file, contest_dir / visits_file.name)

js_string = f"visits = {json_string};"
(contest_dir / visits_file.with_suffix('.js').name).write_text(js_string)


visited_number = {k: len(v) for k, v in visited_with_dates.items()}
pilot_names = skylines.get_club_pilots()
for pilot_id in sorted(visited_number, key=visited_number.get, reverse=True):
    print(pilot_names[pilot_id], visited_number[pilot_id])
