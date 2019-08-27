import pandas as pd
import urllib
import os, sys, json, re
from math import *
from scipy import stats
import numpy as np


filename = "1500_2400Soles.json"
f = open(filename, "r")
data = pd.read_json(f)


# Standard plotly imports
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import matplotlib.pyplot as plt
import plotly_express as px

# Using plotly + cufflinks in offline mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)

# ===============================INITIALIZING ARRAYS =====================================
planSubDurArr = []
actSubDurArr = []
amountMarginUsedArr = {"all":[], "sb":[],"arm": [],"drive": []}
percentMarginUsedArr = {"all":[], "sb":[],"arm": [],"drive": []}
percentPlannedMarginArr = {"all":[], "sb":[],"arm": [],"drive": []}
amountUnusedTimeArr = {"all":[], "sb":[],"arm": [],"drive": []}
subsUsingMarginArr = []
over50PerMarginUseSBArr = []

#=========================================================================================
#==========================================================================================
#=================================== ADDING DATA ==========================================
#==========================================================================================
#==========================================================================================
for uniqueId in data.keys():
    #============================amountMarginUsed=======================================
    #Iterating through Unique ID column and calculating the amountMargin actually used by 
    #subtracting plannedMarginDuration -
    # Divide 60 to get in minutes and round nearest 3rd decimal place. 
    amountMarginUsed = round((data[uniqueId]['planMarginDur'] - data[uniqueId]['actMarginDur'])/60,3) 
    amountMarginUsedArr["all"].append(amountMarginUsed) #appending all of the marginal data 
    if ('SB' in data[uniqueId]['backboneType']):
            amountMarginUsedArr['sb'].append(amountMarginUsed)
    elif ('arm' in data[uniqueId]['backboneType']):
        amountMarginUsedArr['arm'].append(amountMarginUsed)
    elif ('drive' in data[uniqueId]['backboneType']):
        amountMarginUsedArr['drive'].append(amountMarginUsed)
    #============================percentMarginUsed=======================================
    # percent margin used is the amountMarginUsed / planMarginDur in minutes
    percentMarginUsed = round(amountMarginUsed/(data[uniqueId]['planMarginDur']/60),5)*100
    percentMarginUsedArr["all"].append(percentMarginUsed)
    if ('SB' in data[uniqueId]['backboneType']):
        percentMarginUsedArr['sb'].append(percentMarginUsed)
        if percentMarginUsed > 50:
            over50PerMarginUseSBArr.append(uniqueId)
    elif ('arm' in data[uniqueId]['backboneType']):
        percentMarginUsedArr['arm'].append(percentMarginUsed)
    elif ('drive' in data[uniqueId]['backboneType']):
        percentMarginUsedArr['drive'].append(percentMarginUsed)
    #============================percentPlannedMargin=======================================
    # percentPlannedMargin is the planMarginDur / planActivityDur in minutes
    percentPlannedMargin = round(data[uniqueId]['planMarginDur']/data[uniqueId]['planActivityDur'],5)*100
    percentPlannedMarginArr["all"].append(percentPlannedMargin)
    if ('SB' in data[uniqueId]['backboneType']):
        percentPlannedMarginArr['sb'].append(percentPlannedMargin)
    elif ('arm' in data[uniqueId]['backboneType']):
        percentPlannedMarginArr['arm'].append(percentPlannedMargin)
    elif ('drive' in data[uniqueId]['backboneType']):
        percentPlannedMarginArr['drive'].append(percentPlannedMargin)
    #============================create a summary=======================================
    if (percentMarginUsed > 0):
        subsUsingMarginArr.append(uniqueId)
    #  we want to summarize how many unused minutes we are saving as a comparison
    amountUnusedTime = round((data[uniqueId]['planTotalDur'] - data[uniqueId]['actActivityDur'])/60,2)
    if amountUnusedTime >0:
        amountUnusedTimeArr["all"].append(amountUnusedTime)
        if ('SB' in data[uniqueId]['backboneType']):
            amountUnusedTimeArr['sb'].append(amountUnusedTime)
        elif ('arm' in data[uniqueId]['backboneType']):
            amountUnusedTimeArr['arm'].append(amountUnusedTime)
        elif ('drive' in data[uniqueId]['backboneType']):
            amountUnusedTimeArr['drive'].append(amountUnusedTime)    

# amountMarginUsedArr = {"all":[], "sb":[],"arm": [],"drive": []}
# percentMarginUsedArr = {"all":[], "sb":[],"arm": [],"drive": []}
# percentPlannedMarginArr = {"all":[], "sb":[],"arm": [],"drive": []}
# amountUnusedTimeArr = {"all":[], "sb":[],"arm": [],"drive": []}

df_amountMarginUsed = pd.DataFrame(columns = ['all', 'sb', 'arm', 'drive'])
for column in df_amountMarginUsed.keys():
    df_amountMarginUsed[column] = pd.Series(amountMarginUsedArr[column])

df_percentMarginUsed = pd.DataFrame(columns = ['all', 'sb', 'arm', 'drive'])
for column in df_percentMarginUsed.keys():
    df_percentMarginUsed[column] = pd.Series(percentMarginUsedArr[column])

df_percentMarginUsed = pd.DataFrame(columns = ['all', 'sb', 'arm', 'drive'])
for column in df_percentMarginUsed.keys():
    df_percentMarginUsed[column] = pd.Series(percentMarginUsedArr[column])

df_IdleTime = pd.DataFrame(columns = ['all', 'sb', 'arm', 'drive'])
for column in df_IdleTime.keys():
    df_IdleTime[column] = pd.Series(amountUnusedTimeArr[column])
    

df_amountMarginUsed.to_csv(r'explicitMargindata', index = False) # index = False is not generating the row numbers. 