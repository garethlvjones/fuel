#!/usr/bin/python3

from fuel_helpers import *
import sqlite3

""" Expects to run once to get data from external gov.api, then create DB and enter in initial data set """

def main():
    
    ## 1. Does DB exist
    # check database to see if it exists (create if it doesn't)
    try:
        conn = sqlite3.connect('fuel.db')
    except sqlite3.Error:
        print ("Error opening db.\n")
        return False
    
    # make var to use to do db stuff
    c = conn.cursor()
    
    ## 2. Create tables if they don't exist already (brands, fueltypes, stations, prices)
    if (create_tables(c)):
        print("hello")
        conn.commit()

    ## 3. Add data if db table empty
    if (add_data(c)):
        print ("hello2")
        conn.commit()
    

if __name__ == "__main__":
    main();