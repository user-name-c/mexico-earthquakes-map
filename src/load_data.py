import requests
import pandas as pd

def fetch_mexico_earthquakes():
    # URL with parameters for Mexico (Approximate Bounding Box)
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": "2026-02-15", # You can use datetime.now() for dynamism
        "minlatitude": 14.0,
        "maxlatitude": 33.0,
        "minlongitude": -118.0,
        "maxlongitude": -86.0,
        "minmagnitude": 2.5
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract features
    events = []
    for feature in data['features']:
        coords = feature['geometry']['coordinates']
        prop = feature['properties']
        events.append({
            'date': pd.to_datetime(prop['time'], unit='ms'),
            'latitude': coords[1],
            'longitude': coords[0],
            'depth': coords[2],
            'magnitude': prop['mag'],
            'place': prop['place']
        })
    
    df = pd.DataFrame(events)
    return df

# Save to CSV as backup for the exploration notebook
df_sismos = fetch_mexico_earthquakes()
df_sismos.to_csv('../data/earthquakes.csv', index=False)