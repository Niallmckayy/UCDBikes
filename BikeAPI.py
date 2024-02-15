# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 20:37:29 2024

@author: niall
"""

import requests

contract = 'dublin'  # Contract name for Dublin
api_key = '954118b06527f2a603d5abd3c315876b16221c14'  # Your JCDecaux API key
stations = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract}&apiKey={api_key}"
#parks = f"https://api.jcdecaux.com/parking/v1/contracts/{contract}/parks?apiKey={api_key}"
#one_station = f"https://api.jcdecaux.com/vls/v1/stations/{1}?contract={contract}&apiKey={api_key}"

def get_bike_stations(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None



bike_stations = get_bike_stations(stations)
if bike_stations:
    print("Bike station data retrieved successfully:")
    #dynamic data scraper
    for station in bike_stations:
        stationNumber = station["number"]
        lastUpdate = station["last_update"]
        numberBikes = station["available_bikes"]
        numberSlots = station["available_bike_stands"]
        status = station["status"]
    
        print(f"Station : {stationNumber}")
        print(f"Status: {status}")
        print(f"Last Updated: {lastUpdate}")
        print(f"Number of bikes: {numberBikes}")
        print(f"Number of slots: {numberSlots}")


#Key information needed
#last updated
#Number of bikes and slots
#Scraper should be running on the EC2 instance every 5 minutes
#Stored in RDS on AWS
#What happens if the connection drops, error handling, notification, does it still run when the instance is closed
#nohup linux command to keeo scrapper running 
#Crontab
#temux or screen
#memory management


