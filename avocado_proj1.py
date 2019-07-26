#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 22:08:21 2019

@author: Ada Zhu (gz6xw)
"""
import pandas as pd
import numpy as np

df = pd.read_csv("avocado.csv") #18249 rows
df2 = pd.read_csv("uscities.csv", encoding = "ISO-8859-1") #37842
df2.columns = ['region', 'state', 'density'] #rename column names

#remove duplicated cities based on density #around 20 albany across states.
df2unique = df2.sort_values('density', ascending=False).drop_duplicates('region').sort_index() #23944
#remove empty spaces to match with uscities.csv
df2unique['region'] = df2unique['region'].str.replace(' ', '')


'''
df3 = pd.read_csv("states.csv") #18249 rows
df3['State'] = df3['State'].str.replace(' ', '')
df3.columns = ['state']
print(df3)
'''


#add month col
df['month'] = pd.DatetimeIndex(df['Date']).month

#add season col
conditions = [
    df['month'].isin([3, 4, 5]),
    df['month'].isin([6, 7, 8]),
    df['month'].isin([9, 10, 11])]
choices = ['Spring', 'Summer', 'Fall']
df['season'] = np.select(conditions, choices, default='Winter')


df["region"].nunique() #54
df["region"].unique()

#map all to state col

#join with uscities
#if city, map to corresponding state that makes the most sense
comb = pd.merge(df, df2unique, on='region', how='left') #18249
#atlanta IN GEORGIA not TEXAS!
#empty space!!
#cali not in Missouri
#BaltimoreWashington  ---- combined
#saint louis not stlouis


##if already state,  map city to their corresponding states

#hardcode combined cities, region, and TOTAL US.
comb.loc[comb.region == "BaltimoreWashington", 'state'] = "BaltimoreWashington"
comb.loc[comb.region == "BuffaloRochester", 'state'] = "BuffaloRochester"
comb.loc[comb.region == "California", 'state'] = "California"
comb.loc[comb.region == "CincinnatiDayton", 'state'] = "CincinnatiDayton"
comb.loc[comb.region == "DallasFtWorth", 'state'] = "DallasFtWorth"
comb.loc[comb.region == "GreatLakes", 'state'] = "GreatLakes"
comb.loc[comb.region == "HarrisburgScranton", 'state'] = "HarrisburgScranton"
comb.loc[comb.region == "HartfordSpringfield", 'state'] = "HartfordSpringfield"
comb.loc[comb.region == "MiamiFtLauderdale", 'state'] = "MiamiFtLauderdale"
comb.loc[comb.region == "Midsouth", 'state'] = "Midsouth"
comb.loc[comb.region == "NewOrleansMobile", 'state'] = "NewOrleansMobile"
comb.loc[comb.region == "Northeast", 'state'] = "Northeast"
comb.loc[comb.region == "PhoenixTucson", 'state'] = "PhoenixTucson"
comb.loc[comb.region == "RichmondNorfolk", 'state'] = "RichmondNorfolk"
comb.loc[comb.region == "SouthCarolina", 'state'] = "SouthCarolina"
comb.loc[comb.region == "SouthCentral", 'state'] = "SouthCentral"
comb.loc[comb.region == "Southeast", 'state'] = "Southeast"
comb.loc[comb.region == "StLouis", 'state'] = "Oklahoma"
comb.loc[comb.region == "TotalUS", 'state'] = "TotalUS"
comb.loc[comb.region == "WestTexNewMexico", 'state'] = "WestTexNewMexico"

#add COMBINED col
# 1 if the location is a region / combined cities / total US
# 0 o.w
conditions = [
    comb['state'].isin([ "BaltimoreWashington", "BuffaloRochester", "CincinnatiDayton", 
      "DallasFtWorth", "GreatLakes", "HarrisburgScranton", "HartfordSpringfield", 
      "MiamiFtLauderdale", "Midsouth", "NewOrleansMobile", "Northeast", 
      "PhoenixTucson", "RichmondNorfolk", "SouthCentral", "Southeast", "TotalUS", 
      "WestTexNewMexico"])]

choices = [1]
comb['combined'] = np.select(conditions, choices, default=0)

comb.to_csv("avocado_clean.csv")


print(df)