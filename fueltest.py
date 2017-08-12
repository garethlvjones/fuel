#!/usr/bin/python3

import re
import json
import sqlite3
from helpers import *

def main():
    
    # load up json file
    station_data = open('data/fuel2.json')
    
    x = json.load(station_data)
    
    
    with open('data/fuel.json', 'w') as f:                  # we know that file doens't exist yet
        # f.write(station_data)
        json.dump(x, f, indent=4)                           # write to file the json object
    





if __name__ == "__main__":
    main();