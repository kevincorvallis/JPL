#!/tps/bin/python -B

import os, sys, json, re
from math import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

def main():
    # ------------------------------------- Initialization and Input Parameters -------------------------------
    inputFilename = 'submasterDurations_sols1000to2169_preUpdate.json'
    doPlot = True
    doPercentiles = True
    # ------------------------------------- Open json file --------------------------------------------
    with open(inputFilename) as fp:
        data = json.load(fp)
    planSubDurArr = []
    actSubDurArr = []
    amountMarginUsedArr = {"all":[], "sb":[],"arm": [],"drive": []}
    percentMarginUsedArr = {"all":[], "sb":[],"arm": [],"drive": []}
    percentPlannedMarginArr = {"all":[], "sb":[],"arm": [],"drive": []}
    amountUnusedTimeArr = {"all":[], "sb":[],"arm": [],"drive": []}
    subsUsingMarginArr = []
    over50PerMarginUseSBArr = []

    for uniqueId in data.keys():
        # amountMarginUsed is defined as the amount of explicit margin (ie the margin block in MSLICE) that was actual used.  in minutes
        amountMarginUsed = round((data[uniqueId]['planMarginDur'] - data[uniqueId]['actMarginDur'])/60,2)
        amountMarginUsedArr["all"].append(amountMarginUsed)
        # This is a filter to exclude certain specific durations 
        #if data[uniqueId]['planActivityDur'] < 10*60:
        #        continue
        if ('SB' in data[uniqueId]['backboneType']):
            amountMarginUsedArr['sb'].append(amountMarginUsed)
        elif ('arm' in data[uniqueId]['backboneType']):
            amountMarginUsedArr['arm'].append(amountMarginUsed)
        elif ('drive' in data[uniqueId]['backboneType']):
            amountMarginUsedArr['drive'].append(amountMarginUsed)
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
        # percentPlannedMargin is the planMarginDur / planActivityDur in minutes
        percentPlannedMargin = round(data[uniqueId]['planMarginDur']/data[uniqueId]['planActivityDur'],5)*100
        percentPlannedMarginArr["all"].append(percentPlannedMargin)
        if ('SB' in data[uniqueId]['backboneType']):
            percentPlannedMarginArr['sb'].append(percentPlannedMargin)
        elif ('arm' in data[uniqueId]['backboneType']):
            percentPlannedMarginArr['arm'].append(percentPlannedMargin)
        elif ('drive' in data[uniqueId]['backboneType']):
            percentPlannedMarginArr['drive'].append(percentPlannedMargin)
        #create a summary 
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
    # --------------------------------- Create plots --------------------------------------------  
    # create a subplot of histograms of the amount of explicit margin actually used
    if doPlot == True:
        makeQuadPlot (1, 'Amount of Explicit Margin Actually Used in Minutes', 'Amount of Explicit Margin Used (min)', 'Count', amountMarginUsedArr) 
         # create a subplot of histograms of the percent of explicit margin actually used
        makeQuadPlot (2, 'Percent of Explicit Margin Actually Used', '% of Planned Margin', 'Count', percentMarginUsedArr)
        # create a subplot of closer in histograms of the percent of explicit margin actually used
        makeQuadPlot (3, 'Percent of Explicit Margin Actually Used', '% of Planned Margin', 'Count', percentMarginUsedArr, [-100,None])
        #create figure of unused time
        makeQuadPlot (4, 'Amount of Vehicle Idle Time (minutes)', 'Minutes of Idle Time', 'Count', amountUnusedTimeArr)
        # create a subplot of the current practices of planned margin duration of margin as a fraction of planned activity duration
        makeQuadPlot (5, 'Planned Margin Duration as % of Planned Activity Duration', '%', 'Count', percentPlannedMarginArr, [None,100])
        
    #===========================================================================
    # doing various tests for normality.  Trying to figure out how to compare the datasets.
    # plt.figure(6)
    # print(min(amountUnusedTimeArr['all']))
    # vals = np.log(amountUnusedTimeArr['sb'])
    # print(min(vals))
    # print(max(vals))
    # plt.hist(vals)   
    # print(stats.normaltest(amountUnusedTimeArr['sb']))
    # print(stats.normaltest(vals))
    # print(stats.skewtest(amountUnusedTimeArr['sb']))
    # print(stats.kurtosistest(amountUnusedTimeArr['sb']))
    # print("IdleTimeAverage = " + str(np.average(amountUnusedTimeArr['arm'])))
    #===========================================================================
    if doPercentiles == True:
        print('')
        print('Percent Margin ever used:')
        percentilesArr = [25,50,75,95,99]
        for category in percentMarginUsedArr:
            print('Category: ' + category)
            print(str(round(100-stats.percentileofscore(percentMarginUsedArr[category], 0),2)) + '% of ' + category + ' activities use any margin at all')
            percentile_valueArr = np.percentile(percentMarginUsedArr[category],percentilesArr)
            for index, percentileValue in enumerate(percentile_valueArr):
                print(str(percentilesArr[index]) + ' percentile percent of margin used = ' + str(percentileValue) + '%')
        print()
        print('Amount Margin ever used')
        for category in amountMarginUsedArr:
            print('Category: ' + category)
            print(str(round(100-stats.percentileofscore(amountMarginUsedArr[category], 0),2)) + ' minutes of ' + category + ' activities use any margin at all')
            percentile_valueArr = np.percentile(amountMarginUsedArr[category],percentilesArr)
            for index, percentileValue in enumerate(percentile_valueArr):
                print(str(percentilesArr[index]) + ' percentile minutes of margin used = ' + str(percentileValue))
        print('Percent of margin planned relative to activity duration')
        for category in percentPlannedMarginArr:
            print('Category: ' + category)
            percentile_valueArr = np.percentile(percentPlannedMarginArr[category],percentilesArr)
            for index, percentileValue in enumerate(percentile_valueArr):
                print(str(percentilesArr[index]) + ' percentile percent of margin planned relative to activity duration = ' + str(percentileValue))
                
        print('Amount of Idle Time in Minutes')
        for category in amountUnusedTimeArr:
            print('Category: ' + category)
            percentile_valueArr = np.percentile(amountUnusedTimeArr[category],percentilesArr)
            for index, percentileValue in enumerate(percentile_valueArr):
                print(str(percentilesArr[index]) + ' percentile idle time in minutes = ' + str(percentileValue))
                
    #=======================================================================
    # print(stats.percentileofscore(percentMarginUsedArr['all'], 0))
    # print(stats.percentileofscore(percentMarginUsedArr['sb'], 0))
    # print(stats.percentileofscore(percentMarginUsedArr['arm'], 0))
    # print(stats.percentileofscore(percentMarginUsedArr['drive'], 0))    
    # print(np.percentile(percentMarginUsedArr['all'],[25,50,75,95,99]))    
    # print(np.percentile(percentMarginUsedArr['sb'],[25,50,75,95,99])) 
    # print(np.percentile(percentMarginUsedArr['arm'],[25,50,75,95,99])) 
    # print(np.percentile(percentMarginUsedArr['drive'],[25,50,75,95,99]))  
    #=======================================================================
    with open('seqIDsThatUsedAnyMargin.json', 'w') as fp4:
        json.dump(subsUsingMarginArr, fp4, sort_keys = True, indent= 4)
    with open('SBsThatUsed50PercentMargin.json', 'w') as fp4:
        json.dump(over50PerMarginUseSBArr, fp4, sort_keys = True, indent= 4)
    plt.subplots_adjust(left=0.12, bottom=0.10, right=0.95,top=0.88,wspace=0.25, hspace=0.35)
    plt.show()
    print('script complete')

