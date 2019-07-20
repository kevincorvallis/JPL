#!/tps/bin/python -B

import os, sys, json, re
from math import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

def main():
    # ------------------------------------- Open json file --------------------------------------------
    inputFilename = 'submasterDurations_sols2170to2395_postUpdate.json'
    with open(inputFilename) as fp:
        data = json.load(fp)
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


###############################################################################
if __name__ == "__main__":
    main()