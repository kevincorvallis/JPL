#!/tps/bin/python -B

import os, sys, json, re
from math import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

def main():
    # ------------------------------------- Initialization and Input Parameters -------------------------------
    inputFilename = 'submasterDurations_sols2170to2395_postUpdate.json'
    # ------------------------------------- Open json file --------------------------------------------
    with open(inputFilename) as fp:
        data = json.load(fp,object_hook=_byteify)
    masterSols = []
    countSBs = 0
    countArmBBs = 0
    for uniqueID in data.keys():
        if data[uniqueID]["masterSol"] not in masterSols: masterSols.append(data[uniqueID]["masterSol"]) 
        if "arm" in data[uniqueID]["backboneType"]: countArmBBs+=1
        if "SB" in data[uniqueID]["backboneType"]: countSBs+=1
    countMasters = len(masterSols)
    aveSBperMaster = float(countSBs)/float(countMasters)
    aveArmBBsperMaster = float(countArmBBs)/float(countMasters)
    print("Total Masters: " + str(countMasters))
    print("Total SBs: " + str(countSBs))
    print("Total Arm BBs: " + str(countArmBBs))
    print("SBs per Master: " + str(aveSBperMaster))
    print("ArmBBs per Master: " + str(aveArmBBsperMaster))

#######################################################
#helper function borrowed from the internet to import json as ASCII not as unicode
def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data
###############################################################################
if __name__ == "__main__":
    main()