#######################################################
def hist_fixedBinsWidth (fig, arr, width = 1, subplotNum = [], binOverrides = None):
    #Inputs: 
    #   fig = matplotlib figure number as integer; defined from instantiation of figure
    #   arr = array to be plotted on a histogram
    #   width = custom Width of bins as an integer. 
    # Outputs:
    #   returns the figure with updated entries
    binLow = None
    binHigh = None
    if binOverrides:
        if binOverrides[0] != None:
            binLow = binOverrides[0]
        if binOverrides[1] != None:
            binHigh = binOverrides[1]
    if not binLow:
        binLow = int(floor(min(arr)/width)*width)
    if not binHigh:
        binHigh = int(ceil(max(arr)/width)*width)
    binsDist = range(binLow, binHigh+width, width)
    plt.figure(fig)
    if subplotNum:
        plt.subplot(subplotNum[0], subplotNum[1],subplotNum[2])                
    plt.hist(arr, rwidth=.95, bins = binsDist)
    return fig

def makeQuadPlot (figNum, title, xLabel, yLabel, dataArr , binOverrides = None):
    fig = plt.figure(figNum)
    fig.suptitle(title)
    plot_titleAndLabels (figNum, 'All Activities', xLabel, yLabel, [2,2,1])
    if binOverrides:
        hist_fixedBinsWidth (figNum,dataArr['all'],5, [2,2,1], binOverrides)
    else:
        hist_fixedBinsWidth (figNum,dataArr['all'],5, [2,2,1])
    plt.figure(figNum)
    plot_titleAndLabels (figNum, 'Science Blocks', xLabel, yLabel, [2,2,2])
    if binOverrides:
        hist_fixedBinsWidth (figNum,dataArr['sb'],5, [2,2,2], binOverrides)
    else: 
        hist_fixedBinsWidth (figNum,dataArr['sb'],5, [2,2,2])
    plt.figure(figNum)
    plot_titleAndLabels (figNum, 'Arm Backbones', xLabel, yLabel, [2,2,3])
    if binOverrides:
        hist_fixedBinsWidth (figNum,dataArr['arm'],5, [2,2,3], binOverrides)
    else: 
        hist_fixedBinsWidth (figNum,dataArr['arm'],5, [2,2,3])
    plt.figure(figNum)
    plot_titleAndLabels (figNum, 'Drives', xLabel, yLabel,[2,2,4])
    if binOverrides:
        hist_fixedBinsWidth (figNum,dataArr['drive'],5, [2,2,4], binOverrides)
    else: 
        hist_fixedBinsWidth (figNum,dataArr['drive'],5, [2,2,4], binOverrides)
        
