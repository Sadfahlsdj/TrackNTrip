import osmnx as ox
import networkx as nx
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from geopy.geocoders import Nominatim
import time
import logging
import cProfile
import psutil
from sklearn.metrics import r2_score, mean_squared_error

# Configure logging
logging.basicConfig(filename='gas_station_optimization.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Data Loading and Preprocessing
start_time = time.time()
logging.info("Starting data loading and preprocessing...")

try:
    landmarks = pd.read_csv("landmarks_data/landmarks_boston_cleaned.csv")
    gas_stations = pd.read_csv("gas_station_data/boston_gas_stations.csv")
except FileNotFoundError as e:
    logging.error(f"Error loading CSV files: {e}. Make sure the files exist in the correct directory.")
    exit()  # Exit the script if files are not found

# Geocoding if addresses are present (if lat/lon is not available in gas_stations)
geolocator = Nominatim(user_agent="gas_station_app")

def get_coordinates(location_str):
    try:
        location = geolocator.geocode(location_str)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        logging.error(f"Geocoding error: {e}")
        return None

# Convert lat_lon to tuples if they're strings (landmarks)
landmarks['lat_lon'] = landmarks['lat_lon'].apply(eval)


# 2. Download and Prepare Street Network
place = "Boston, Massachusetts, USA"  # Or a more specific area
try:
    G = ox.graph_from_place(place, network_type="drive")
except Exception as e:
    logging.error(f"Error downloading street network: {e}")
    exit()

# Add 'travel_time' attribute (important for realistic times)
for u, v, k, data in G.edges(keys=True, data=True):
    length_meters = data['length']
    speed_kph = 40  # Example speed limit (adjust as needed)
    travel_time_seconds = (length_meters / (speed_kph * 1000 / 3600))
    G.edges[u, v, k]['travel_time'] = travel_time_seconds

# 3. Find Nearest Nodes and Calculate Distances/Times
def get_nearest_node_osmnx(graph, point):
    try:
        return ox.distance.nearest_nodes(graph, point[1], point[0])  # osmnx uses (y,x)
    except Exception as e:
        print(f"Error finding nearest node: {e}")
        return None

# Sample start and end points
start_landmark = landmarks.sample(1)
end_landmark = landmarks.sample(1)

start_coords = start_landmark['lat_lon'].iloc[0]
end_coords = end_landmark['lat_lon'].iloc[0]

start_node = get_nearest_node_osmnx(G, start_coords)
end_node = get_nearest_node_osmnx(G, end_coords)

distances = []
times = []
for index, station in gas_stations.iterrows():
    if 'latitude' in gas_stations.columns and 'longitude' in gas_stations.columns:
        gas_station_coords = (station['latitude'], station['longitude'])
    else:
        gas_station_coords = get_coordinates(station['address'])

    if gas_station_coords:
        gas_station_node = get_nearest_node_osmnx(G, gas_station_coords)

        if start_node and end_node and gas_station_node:
            try:
                dist_to_station = nx.shortest_path_length(G, start_node, gas_station_node, weight='length')
                dist_from_station = nx.shortest_path_length(G, gas_station_node, end_node, weight='length')
                time_to_station = nx.shortest_path_length(G, start_node, gas_station_node, weight='travel_time')
                time_from_station = nx.shortest_path_length(G, gas_station_node, end_node, weight='travel_time')

                distances.append(dist_to_station + dist_from_station)
                times.append(time_to_station + time_from_station)
            except nx.NetworkXNoPath:
                print("No path found between nodes. Skipping gas station.")
                distances.append(np.nan)
                times.append(np.nan)
        else:
            distances.append(np.nan)
            times.append(np.nan)
    else:
        distances.append(np.nan)
        times.append(np.nan)

gas_stations['added_mileage'] = distances
gas_stations['added_time'] = times

gas_stations.dropna(inplace=True)  # Remove rows with NaN values

end_time = time.time()
logging.info(f"Data loading and preprocessing complete. Time taken: {end_time - start_time:.2f} seconds")

# 4. Feature Scaling, Model Training, Evaluation
scaler = StandardScaler()
X = gas_stations[['added_mileage', 'added_time', 'price']]
y = gas_stations['price']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# 5. Hyperparameter Tuning and Model Training
start_time = time.time()
logging.info("Starting hyperparameter tuning and model training...")

param_grid = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None]
}

random_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    n_iter=10,  # Reduced for faster execution in this example
    cv=3,
    scoring='r2',
    n_jobs=-1,
    verbose=0,
    random_state=42
)

random_search.fit(X_train_scaled, y_train)

best_model = random_search.best_estimator_
print(f"Best Hyperparameters: {random_search.best_params_}")

end_time = time.time()
logging.info(f"Hyperparameter tuning and model training complete. Time taken: {end_time - start_time:.2f} seconds")


# 6. Model Evaluation
start_time = time.time()
logging.info("Starting model evaluation...")

y_pred = best_model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"R-squared score (on test set): {r2}")
print(f"Mean Squared Error (on test set): {mse}")
print(f"Root Mean Squared Error (on test set): {rmse}")

end_time = time.time()
logging.info(f"Model evaluation complete. Time taken: {end_time - start_time:.2f} seconds")

# 7. Make Predictions on New Data
start_time = time.time()
logging.info("Starting predictions on new data...")

new_data = pd.DataFrame({
    'added_mileage': [10,20],  # Example new data
    'added_time': [5,10],
    'price': [4,5]
})

new_data_scaled = scaler.transform(new_data)  # Important: Use the same scaler
predictions = best_model.predict(new_data_scaled)
print(f"Predictions: {predictions}")

end_time = time.time()
logging.info(f"Predictions on new data complete). Time taken: {end_time - start_time:.2f} seconds")