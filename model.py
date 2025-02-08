import ast
import re
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
    exit()

# Function to safely convert lat_lon to tuple (split by semicolon)
def latlon_to_tuple(latlon_str):
    if not isinstance(latlon_str, str):
        return None

    try:
        lat_str, lon_str = latlon_str.split(';')
        lat = float(lat_str)
        lon = float(lon_str)
        return (lat, lon)
    except (ValueError, AttributeError):
        logging.error(f"Invalid latlon format: {latlon_str}")
        return None

# Convert lat_lon to tuples (landmarks)
landmarks['lat_lon'] = landmarks['lat_lon'].apply(latlon_to_tuple)
landmarks.dropna(subset=['lat_lon'], inplace=True)

# Convert gas station lat/lon to numeric (floats)
gas_stations['latlons'] = gas_stations['latlons'].apply(latlon_to_tuple)
gas_stations.dropna(subset=['latlons'], inplace=True)  # Drop rows with invalid coordinates

# 2. Download and Prepare Street Network
place = "Boston, Massachusetts, USA"
try:
    G = ox.graph_from_place(place, network_type="drive")
except Exception as e:
    logging.error(f"Error downloading street network: {e}")
    exit()

# Add 'travel_time' attribute
for u, v, k, data in G.edges(keys=True, data=True):
    length_meters = data['length']
    speed_kph = 40  # Example speed limit (adjust as needed)
    travel_time_seconds = (length_meters / (speed_kph * 1000 / 3600))
    G.edges[u, v, k]['travel_time'] = travel_time_seconds

# 3. Find Nearest Nodes and Calculate Distances/Times
def get_nearest_node_osmnx(graph, point):
    if point is None or any(np.isnan(point)):
        return None
    try:
        return ox.distance.nearest_nodes(graph, point[1], point[0])
    except Exception as e:
        logging.error(f"Error finding nearest node: {e} for point: {point}")
        return None

if landmarks.empty:
    logging.error("The landmarks DataFrame is empty. Check your data loading and preprocessing steps.")
    exit()

# Sample start and end points (using indices for consistent sample)
start_landmark_index = 0  # Example index, change as needed
end_landmark_index = 1    # Example index, change as needed

start_coords = landmarks['lat_lon'].iloc[start_landmark_index]
end_coords = landmarks['lat_lon'].iloc[end_landmark_index]

start_node = get_nearest_node_osmnx(G, start_coords)
end_node = get_nearest_node_osmnx(G, end_coords)

if start_node is None or end_node is None:
    logging.error("Could not find nearest nodes for start or end coordinates.")
    exit()

# Calculate distances and times to gas stations
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
                print("No path found between nodes. Skipping gas station.")
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

end_time = time.time()
logging.info(f"Data loading and preprocessing complete. Time taken: {end_time - start_time:.2f} seconds")

# 4. Feature Scaling, Model Training, Evaluation
if gas_stations.empty:
    logging.error("Gas stations dataframe is empty after processing")
    exit()

scaler = StandardScaler()
X = gas_stations[['added_mileage', 'added_time', 'price_per_gallon']]
y = gas_stations['price_per_gallon']  # Or another relevant target variable

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

# 7. Make Predictions on New Data (Example)
start_time = time.time()
logging.info("Starting predictions on new data...")

# Create new data (make sure the column names match your training data)
new_data = pd.DataFrame({
    'added_mileage': [15, 25, 10],  # Example values
    'added_time': [8, 12, 5],      # Example values
    'price_per_gallon': [4.5, 4.2, 4.7] # Example values
})

# Scale the new data using the SAME scaler that was fit on the training data
new_data_scaled = scaler.transform(new_data)

# Make predictions
predictions = best_model.predict(new_data_scaled)
print(f"Predictions: {predictions}")

end_time = time.time()
logging.info(f"Predictions on new data complete. Time taken: {end_time - start_time:.2f} seconds")


# 8. Finding the Optimal Gas Station (Example)

# Assuming you want to find the best gas station from the new_data DataFrame:
best_station_index = np.argmin(predictions)  # Index of the minimum predicted price
best_station = new_data.iloc[best_station_index]

print("\nOptimal Gas Station (based on lowest predicted price):")
print(best_station)

# Or, if you want to find the best gas station from the original gas_stations DataFrame
# based on the model's predictions:

# Scale the original gas_stations data
gas_stations_scaled = scaler.transform(gas_stations[['added_mileage', 'added_time', 'price_per_gallon']])
gas_station_predictions = best_model.predict(gas_stations_scaled)

best_gas_station_index = np.argmin(gas_station_predictions)
best_gas_station = gas_stations.iloc[best_gas_station_index]

print("\nOptimal Gas Station (from original data, based on model predictions):")
print(best_gas_station)

# 9. Saving the Model (Optional)
import joblib  # For saving models

model_filename = "gas_station_model.pkl"  # Choose a filename
joblib.dump(best_model, model_filename)
logging.info(f"Model saved to {model_filename}")