def plot_titleAndLabels (fig, title_s, xlabel_s, ylabel_s, subplotNum=[]):
    #Inputs:
    #   fig = matplotlib figure number as integer; defined from instantiation of figure
    #   title_s = string of the title to put on the figure
    #   xlabel_s = string of the xlabel to put on the figure
    #   ylabel_s = string of the ylabel to put on the figure
    # Outputs:
    #   returns the figure with updated entries
    plt.figure(fig)
    print("Subplot numbers are ", subplotNum)
    if subplotNum:
        plt.subplot(subplotNum[0], subplotNum[1],subplotNum[2])
        if (subplotNum[2]>subplotNum[0]*subplotNum[1]-subplotNum[0]):
            plt.xlabel(xlabel_s)
    else:
        plt.xlabel(xlabel_s)
    plt.title(title_s)
    plt.ylabel(ylabel_s)
    return fig
#######################################################
# #helper function borrowed from the internet to import json as ASCII not as unicode
# def _byteify(data, ignore_dicts = False):
#     # if this is a unicode string, return its string representation
#     if isinstance(data, unicode):
#         return data.encode('utf-8')
#     # if this is a list of values, return list of byteified values
#     if isinstance(data, list):
#         return [ _byteify(item, ignore_dicts=True) for item in data ]
#     # if this is a dictionary, return dictionary of byteified keys and values
#     # but only if we haven't already byteified it
#     if isinstance(data, dict) and not ignore_dicts:
#         return {
#             _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
#             for key, value in data.iteritems()
#         }
#     # if it's anything else, return it in its original form
#     return data
###############################################################################
if __name__ == "__main__":
    main()