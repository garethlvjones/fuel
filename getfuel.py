#!/usr/bin/python3

import os
import re
import requests
import json
import sqlite3


""" AIMS:
- Get full dataset once, inset into DB
    - split dataset addresses for suburb, postcode
- Hourly check for change since [last check]
- poss calc best day, 7 day chart, etc
"""

### MAIN ###
def main():
    
                                                    ## 1. Get Data, store in file
    # open reference.json for writing
    # get reference from api.gov
    # pipe input to reference.json
    
    ### TO DO TO DO ###
    # use manual file to start with. This isn't too hard - do the hard db stuff first
    
                                                    ## 2. Create/open DB, open file, add data to tables
    
    # Create or open database
    # https://docs.python.org/3.6/library/sqlite3.html
    try:
        conn = sqlite3.connect('fuel.db')
    except sqlite3.Error:
        print ("Error opening db.\n")
        return False
        
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
                'longitude' REAL)'''
            )

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