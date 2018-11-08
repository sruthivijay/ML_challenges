# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 17:16:30 2018

@author: sruthi.vs
"""

import xml.etree.ElementTree as ET
import pandas as pd
import xmltodict
import pprint
import json


class xmltojson:
    def __init__(self,name):
        file_name = name
    def converter(self):
        with open("xml_data.xml") as fd:
            doc = xmltodict.parse(fd.read())
            data = json.dumps(doc)
        return data
    

final_data = xmltojson("xml_data.xml")

data2 = final_data.converter()