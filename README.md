# F1WinnerPredictions

# 🏎️ F1 Predictions 2025 - Machine Learning Model

Welcome to the **F1 Predictions 2025** repository! This project uses **machine learning, FastF1 API data, and historical F1 race results** to predict race outcomes for the 2025 Formula 1 season. This repository is called **F1WinnerPredictions**.

## 🚀 Project Overview

This repository contains a **machine learning model** that predicts race results based on past performance, qualifying times, and other structured F1 data. We are using a **Random Forest Regressor** for prediction. The model leverages:

- FastF1 API for historical race data
- 2024 race results
- 2025 qualifying session results
- Feature engineering techniques to improve predictions


## 📊 Data Sources

- **FastF1 API**: Fetches lap times, race results, and telemetry data.
- **2025 Qualifying Data**: Used for prediction.
- **Historical F1 Results (2024 Chinese GP)**: Processed from FastF1 for training the model.


## 🏁 How It Works

1. **Data Collection**: The script pulls relevant F1 data using the FastF1 API and creates a cache for faster access.
2. **Preprocessing & Feature Engineering**: Converts lap times to seconds, normalizes driver names using a mapping, and structures race data into a usable format. It combines qualifying and sector times as features.
3. **Model Training**: A **Random Forest Regressor** is trained using 2024 Chinese Grand Prix race results. We experimented with various models, including Gradient Boosting, K-Nearest Neighbors, and Random Forest, before selecting the best-performing model.
4. **Prediction**: The model predicts race times for the 2025 Chinese Grand Prix based on qualifying data and ranks drivers accordingly.
5. **Evaluation**: Model performance is measured using **Mean Absolute Error (MAE)**.


## 📦 Dependencies

- `fastf1`
- `numpy`
- `pandas`
- `scikit-learn`


## 🔧 Usage

1.  **Install Dependencies:**
2.  **Run the prediction script:**


## 📈 Model Performance

The model's performance is evaluated using Mean Absolute Error (MAE). The lower the MAE, the better the model's predictions.

The Random Forest Regressor model has been chosen for its superior performance and ability to handle complex relationships in the data.


## ✨ Future Improvements

- Incorporate more historical race data from previous seasons to enhance model accuracy.
- Explore additional features, such as driver standings, tyre strategies, and weather conditions.
- Implement hyperparameter tuning to optimize the model's performance further.
- Update predictions dynamically as the season progresses, reflecting real-time data.
- Extend predictions to include other races in the 2025 calendar.
