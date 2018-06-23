# -*- coding: utf-8 -*-
"""
Created on Mon May 28 10:00:38 2018

@author: lauri.kangas
"""

from pathlib import Path
import datetime
import json
import skylines

def get_pilots(flights):
    a = set(flights[flight]['pilot'] for flight in flights if flights[flight]['pilot'] is not None)
    b = set(flights[flight]['copilot'] for flight in flights if flights[flight]['copilot'] is not None)
    return list(a.union(b))

def flights_by_pilot(flights, pilot):
    return {k: v for k, v in flights.items() if ((v['pilot'] == pilot or v['copilot'] == pilot) and v['plane'] in ['OH-952','OH-733','OH-883','OH-787','OH-650'])}

def visited_by_pilot(flights):
    pilots = get_pilots(flights)
    turned = {}
    for pilot in pilots:
        all_points = []
        pilot_flights = flights_by_pilot(flights, pilot)
        for flight in pilot_flights:
            all_points += pilot_flights[flight]['visited']
        turned[pilot] = sorted(list(set(all_points)))
        
    return turned
    

year = datetime.datetime.now().year
flights_file = Path(f'flights_{year}.txt')

with flights_file.open() as f:
    flights = json.load(f)
    
visited_points = visited_by_pilot(flights)
pilot_names = skylines.get_club_pilots()
visited_number = {k: len(v) for k, v in visited_points.items()}

for pilot_id in sorted(visited_number, key=visited_number.get, reverse=True):
    print(pilot_names[pilot_id], visited_number[pilot_id])
