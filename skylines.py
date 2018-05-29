# -*- coding: utf-8 -*-

import requests
from dateutil.parser import parse
from collections import defaultdict

def get_flights(target_year, club=345):
    url = f'https://skylines.aero/api/flights/club/{club}'
    params = {'column': 'date',
              'order': 'desc',
              'page': 1}
    cont = True
    flights = []
    
    while cont:
        r = requests.get(url, params=params)
        j = r.json()
        
        flights += j['flights']
        years = flights_years(j['flights'])
        
        if min(years) < target_year:
            break
        
        params['page'] += 1

    return select_flights(flights, year=target_year)

def flights_years(flights):
    return set(parse(flight['scoreDate']).year for flight in flights)

def select_flights(flights, year):
    return [f for f in flights if parse(f['scoreDate']).year == year]

def flights_pilots(flights):
    return list(set(f['pilot']['id'] for f in flights))

def get_pilot_igcs(flights):
    pilot_igcs = defaultdict(list)
    copilot_igcs = defaultdict(list)
    
    for flight in flights:
        try:
            pilot = flight['pilot']['id']
            pilot_igcs[pilot] += [flight['igcFile']['filename']]
        except TypeError:
            print(f"no pilot id for flight {flight['id']}")
        
        
        copilot = flight['copilot']
        if copilot:
            copilot = copilot['id']
            copilot_igcs[copilot] += [flight['igcFile']['filename']]
    
    return pilot_igcs, copilot_igcs

def get_flight_igc_data(url):
    flight_id = int(url.split('/')[-1])
    api_url = f'https://skylines.aero/api/flights/{flight_id}'
    r = requests.get(api_url)
    j = r.json()
    filename = j['flight']['igcFile']['filename']
    r = requests.get(skylines_igc_url(filename))
    return r.text
    
def skylines_igc_url(filename):
    return f'https://skylines.aero/files/{filename}'
    

def get_club_pilots(club=345):
    url = f'https://skylines.aero/api/users?club={club}'
    r = requests.get(url)
    j = r.json()
    d = {}
    for user in j['users']:
        d[user['id']] = user['name']
    return d
    



    
    