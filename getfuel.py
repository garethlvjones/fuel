#!/usr/bin/python3

import re
import json
import sqlite3
from helpers import *

### MAIN ###
def main():
    
    """
    1. Does DB Exsist
        - n. create
    
    2. Do tables exist (brands, fueltypes, stations, prices)
        - n. create empty
    
    3. Do tables have data
        - n. run get reference, run get fuel only if needed
        3.1 add data to DB
        """
    
    ## 1. Does DB exist
    # check database to see if it exists (create if it doesn't)
    try:
        conn = sqlite3.connect('fuel.db')
    except sqlite3.Error:
        print ("Error opening db.\n")
        return False
    
    # make var to use to do db stuff
    c = conn.cursor()
    
    ## 2. Create tables if they don't exist already (brands, fueltypes, stations)
    c.execute('''CREATE TABLE IF NOT EXISTS brands
    ('name' TEXT NOT NULL, 'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS 
            fueltypes (
                'code' TEXT PRIMARY KEY NOT NULL, 
                'name' TEXT NOT NULL)''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS 
            stations (
                'brand' TEXT NOT NULL, 
                'code' INTEGER PRIMARY KEY,
                'name' TEXT NOT NULL,
                'address' TEXT NOT NULL,
                'suburb' TEXT NOT NULL,
                'postcode' TEXT NOT NULL,
                'latitude' REAL,
                'longitude' REAL,
                'last_updated' DATETIME
            )''')
            
    c.execute('''
        CREATE TABLE IF NOT EXISTS 
            prices (
                'code' INTEGER NOT NULL PRIMARY KEY, 
                '
            )''')
            
    ## 3. Do tables have data already
    c.execute('SELECT EXISTS (SELECT 1 FROM brands)')
    exists_brands = c.fetchone()[0]
    
    c.execute('SELECT EXISTS (SELECT 1 FROM fueltypes)')
    exists_fueltypes = c.fetchone()[0]
    
    c.execute('SELECT EXISTS (SELECT 1 FROM stations)')
    exists_stations = c.fetchone()[0]
    
    if (exists_brands == 0 || exists_fueltypes == 0):
        ref_data = get_reference_data()             # get reference data from gov.api
        
        fueltypes = ref_data['fueltypes']['items']  # insert data into table fueltypes
        c.executemany('''
            INSERT INTO fueltypes
                (code, name)
            VALUES
                (:code, :name)''', fueltypes)
                
        brands = ref_data['brands']['items']        # insert data into table brands
        for item in brands:
            for val in list(item.values()):
                c.execute('INSERT INTO brands (name) VALUES (?)', [val])
        
                
    if (exists_stations == 0):
        fuel_data = get_all_fuel_prices()            # get current prices from gov.api
        stations = fuel_data['stations']
        prices = fuel_data['prices']
        
        for station in stations:                    # add station data to station table
            postcode = station['address'][-4:]
            reversed = station['address'][::-1]
            suburbrev = re.search('N (.*?),',reversed)
            suburb = suburbrev.group(1)[::-1]
            c.execute('''
                INSERT INTO stations
                    (brand, code, name, address, suburb, postcode, latitude, longitude)
                VALUES
                    (?,?,?,?,?,?,?,?)''', 
                    (station['brand'], station['code'], station['name'], station['address'], \
                     suburb, postcode, station['location']['latitude'], station['location']['longitude'])
                )
        
        for prices in stations:                     # add price data to prices table
    
    
                                                    ## 1. Get Data, store in file
    

    # get all fuel prices
    all_fuel = get_all_fuel_prices()

    
    """
    get_reference_data()
    update_reference_data()
    update_fuel_prices()
    """
    

    """ 
    to do here: 
    # get reference.json from api call
    # update reference.json file
    # put allfuel in to data/allfuel.json
    # insert allfuel.json in to db, using 'code' to update
    # update last_update field in DB
    """    
        
    
                                                    ## 2. Create/open DB, open file, add data to tables
    

    # make var to use to do db stuff
    c = conn.cursor()
    
    # load up json file
    ref_data = json.load(open('data/reference.json'))

    
    ## Insert brands
    # create empty table 'brands if not there already'
    c.execute('''CREATE TABLE IF NOT EXISTS brands
    ('name' TEXT NOT NULL, 'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)''')

    # Insert brands data to DB
    c.execute('SELECT EXISTS (SELECT 1 FROM brands)')
    exists_brands = c.fetchone()[0]
    
    if (exists_brands == 0):
        brands = ref_data['brands']['items']
        for item in brands:
            for val in list(item.values()):
                c.execute('INSERT INTO brands (name) VALUES (?)', [val])
                
                
    ## Insert fueltypes (name, code)
    # create table 'fueltypes' if not there already
    c.execute('''
        CREATE TABLE IF NOT EXISTS 
            fueltypes (
                'code' TEXT PRIMARY KEY NOT NULL, 
                'name' TEXT NOT NULL)''')
    
    c.execute('SELECT EXISTS (SELECT 1 FROM fueltypes)')
    exists_fueltypes = c.fetchone()[0]
    
    if (exists_fueltypes == 0):
        fueltypes = ref_data['fueltypes']['items']
        c.executemany('''
            INSERT INTO fueltypes
                (code, name)
            VALUES
                (:code, :name)''', fueltypes)
    
    ## Insert stations (brand, code, name, address, lat, long)
    # create table 'stations' if not there already
    c.execute('''
        CREATE TABLE IF NOT EXISTS 
            stations (
                'brand' TEXT NOT NULL, 
                'code' INTEGER PRIMARY KEY,
                'name' TEXT NOT NULL,
                'address' TEXT NOT NULL,
                'suburb' TEXT NOT NULL,
                'postcode' TEXT NOT NULL,
                'latitude' REAL,
                'longitude' REAL,
                'current_price' INTEGER)''')

    # insert data, inc raw address
    c.execute('SELECT EXISTS (SELECT 1 FROM stations)')
    exists_stations = c.fetchone()[0]
    
    stations = ref_data['stations']['items']
    
    if (exists_stations == 0):
        for station in stations:
            postcode = station['address'][-4:]
            reversed = station['address'][::-1]
            suburbrev = re.search('N (.*?),',reversed)
            suburb = suburbrev.group(1)[::-1]
            c.execute('''
                INSERT INTO stations
                    (brand, code, name, address, suburb, postcode, latitude, longitude)
                VALUES
                    (?,?,?,?,?,?,?,?)''', 
                    (station['brand'], station['code'], station['name'], station['address'], suburb, postcode, station['location']['latitude'], station['location']['longitude'])
                )

    conn.commit()
    


    ## Close reference.json file! 
    


### END MAIN ###



if __name__ == "__main__":
    main();