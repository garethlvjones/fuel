#!/usr/bin/python3

import os
import re
from cs50 import SQL
import requests
import json

""" AIMS:
- Get full dataset once, inset into DB
    - split dataset addresses for suburb, postcode
- Hourly check for change since [last check]
- poss calc best day, 7 day chart, etc
"""

### MAIN ###
def main():
    
    """ Use reference.json to create database 
    with open('static/reference.json') as reference:
        ref_data = reference.read() 
    """
        
    ref_data = json.load(open('static/reference.json'))
    
    # print(ref_data["brands"]["items"][0])
    
    # brands = ref_data["brands"]["items"]
    
    print ("brands[0]['Name']: ", ref_data['brands']['items'][0]['name'])
    
    
    ## Close file! 
    


### END MAIN ###



if __name__ == "__main__":
    main();