#!/usr/bin/python3

import os
import re
# from cs50 import SQL
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
    ref_data = json.load(open('static/reference.json'))
    
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
                'latitude' REAL NOT NULL,
                'longitude' REAL NOT NULL)''')
    
    c.execute('SELECT EXISTS (SELECT 1 FROM stations)')
    exists_stations = c.fetchone()[0]
    
    if (exists_stations == 0):
        stations = ref_data['stations']['items']
        c.executemany('''
            INSERT INTO stations
                (brand, code, name, address, latitude, longitude)
            VALUES
                (:brand, :code, :name, :address, :latitude, :longitude)''', stations)
    

    conn.commit()




    ## Close reference.json file! 
    


### END MAIN ###



if __name__ == "__main__":
    main();