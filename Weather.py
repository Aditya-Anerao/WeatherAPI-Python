#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Assignment 1: 
Open Weather Map Weather Forecast
Due: Tuesday, August 31, 11:59pm
https://www.csc2.ncsu.edu/faculty/healey/msa/python/assn-openweathermap/

@author: Aditya Anerao
"""
# Relevant Packages
import requests
from datetime import datetime, timedelta, date
import sys
import numpy as np
import csv


api_key = 'XXXX' #API Key
link = 'https://api.openweathermap.org/data/2.5/forecast?' # Link to URL

# Set Cities
loc = [\
  [ 'Anchorage', 'Alaska', "USA" ],\
  [ 'Chennai', 'India' ],\
  [ 'Jiangbei', 'China' ],\
  [ 'Kathmandu', 'Nepal' ],\
  [ 'Kothagudem', 'India' ],\
  [ 'Lima', 'Peru' ],\
  [ 'Manhasset', 'New York', "USA" ],\
  [ 'Mexico City', 'Mexico' ],\
  [ 'Nanaimo', 'Canada' ],\
  [ 'Peterhead', 'Scotland' ],\
  [ 'Polevskoy', 'Russia' ],\
  [ 'Round Rock', 'Texas', "USA" ],\
  [ 'Seoul', 'South Korea' ],\
  [ 'Solihull', 'England' ],\
  [ 'Tel Aviv', 'Israel' ]\
]

# Create CSV File
out = open('temp.csv', 'w', newline='', encoding='latin')
writer = csv.writer(out)
# Write Header
writer.writerow(['City', 'Min 1', 'Max 1', 'Min 2', 'Max 2', 'Min 3',
 'Max 3', 'Min 4', 'Max 4', 'Min 5', 'Max 5', 'Min Avg', 'Max Avg'])


for City in loc:
    #Update API URL for City of interest
    URL = link + 'q=' + City[0] + "," + City[1] + '&appid=' + api_key +'&units=metric'
    
    #Obtain data from API
    response = requests.get( URL )
    if response.status_code != 200:      # Failure?
        print( 'Error:', response.status_code )
        sys.exit( 0 )
    
    data = response.json()
       
    # get current date
    now_date = date.today()
  
    # Create Empty lists for each day's temperature values 
    mini_1 = []
    maxi_1 = []
    mini_2 = []
    maxi_2 = []
    mini_3 = []
    maxi_3 = []
    mini_4 = []
    maxi_4 = []
    mini_5 = []
    maxi_5 = []
    
    # For each time block 
    for i in range( 0, len( data[ 'list' ] ) ):
       
        dt_string = data['list'][i]['dt_txt'] #isolate timestamp of timeblock
        dt_UTC = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S') # convert timestamp string to date
        UTC_offset = data[ 'city' ]['timezone'] #define timezone offset
        dt_local = dt_UTC + timedelta(seconds = UTC_offset) #convert UTC --> local time
        dt_date = dt_local.date() #isolate date from date_time
        days = timedelta(days=1) # set date incrementor
        
        # Day 0
        if dt_date == now_date:
            next
                
        #Day 1
        if dt_date == (now_date + days): # Day 1
            mini_1.append(data['list'][i]['main']['temp_min'])
            maxi_1.append(data['list'][i]['main']['temp_max'])
        
        # Day 2
        if dt_date == (now_date + 2 * days): # Day 2
            mini_2.append(data['list'][i]['main']['temp_min'])
            maxi_2.append(data['list'][i]['main']['temp_max'])
        
        # Day 3
        if dt_date == (now_date + 3 * days): # Day 3
            mini_3.append(data['list'][i]['main']['temp_min'])
            maxi_3.append(data['list'][i]['main']['temp_max'])
        
        # Day 4
        if dt_date == (now_date + 4 * days): # Day 4           
            mini_4.append(data['list'][i]['main']['temp_min'])
            maxi_4.append(data['list'][i]['main']['temp_max'])
        
        # Day 5
        if dt_date == (now_date + 5 * days): # Day 5
            mini_5.append(data['list'][i]['main']['temp_min'])
            maxi_5.append(data['list'][i]['main']['temp_max'])
        
    #Find minimum and maximum values for each day
    
    min1 = min(mini_1)
    max1 = max(maxi_1)
    
    min2 = min(mini_2)
    max2 = max(maxi_2)
            
    min3 = min(mini_3)
    max3 = max(maxi_3)
    
    min4 = min(mini_4)
    max4 = max(maxi_4)
    
    if mini_5 != []:
        min5 = min(mini_5)
    else:
        min5 = np.nan
    if maxi_5 != []:
        max5 = max(maxi_5)
    else:
        max5 = np.nan
  
    #Calculate Average minimum and Average maximum
    minAvg = np.nanmean([min1,min2,min3,min4,min5])
    maxAvg = np.nanmean([max1,max2,max3,max4,max5])
    
    #Drop State from US cities
    City = City[0]+ ", " + City[-1]
    
    # Create row with data
    row = [City, min1, max1, min2, max2, min3, max3, min4, max4, min5, max5,
           minAvg, maxAvg]
    
    # format data to 2 decimal places
    for i in range(1,len(row)):
        row[i] = format(row[i], '.2f')
           
    #Write Row to CSV
    writer.writerow(row) 

out.close() 