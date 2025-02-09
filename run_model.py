import joblib
import pandas as pd
import osmnx as ox
import numpy as np
import networkx as nx
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
import os
import pickle

def latlon_to_tuple(latlon_str):
    if not isinstance(latlon_str, str):
        return None
    try:
        lat_str, lon_str = latlon_str.split(';')
        lat = float(lat_str)
        lon = float(lon_str)
        return (lat, lon)
    except (ValueError, AttributeError):
        return None
def get_nearest_node_osmnx(graph, point):
    if point is None or any(np.isnan(point)):
        return None
    try:
        return ox.distance.nearest_nodes(graph, point[1], point[0])
    except Exception as e:
        return None
def return_best_stations(start_coords, end_coords, csv_name):
    """

    :param start_coords: tuple of (lat, lon) of start coords
    :param end_coords: tuple of (lat, lon) of end coords
    :param csv_name: name of relevant csv file
    :return: best gas stations along path from start_coords to end_coords
    """
    model_file = "xgboost_gas_station_model.pkl"
    model = joblib.load(model_file)

    gas_stations = pd.read_csv(csv_name)
    gas_stations['latlons'] = gas_stations['latlons'].apply(latlon_to_tuple)
    gas_stations.dropna(subset=['latlons'], inplace=True)  # Drop rows with invalid coordinates

    place = 'boston' # hardcoded for now
    try:
        os.mkdir('city_map_pickles')
    except:
        pass
    try:
        if os.path.exists(f'city_map_pickles/{place}'):
            with open(f'city_map_pickles/{place}', 'rb') as f:
                G = pickle.load(f)
        else:
            G = ox.graph_from_place(place, network_type="drive")
            with open(f'city_map_pickles/{place}', 'ab') as f:
                pickle.dump(G, f)
    except Exception as e:
        exit()

    for u, v, k, data in G.edges(keys=True, data=True):
        length_meters = data['length']
        speed_kph = 40  # Example speed limit (adjust as needed)
        travel_time_seconds = (length_meters / (speed_kph * 1000 / 3600))
        G.edges[u, v, k]['travel_time'] = travel_time_seconds

    start_node = get_nearest_node_osmnx(G, start_coords)
    end_node = get_nearest_node_osmnx(G, end_coords)

    if start_node is None or end_node is None:
        exit()

    distances = []
    times = []
    price_per_station = []

    for index, station in gas_stations.iterrows():
        gas_station_coords = (station['latlons'][0], station['latlons'][1])

        if gas_station_coords and not any(np.isnan(gas_station_coords)):
            gas_station_node = get_nearest_node_osmnx(G, gas_station_coords)

            if gas_station_node:
                try:
                    dist_to_station = nx.shortest_path_length(G, start_node, gas_station_node, weight='length')
                    dist_from_station = nx.shortest_path_length(G, gas_station_node, end_node, weight='length')
                    time_to_station = nx.shortest_path_length(G, start_node, gas_station_node, weight='travel_time')
                    time_from_station = nx.shortest_path_length(G, gas_station_node, end_node, weight='travel_time')

                    distances.append(dist_to_station + dist_from_station)
                    times.append(time_to_station + time_from_station)
                    price_per_station.append(station['price'])
                except nx.NetworkXNoPath:
                    # print("No path found between nodes. Skipping gas station.")
                    distances.append(np.nan)
                    times.append(np.nan)
                    price_per_station.append(np.nan)
            else:
                distances.append(np.nan)
                times.append(np.nan)
                price_per_station.append(np.nan)
        else:
            distances.append(np.nan)
            times.append(np.nan)
            price_per_station.append(np.nan)

    gas_stations['added_mileage'] = distances
    gas_stations['added_time'] = times
    gas_stations['price_per_gallon'] = price_per_station

    gas_stations.dropna(inplace=True)
    X = gas_stations[['added_mileage', 'added_time', 'price_per_gallon']]  # Original features

    poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    X_poly = poly.fit_transform(X)
    X_poly_all = poly.transform(X)  # Use the same polynomial features as training
    predictions = model.predict(X_poly_all)

    # 2. Create a DataFrame with Predictions and Original Data
    results_df = gas_stations.copy()  # Create a copy to avoid SettingWithCopyWarning
    results_df['predicted_composite_score'] = predictions

    # 3. Sort by Predicted Score (Descending)
    results_df_sorted = results_df.sort_values(by='predicted_composite_score', ascending=False)

    # 4. Print the Top 5
    top_5_results = results_df_sorted.head(5)
    # print("Top 5 Gas Stations (Ranked by Predicted Composite Score):")
    return top_5_results[['name', 'address', 'latlons', 'price', 'price_per_gallon']]

def main():
    print(return_best_stations((42.000, 71.000), (42.010, 71.000),
                     'gas_station_data/boston_gas_stations.csv').to_string())

if __name__ == '__main__':
    main()


