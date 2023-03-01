#%%
import requests
import urllib
import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm
import folium 

# USGS Elevation Point Query Service
url = r'https://nationalmap.gov/epqs/pqs.php?'

CITIES_DATA_PATH = 'data/Cities.csv'
geolocator = Nominatim(user_agent = 'march-madness-experiment')


def elevation_function(df, lat_column, lon_column):
    """Query service using lat, lon. add the elevation values as a new column."""
    elevations = []
    for lat, lon in zip(df[lat_column], df[lon_column]):

        # define rest query params
        params = {
            'output': 'json',
            'x': lon,
            'y': lat,
            'units': 'Meters'
        }

        # format query string and return query value
        result = requests.get((url + urllib.parse.urlencode(params)))
        elevations.append(result.json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation'])

    df['elev_meters'] = elevations


#%%

cities_df = pd.read_csv(CITIES_DATA_PATH)
# %%
cities_df.head(5)
# %%
cities_df['full_name'] = cities_df['City'] + ', ' + cities_df['State'] + ', U.S.'
# %%

coordinates = []
for city in tqdm(cities_df['full_name'].values):
    try:
        location = geolocator.geocode(city)

        city_coordinates = (location.latitude, location.longitude)
        coordinates.append(city_coordinates)
    except:
        coordinates.append(None)

# %%
cities_df['coordinates'] = coordinates
# %%
cities_df.coordinates.isna().value_counts()
# %%
us_map = folium.Map(location=[48, -102], zoom_start=3)
# %%
# Check whether cities are indeed in the us; 
for city_coords in cities_df.coordinates.values:
    try:
        latitude, longitude = city_coords
        folium.Marker([latitude, longitude]).add_to(us_map)
    except:
        print(city_coords)
# %%
us_map
# %%
