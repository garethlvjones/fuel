import os
import time
import requests
import json
import sqlite3
import re

# global vars

fuel_key = "2SeFzEBklYy8HGNfK4H7yMOKHpGNfGw5"
fuel_auth = "Bearer sNCwVGSniGvsPaGWWkUAAvbXI7UA"
time_format = time.strftime("%d/%m/%Y %H:%M:%S %p")
transaction_id = str(int(time.time()))

get_stations_fuel_url = 'https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices'
get_reference_data_url = 'https://api.onegov.nsw.gov.au/FuelCheckRefData/v1/fuel/lovs'
# get_access_token = 'https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken'


def get_reference_data():
    
    ref_data = json.load(open('data/reference.json'))
    
    return ref_data  

    """
    get_reference_headers = {
    'content-type': "application/json; charset=utf-8",
    'apikey': fuel_key,
    'authorization': fuel_auth,
    'transactionid': transaction_id,
    'requesttimestamp': time_format,
    'if-modified-since': "24/06/2015 03:10:22 am",
    'cache-control': "no-cache",
    }
    
    response = requests.get(get_reference_data_url, headers=get_reference_headers)
    
    if (response.status_code == requests.codes.ok):
        ref_data = response.json()
    else:
        response.raise_for_status()
    
    return ref_data
    """


def get_stations_fuel():
    
    """ json data from gov.api is stored in data/fuel.json """
    
    # check if file exists (or is empty), return it if so
    if ( os.path.isfile('data/fuel.json') and os.path.getsize('data/fuel.json') > 0 ):
        station_data = json.load(open('data/fuel.json'))
        return station_data
        
    # if file doesn't exist, go get it from api
    else:
        get_stations_fuel_headers = {
            'content-type': "application/json; charset=utf-8",
            'apikey': fuel_key,
            'authorization': fuel_auth,
            'transactionid': transaction_id,
            'requesttimestamp': time_format,
            'cache-control': "no-cache",
        }
    
        fuel_output = requests.get(get_stations_fuel_url, headers=get_stations_fuel_headers)
        
        # Check api call worked, write file, return data
        if (fuel_output.status_code == requests.codes.ok):          # did api call work?
            x = fuel_output.json()                                  # jsonify return data
            with open('data/fuel.json', 'w') as f:                  # we know that file doens't exist yet
                json.dump(x, f, indent=4)                           # write to file the json object
        else:
            response.raise_for_status()
        
        station_data = json.load(open('data/fuel.json'))            # then re-read in the data, just to be sure it went ok
        return station_data                                         # and then return the data

def create_tables(c):
    
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS 
            brands (
                'name' TEXT NOT NULL, 'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
            )
        ''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS 
            fueltypes (
                'code' TEXT PRIMARY KEY NOT NULL, 
                'name' TEXT NOT NULL
            )
        ''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS 
            stations (
                'brand' TEXT NOT NULL, 
                'station_code' INTEGER PRIMARY KEY,
                'name' TEXT NOT NULL,
                'address' TEXT NOT NULL,
                'suburb' TEXT NOT NULL,
                'postcode' TEXT NOT NULL,
                'latitude' REAL,
                'longitude' REAL
            )
        ''')
                
        c.execute('''CREATE TABLE IF NOT EXISTS
            prices (
                'station_code' INTEGER,
                'fueltype' TEXT,
                'price' INTEGER,
                'last_updated' DATETIME
            )
        ''')
        return True
        
    except sqlite3.Error:
        print ("Error creating or checking tables.\n")
        return False

def add_data(c):
    
    try:
        c.execute('SELECT EXISTS (SELECT 1 FROM brands, fueltypes)')
        exists_brands_fueltypes = c.fetchone()[0]
        
        # check brand and fueltypes tables
        if (exists_brands_fueltypes == 0):
            ref_data = get_reference_data()             # get reference data from gov.api
            brands = ref_data['brands']['items']        # insert data into table brands
            for item in brands:
                for val in list(item.values()):
                    c.execute('INSERT INTO brands (name) VALUES (?)', [val])
            
            fueltypes = ref_data['fueltypes']['items']  # insert data into table fueltypes
            c.executemany('''
                INSERT INTO fueltypes
                    (code, name)
                VALUES
                    (:code, :name)''', fueltypes)
        
        # check stations and price tables    
        c.execute('SELECT EXISTS (SELECT 1 FROM stations, prices)')
        exists_stations_prices = c.fetchone()[0]
        
        if (exists_stations_prices == 0):
            station_data = get_stations_fuel()          # get station and price data from gov.api
            
            stations = station_data['stations']
            for station in stations:                    # add station data to station table
                postcode = station['address'][-4:]
                reversey = station['address'][::-1]
                suburbrev = re.search('N (.*?),',reversey)
                suburb = suburbrev.group(1)[::-1]
                c.execute(''' 
                    INSERT INTO 
                        stations (brand, station_code, name, address, suburb, postcode, latitude, longitude)
                    VALUES (?,?,?,?,?,?,?,?)''', 
                        (station['brand'], station['code'], station['name'], station['address'], suburb, postcode, 
                        station['location']['latitude'], station['location']['longitude'])
                )
            prices = station_data['prices']
            for price in prices:                        # add price data to prices table
                priceten = price['price'] * 10
                c.execute('''
                    INSERT INTO prices
                        (station_code, fueltype, price, last_updated)
                    VALUES
                        (?, ?, ?, ?)''', 
                        (price['stationcode'], price['fueltype'], priceten, price['lastupdated'])
                )
        return True
            
    except sqlite3.Error:
        print ("Error adding data.\n")
        return False

