import json
import mysql.connector
import sqlalchemy as sqla
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
import pandas as pd
import traceback
import requests
import logging
from sqlalchemy.sql import text

class DatabaseManager:
    def __init__(self, url, port, db, user, password):
        self.url = url
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{db}", echo=True)
        self.metadata = MetaData()
        self.connection = self.engine.connect()
        
    def create_table(self, table_name, columns):
        table = Table(table_name, self.metadata, *columns)
        table.create(self.engine, checkfirst=True)
        logging.info(f"Table {table_name} created successfully.")
        print(f"Table {table_name} created successfully.")
    
    #potentially irrelevant        
    def execute_sql(self, sql, values):
        try:
            self.connection.execute(sql, values)
            logging.info("SQL command executed successfully.")
        except Exception as e:
            logging.error(f"Error executing SQL command: {e}")
            print(f"Error executing SQL command: {e}")

        

class StationDataHandler:
    def __init__(self, contract, api_key):
        self.contract = contract
        self.api_key = api_key
        self.stations_url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract}&apiKey={api_key}"

    def get_station_info(self):
        try:
            response = requests.get(self.stations_url)
            if response.status_code == 200:
                json.loads(response.text)
                return json.loads(response.text)
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def insert_station_data(self, db_manager, station_data):
        columns = [
            Column('address', String(256)),
            Column('banking', Integer),
            Column('bike_stands', Integer),
            Column('bonus', Integer),
            Column('contract_name', String(256)),
            Column('name', String(256)),
            Column('number', Integer),
            Column('position_lat', Float),
            Column('position_lng', Float),
            Column('status', String(256))
        ]
        db_manager.create_table("station", columns)

        if station_data:
            
            for data in station_data:

                address = data.get('address')
                banking =  int(data.get('banking'))
                bike_stands = data.get('bike_stands')
                bonus = int(data.get('bonus'))
                contract = data.get('contract_name')
                name = data.get('name')
                number = data.get('number')
                lat = data.get('position').get('lat')
                lng = data.get('position').get('lng')
                status = data.get('status')

                values = (address, banking, bike_stands, bonus, contract, name, number, lat, lng, status)
                #Values are correctly pulled from the API
                print(values)

                #Issue with executing code below
                db_manager.engine.execute("INSERT INTO station VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
                print(f"Station {name} inserted successfully.")

# Database connection details
URL = "dublinbikes.c1ywqa2sojjb.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dublinbikes"
USER = "admin"
PASSWORD = "boldlynavigatingnature"


db_manager = DatabaseManager(URL, PORT, DB, USER, PASSWORD)

# API connection details
contract = 'dublin'
api_key = '954118b06527f2a603d5abd3c315876b16221c14'


station_data_handler = StationDataHandler(contract, api_key)

# Fetching station information from the API
station_data = station_data_handler.get_station_info()

# Inserting station data into the database
if station_data:
    station_data_handler.insert_station_data(db_manager, station_data)



