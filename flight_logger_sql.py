#!/usr/bin/python3
import os
from datetime import datetime
from datetime import date
import json
import csv

try:
    from dotenv import load_dotenv
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'python-dotenv'])
    from dotenv import load_dotenv

try:
    import requests
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'requests'])
    import requests

try:
    import pandas as pd
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'pandas'])
    import pandas as pd

try:
    import numpy as np
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'numpy'])
    import numpy as np
try:
    import sqlalchemy
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'SQLAlchemy psycopg2-binary'])
    import sqlalchemy

from sqlalchemy import create_engine

# Load env variables
load_dotenv(dotenv_path='')
#db = os.getenv("flightdata.db")
#db = os.getenv('sqlite:///flightdata.db')
#db_table = os.getenv('flight_data')
db= 'sqlite:////home/pi/flightlogger/flightdata.db'
db_table = 'flight_data'

# get json data
with open("/run/dump1090-fa/aircraft.json", "r") as aircraft:
    file_contents = aircraft.read()
    json_dump = json.loads(file_contents)

#engine = create_engine(db)
engine = create_engine(db)

# get today's date and time of pull
today = date.today()
time = datetime.now().strftime("%H:%M:%S")

# turn JSON dump into a Panda's Data Frame
df = pd.json_normalize(json_dump['aircraft'])

# Add a date and time column to the Data Frame
df['date'], df['time'] = [today, time]

# Get rid of the columns we don't want
df = df.filter(items=['hex', 'flight', 'alt_baro', 'alt_geom', 'gs', 'track', 'geom_rate', 'squawk', 'emergency', 'category', 'nav_qnh', 'nav_altitude_mcp', 'lat', 'lon', 'date', 'time'])

# Remove any rows that do not have location data
df.dropna(subset=['lat'], inplace=True)

# Send Data Frame to your sql database
df.to_sql(db_table, con=engine, if_exists='append', index=False)

# print success and exit the program
print("File Transfer Complete")
exit()

