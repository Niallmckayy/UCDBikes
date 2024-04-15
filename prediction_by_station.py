import pandas as pd
import requests
import json
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pickle


APIKey = 'a155d66d86bdd268b15c6488321141e9'
lat = '53.3498'
lon = '6.2603'

def get_forecast_data():
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={APIKey}&units=metric'
    try:
        response = requests.get(forecast_url)
        if response.status_code == 200:
            forecast_data = json.loads(response.text)

            if forecast_data and 'list' in forecast_data:
                forecast_list = forecast_data['list']
                forecast_info_list = []

                for entry in forecast_list:
                    # Parsing the date and time from the entry
                    dt = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
                    day_of_week = dt.weekday()  # Monday is 0 and Sunday is 6
                    hour_of_day = dt.hour

                    # Extracting the required fields
                    weather_main = entry['weather'][0]['main']
                    rain = float(entry.get('rain', {}).get('3h', 0.0))  # Ensure rain is a float
                    temp = float(entry['main']['temp'])  # Ensure temp is a float
                    wind_speed = float(entry['wind']['speed'])  # Ensure wind_speed is a float

                    # Compile extracted data into a dictionary
                    forecast_info = {
                        'main': weather_main,
                        'rain': rain,
                        'temp': temp,
                        'wind_speed': wind_speed,
                        'Day': day_of_week,
                        'Hour': hour_of_day,
                    }
                    forecast_info_list.append(forecast_info)

                # Create DataFrame from list of dictionaries
                forecast_df = pd.DataFrame(forecast_info_list)
                # Convert 'Day', 'Hour', and 'main' to categorical
                forecast_df['Day'] = forecast_df['Day'].astype('category')
                forecast_df['Hour'] = forecast_df['Hour'].astype('category')
                forecast_df['main'] = forecast_df['main'].astype('category')

                print(forecast_df.dtypes)  # Print data types to verify
                return forecast_df
            else:
                print("No data found in the response")
                return pd.DataFrame()
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

# Example usage:
forecast_df = get_forecast_data()
print(forecast_df)


def predict_available_bikes(df, model):
    """Predict the number of available bikes using the given model and DataFrame."""
    try:
        predicted_bikes = model.predict(df)[0]
        return predicted_bikes
    except Exception as e:
        print(f"An error occurred during prediction: {e}")

def get_model(station_number):
    model_name = f"RandomForest_Station_{station_number}.pkl"
    filepath = f"pickle_files/{model_name}"

    try:
        with open(filepath, 'rb') as file:
            station_model = pickle.load(file)
        print("Model loaded successfully.")
        return station_model
    except FileNotFoundError:
        print(f"File not found: {filepath}. Please check the filename and path.")
    except Exception as e:
        print(f"An error occurred while loading the pickle file: {e}")

def slice_forcast_data(day, hour, df):
    """Slice the forecast DataFrame based on the given day and hour."""
    sliced_df = df[(df['Day'] == day) & (df['Hour'] == hour)]
    return sliced_df

def run_prediction(day, hour, forecast_df, station_number):
    input_data = slice_forcast_data(day, hour, forecast_df)
    station_model = get_model(station_number)
    predicted_bikes = round(predict_available_bikes(input_data, station_model))
    return predicted_bikes

#day = int(input("Enter a Day (0=Monday, 6=Sunday): "))
#hour = round(int(input("Enter an hour (0-23, 24hr Clock): ")) / 3) * 3
#station_number = int(input("Enter a station number: "))

#predicted_bikes = run_prediction(day, hour, forecast_df, station_number)
#print(f"Predicted available bikes: {predicted_bikes}")


    
