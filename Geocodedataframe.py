# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:53:52 2018

@author: sruthi.vs
"""

import geocoder
import pandas as pd
import time

class Geocodedataframe:
    def __init__(self,data):
        self.root = data
        
    def GeoCode(self):
        for index, row in self.root.iterrows():
            location = row['location']
            success = True
            try:
                results = geocoder.google(location)
                latlng = results.latlng
                #print(latlng)
                time.sleep(0.1)
                if success:
                    self.root.loc[index,'lat'] = latlng[0]
                    self.root.loc[index,'long'] = latlng[1]
                    print(data.loc[index,'lat'])
            except Exception as e:
               print(e)
        return(data)
    def ReverseGeoCode(self):
        for index, row in self.root.iterrows():
            lat = row['lat']
            lon = row['long']
            success = True
            try:
                results = Geocoder.reverse_geocode(lat,lon)
                #print(results)
                time.sleep(0.1)
                if success:
                    self.root.loc[index,'Address'] = results.formatted_address
            except Exception as e:
                print(e)
        return(data)

        

df = Geocodedataframe(data)

data2 = df.process()
