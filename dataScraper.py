import sqlalchemy as sqla
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
import pandas as pd
import traceback
import requests

class DatabaseManager:
    def __init__(self, url, port, db, user, password):
        self.url = url
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{url}:{port}/{db}", echo=True)
        self.metadata = MetaData()
        self.connection = self.engine.connect()
        
    def create_table(self, table_name, columns):
        table = Table(table_name, self.metadata, *columns)
        table.create(self.engine, checkfirst=True)
        return table
            
    def execute_sql(self, sql):
        self.engine.execute(sql)


class StationDataHandler:
    def __init__(self, contract, api_key):
        self.contract = contract
        self.api_key = api_key
        self.stations_url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract}&apiKey={api_key}"

    def get_station_info(self):
        try:
            response = requests.get(self.stations_url)
            response.raise_for_status()
            print(response.json())
            return response.json()
        except Exception as e:
            print(f"Error fetching station information: {e}")
            traceback.print_exc()
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
        table = db_manager.create_table("station", columns)

        if station_data:
            # Assuming station_data is a list of dictionaries
            for data in station_data:
                db_manager.execute_sql(
                    table.insert(),
                    [
                        {
                            'address': data['address'],
                            'banking': data['banking'],
                            'bike_stands': data['bike_stands'],
                            'bonus': data['bonus'],
                            'contract_name': data['contract_name'],
                            'name': data['name'],
                            'number': data['number'],
                            'position_lat': data['position']['latitude'],
                            'position_lng': data['position']['longitude'],
                            'status': data['status']
                        }
                    ]
                )


# Define your database connection details
URL = "dublinbikes.c1ywqa2sojjb.eu-west-1.rds.amazonaws.com"
PORT = "3306"
DB = "dublinbikes"
USER = "admin"
PASSWORD = "boldlynavigatingnature"

# Create a DatabaseManager instance to manage database operations
db_manager = DatabaseManager(URL, PORT, DB, USER, PASSWORD)

# Define your API contract and key
contract = 'dublin'
api_key = '954118b06527f2a603d5abd3c315876b16221c14'

# Create a StationDataHandler instance to handle station data operations
station_data_handler = StationDataHandler(contract, api_key)

# Fetching station information from the API
station_data = station_data_handler.get_station_info()

# Inserting station data into the database
if station_data:
    station_data_handler.insert_station_data(db_manager, station_data)


