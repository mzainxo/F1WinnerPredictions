# -*- coding: utf-8 -*-
"""ChineseGP_F1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P9ERQfqrOyDNbGgZ0sjU8HyKlDu2EqnT
"""

pip install fastf1 pandas numpy scikit-learn

# Necessary imports
import os
import fastf1
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

# Define cache directory
cache_dir = "/content/f1_cache2"

# Create the directory
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Enable FastF1 caching
fastf1.Cache.enable_cache(cache_dir)
print("Cache enabled at:", cache_dir)

#Load Fast F1 2024 Chinese GP race session
session_2024 = fastf1.get_session(2024, "China", 'R')
session_2024.load()

session_2024.laps.info()

# Extract lap and sector times
laps_2024 = session_2024.laps[["Driver", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]].copy()
laps_2024.dropna(inplace=True)

# Convert times to seconds
for col in ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]:
    laps_2024[f"{col}Seconds"] = laps_2024[col].dt.total_seconds()

laps_2024.Driver.unique()

# Group by driver to get average sector times per driver
sector_times_2024 = laps_2024.groupby("Driver")[["Sector1TimeSeconds", "Sector2TimeSeconds", "Sector3TimeSeconds"]].mean().reset_index()

# 2025 Qualifying Data Chinese GP
qualifying_2025 = pd.DataFrame({
    "Driver": ["Oscar Piastri", "George Russell", "Lando Norris", "Max Verstappen", "Lewis Hamilton",
               "Charles Leclerc", "Yuki Tsunoda", "Alexander Albon","Esteban Ocon", "Nico Hülkenberg",
               "Fernando Alonso", "Lance Stroll", "Carlos Sainz", "Pierre Gasly"],
    "QualifyingSeconds": [90.641, 90.723, 90.793, 90.817, 90.927,
                           91.021, 91.638, 91.706, 91.625, 91.632,
                          91.688, 91.773, 91.840, 91.992]
})
qualifying_2025

# Map full names to FastF1 3-letter codes
driver_mapping = {
    "Oscar Piastri": "PIA", "George Russell": "RUS", "Lando Norris": "NOR", "Max Verstappen": "VER",
    "Lewis Hamilton": "HAM", "Charles Leclerc": "LEC", "Yuki Tsunoda": "TSU", "Alexander Albon": "ALB", "Esteban Ocon": "OCO",
    "Nico Hülkenberg": "HUL", "Fernando Alonso": "ALO", "Lance Stroll": "STR", "Carlos Sainz": "SAI", "Pierre Gasly": "GAS",
}

qualifying_2025["DriverCode"] = qualifying_2025["Driver"].map(driver_mapping)

# Merge 2025 qualifying data with 2024 race data
merged_data = qualifying_2025.merge(sector_times_2024, left_on="DriverCode", right_on="Driver", how="left")
merged_data.dropna(inplace=True)
merged_data

# Define feature set (Qualifying + Sector Times)
X = merged_data[["QualifyingSeconds", "Sector1TimeSeconds", "Sector2TimeSeconds", "Sector3TimeSeconds"]].fillna(0)
y = merged_data.merge(laps_2024.groupby("Driver")["LapTimeSeconds"].mean(), left_on="DriverCode", right_index=True)["LapTimeSeconds"]

# Train Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=38)

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.neighbors import KNeighborsRegressor

knn_model = KNeighborsRegressor(n_neighbors=5)  # Try different values for n_neighbors
knn_model.fit(X_train, y_train)
y_pred_knn = knn_model.predict(X_test)

# Train Gradient Boosting model
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=38)
model.fit(X_train, y_train)

# Train Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=38)
rf_model.fit(X_train, y_train)


# Make predictions with each model
y_pred_gb = model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)


# Evaluate each model
mae_knn = mean_absolute_error(y_test, y_pred_knn)
mae_gb = mean_absolute_error(y_test, y_pred_gb)
mae_rf = mean_absolute_error(y_test, y_pred_rf)


print("KNN MAE:", mae_knn)
print("Gradient Boosting MAE:", mae_gb)
print("Random Forest MAE:", mae_rf)

#dataset split
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

#Predict using 2025 qualifying times
predicted_race_times = rf_model.predict(X)
qualifying_2025["PredictedRaceTimeSeconds"] = predicted_race_times

# Rank drivers by predicted race time
qualifying_2025 = qualifying_2025.sort_values(by="PredictedRaceTimeSeconds")

# Final prediction
print("\nPREDICTED CHINESE GRAND PRIX 2025 WINNER\n")
qualifying_2025[["Driver","PredictedRaceTimeSeconds"]]

print("Gradient Boosting MAE:", mae_gb)
print("Random Forest MAE:", mae_rf)