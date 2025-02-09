import ast
import re
import osmnx as ox
import networkx as nx
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from geopy.geocoders import Nominatim
import time
import logging
from sklearn.metrics import r2_score, mean_squared_error
import shap
import joblib

# Configure logging
logging.basicConfig(filename='gas_station_optimization_xgboost.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_composite_score(gas_stations, weights):
    # ... (same function as in the previous response) ...
    for col in weights:
        if col not in gas_stations.columns:
            raise ValueError(f"Column '{col}' not found in gas_stations DataFrame.")
        gas_stations[col] = gas_stations[col].fillna(gas_stations[col].mean())

    normalized_data = gas_stations[weights.keys()].copy()
    for col in weights:
        min_val = normalized_data[col].min()
        max_val = normalized_data[col].max()
        if max_val - min_val != 0:
            normalized_data[col] = (normalized_data[col] - min_val) / (max_val - min_val)
        else:
            normalized_data[col] = 0

    composite_score = np.zeros(len(gas_stations))
    for col, weight in weights.items():
        composite_score += normalized_data[col] * weight

    return pd.Series(composite_score, name="composite_score")

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

# 4. Feature Engineering and Composite Score Calculation
start_time = time.time()
logging.info("Starting feature engineering and composite score calculation...")

X = gas_stations[['added_mileage', 'added_time', 'price_per_gallon']]  # Original features

# --- Calculate Composite Score ---
weights = {
    'price_per_gallon': -0.4,  # Adjust weights as needed
    'added_mileage': -0.3,       # Shorter distance is better
    'added_time': -0.2          # Shorter time is better
}
gas_stations['composite_score'] = calculate_composite_score(gas_stations, weights)
y = gas_stations['composite_score'] # Target variable now composite score!

# --- Feature Scaling and Polynomial Features (on original X) ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_poly = poly.fit_transform(X)
poly_feature_names = poly.get_feature_names_out(X.columns)
X_poly = pd.DataFrame(X_poly, columns=poly_feature_names)

# Train-test split (using X_poly)
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

end_time = time.time()
logging.info(f"Feature engineering and composite score calculation complete. Time taken: {end_time - start_time:.2f} seconds")

# 5. Hyperparameter Tuning and Model Training (XGBoost)
start_time = time.time()
logging.info("Starting hyperparameter tuning and model training with XGBoost...")

# 6. Model Training and Evaluation
param_grid = {
    'n_estimators': 317,
    'max_depth': 4,
    'learning_rate': 0.05,
    'subsample': 0.9,
    'colsample_bytree': 0.78,
    'gamma': 0.00021,
    'reg_alpha': 0.1512,
    'reg_lambda': 0.4245 
}

model = XGBRegressor(**param_grid, random_state=42)
model.fit(X_train, y_train) # No need for GridSearchCV

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"R-squared score (on test set): {r2}")
print(f"Mean Squared Error (on test set): {mse}")
print(f"Root Mean Squared Error (on test set): {rmse}")

# 8. SHAP Analysis
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Save SHAP values to a file
shap_values_file = "shap_values.npy"
np.save(shap_values_file, shap_values)

# shap.summary_plot(shap_values, X_test, feature_names=poly_feature_names)
# shap.summary_plot(shap_values, X_test, feature_names=poly_feature_names, plot_type="bar")

X_poly_all = poly.transform(X) # Use the same polynomial features as training
predictions = model.predict(X_poly_all)

# 2. Create a DataFrame with Predictions and Original Data
results_df = gas_stations.copy() # Create a copy to avoid SettingWithCopyWarning
results_df['predicted_composite_score'] = predictions

# 3. Sort by Predicted Score (Descending)
results_df_sorted = results_df.sort_values(by='predicted_composite_score', ascending=False)

# 4. Print the Top 5
top_5_results = results_df_sorted.head(5)
print("Top 5 Gas Stations (Ranked by Predicted Composite Score):")
print(top_5_results)

# Save the model
joblib.dump(model, 'xgboost_gas_station_model.pkl')