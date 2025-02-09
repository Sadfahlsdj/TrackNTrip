from flask import Flask, request, jsonify
import pandas as pd
from run_model import return_best_stations
from geopy import Nominatim
from geopy.geocoders import OpenCage
import osmnx as ox
import numpy as np
import networkx as nx
import os
import pickle
import time

app = Flask(__name__)

@app.get('/info')
def get_info():
    """
    api arguments:
        city - city name (only supports boston right now)
        landmark - name of landmark (needs to match case insensitive exactly for now)

    :return: json with date, description, latitude longitude data, address

    example usage: http://127.0.0.1:5000/info?city=boston&landmark=African%20Meeting%20House
    """
    city = request.args.get('city').lower()
    landmark = request.args.get('landmark').lower()

    path = f'landmarks_data/landmarks_{city}_cleaned.csv'
    df = pd.read_csv(path)
    out = df[df['name'] == landmark][['Date', 'Description', 'lat_lon', 'address']]

    return out.to_json(orient='records')

@app.get('/keyword')
def get_landmark_by_keyword():
    """
    api arguments:
        city - city name (only supports boston right now)
        keyword - keyword to search

    :return: name of every landmark which contains the keyword in its description
    sample usage: http://127.0.0.1:5000/keyword?city=boston&keyword=church
    """
    keyword = request.args.get('keyword').lower()
    city = request.args.get('city').lower()

    path = f'landmarks_data/landmarks_{city}_cleaned.csv'
    df = pd.read_csv(path)

    out = df[df['Description'].str.contains(keyword, case=False)]['name']
    return out.to_json(orient='records')

@app.get('/stations')
def get_stations():
    """
    api arguments:
        city - city name (only supports boston right now)
        type - either gas or electric
        start - lat/lon of start of trip
        end - lat/lon of end of trip

    :return: top 5 gas stations along the path as gotten by model
    sample usage (ALL ONE LINE):
    http://127.0.0.1:5000/stations?city=boston&type=gas
    &start=42.36;71.06555555555555&end=42.358333333333334;71.06194444444444
    """

    start = request.args.get('start').lower()
    start_coords = (float(start.split(';')[0]), float(start.split(';')[1]))
    end = request.args.get('end').lower()
    end_coords = (float(end.split(';')[0]), float(end.split(';')[1]))
    city = request.args.get('city').lower()
    type = request.args.get('type').lower()

    path = f'gas_station_data/{city}_{type}_stations.csv'

    out = return_best_stations(start_coords, end_coords, path)
    return out.to_json(orient='records')
    # pass in start lat/lon and end lat/lon to ML function here, and return results

@app.get('/coords')
def get_coords():
    """
    api arguments:
        address: full address of location; should be formatted as Address City State if possible
        example: 5315 Washington St West Roxbury, MA
            (comma is optional)
            adding city/state is not strictly necessary but greatly increases success rate

    :return: json with one field coords which is in the format "lat;long"

    example usage: http://127.0.0.1:5000/coords?address=8%20Smith%20Ct%20Beacon%20Hill
    """
    address = request.args.get('address').lower()
    user_agent = "HBP_2025/1.0 (wilsar964@gmail.com)"
    geolocator = Nominatim(user_agent=user_agent)
    try:
        l = geolocator.geocode(address)
    except:
        print(f'nominatim is dead, using opencage')
        api_key = '25dadb1d0d3d4d57ae50cbc1f1b829d2' # free version on a burner gmail i don't care

        geolocator = OpenCage(api_key=api_key)
        time.sleep(1)
        l = geolocator.geocode(address)

    if l is not None:
        out = {'coords': f'{l.latitude};{l.longitude}'}
        return jsonify(out)

    return 'address not found'

def get_nearest_node_osmnx(graph, point):
    """
    helper function for /distance endpoint
    :param graph: OSMnx graph
    :param point: lat/long tuple to test
    :return:
    """
    if point is None or any(np.isnan(point)):
        return None
    try:
        return ox.distance.nearest_nodes(graph, point[1], point[0])
    except Exception as e:
        return None
@app.get('/distance')
def get_distance():
    """
    api args:
        start - coordinates of start in the format lat;lon
        end - coordinates of end in the format lat;lon
        location - location to generate map around
            stick to cities for now, states and larger take a LONG time to generate
    :return: json with 1 field distance_miles which shows the shortest driving distance between the 2

    example usage (ONE LINE ONLY):
    http://127.0.0.1:5000/distance?start=42.36;-71.06555555555555
    &end=42.356944444444444;-71.0663888888&location=Boston
    """
    start = request.args.get('start').lower()
    end = request.args.get('end').lower()
    location = request.args.get('location').lower()

    start_coords = (float(start.split(';')[0]), float(start.split(';')[1]))
    end_coords = (float(end.split(';')[0]), float(end.split(';')[1]))

    try:
        os.mkdir('city_map_pickles')
    except:
        pass

    place = location
    try:
        if os.path.exists(f'city_map_pickles/{location}'):
            with open(f'city_map_pickles/{location}', 'rb') as f:
                G = pickle.load(f)
        else:
            G = ox.graph_from_place(place, network_type="drive")
            with open(f'city_map_pickles/{location}', 'ab') as f:
                pickle.dump(G, f)
    except Exception as e:
        return 'could not make map'

    start_node = get_nearest_node_osmnx(G, start_coords)
    end_node = get_nearest_node_osmnx(G, end_coords)

    try:
        dist = nx.shortest_path_length(G, start_node, end_node) # returns a weird unit
        dist_converted = dist * 0.075 # rough conversion based on manual testing
        return(jsonify({'distance_miles': dist_converted}))
    except:
        return('no path found')

def separate_latlon(start): # helper function to separate our encoding of lat/lon
    # will go back and standardize functions to use this later
    return (float(start.split(';')[0]), float(start.split(';')[1]))

@app.get('/landmarks')
def find_landmarks():
    """
    api arguments:
        start: start lat/lon in the format lat;lon
        end: end lat/lon in a similar format
        city: which city to check (only boston for now)
    :return: all landmarks in a rectangle between the 2
    example usage: http://127.0.0.1:5000/landmarks?start=0;0&end=100;-100&city=boston
    """
    start = request.args.get('start').lower()
    end = request.args.get('end').lower()
    city = request.args.get('city').lower()

    start_coords = (float(start.split(';')[0]), float(start.split(';')[1]))
    end_coords = (float(end.split(';')[0]), float(end.split(';')[1]))

    max_lat, min_lat = max(start_coords[0], end_coords[0]), min(start_coords[0], end_coords[0])
    max_lon, min_lon = max(start_coords[1], end_coords[1]), min(start_coords[1], end_coords[1])

    df = pd.read_csv(f'landmarks_data/landmarks_{city}_cleaned.csv')
    out = pd.DataFrame(columns=df.columns)

    for i, row in df.iterrows():
        coords = separate_latlon(row['lat_lon'])
        # print(f'{min_lat}, {max_lat}')
        # print(f'{min_lon}, {max_lon}')

        if (min_lat < coords[0] < max_lat) and (min_lon < coords[1] < max_lon):
            out.loc[len(out)] = row

    return out.to_json(orient='records')


