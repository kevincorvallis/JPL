#!/tps/bin/python -B

import os, sys, json, re
from math import floor
import elasticsearch, urllib3
from elasticsearch1 import helpers
pwd = os.getcwd()
sys.path.insert(0, '{}/msl-datalytics/src/'.format(pwd))
from spazz import *
# from msldatalytics.src.spazz import *
#from spazz import *

es = elasticsearch.Elasticsearch('https://msl-ops-es.cld.jpl.nasa.gov',sniff_on_start=False)
urllib3.disable_warnings()

global index
index = 'mslice_db'

def main():
    #Query for all submasters.  We want all activity groups (Pie observations) where the seqID field = sub_XXXX in the last 1000 sols.
    # --------------------------------------------- Input Parameters and Initializaton -------------------------------------------------
    # parameters that should eventually be inputs
    verbose = False # a verbose flag that identifies every time a submaster was rejected from the analysis
    filename = 'submasterDurations_sols2170to2395_postUpdate' # name of the .json file output to be used as a pseudo-database
    queryLen = 5000 # how large do we let the query get.  Currently we wouldn't want anything larger than 5000 results
    earliestSol = 2170 # the earliest sol of results we want to include in our data.  With our naming convention for submaster sequences we should only query within modulo 1000
    #note that we changed to the current margin strategy on 2169
    latestSol = 2395
    keepOutSols = range(1759, 1779)+range(2172,2209)+range(2320,2348) # a list of sols we know we don't want to include in the results; 
    #1759-1779 = conjunction; 2172-2209 = 2172 anomaly recovery; 2320-2348 = Safing on RCE-A on 2320 and again on 2339 and subsequent swap to B
    # create some counters that explain the reason for dropping various submasters
    numDuplicateSubsErrors = 0
    numKeepOutSolsErrors = 0
    numSubDatabaseErrors = 0
    numMissingMarginErrors = 0
    numMarginDatabaseErrors = 0
    numMissingActualsErrors = 0
    numMultipleActualsErrors = 0
    # initialize Spazz for a future query
    spazzObj = spazz({'beginTime' : "Sol-" + str(earliestSol) + "M00:00:00",'timeType': "LST"})
    #initialize the query
    # the "not" line should remove all instances of sub_00000
    q = {
        "query": {
            "filtered": {
                "query": { 
                    "bool" : {
                        "must":[
                        { "match": {"seqId":"sub"}}
                        ]
                    }
                },    
                "filter": {
                    "bool":{
                        "must":[
                            {"range" : {
                                "planSol" : {
                                    "gte" : earliestSol,
                                    "lte" : latestSol
                                }
                            }},
                            {"term" : {"Tag" : "activitygroup" }},
                            {"not": {"term" : {"seqId": "00000"}}}
                        ]
                    }
                }
            }
        },
        "size": queryLen,
        "_source": ["seqId","Duration","Children","masterSol", "seqgenDuration"],
        "sort": { "masterSol": { "order": "desc" }}
    }
    # ------------------------------------------ Search ---------------------------------------------------
    #send query to ES and reduce it down to results
    search = es.search(index=index, body=q)
    results = search['hits']['hits']
    totalHits = len(search['hits']['hits'])
    #create a variable to store unidentified backbone child names for troubleshooting
    unidentifiedBackbones = []
    marginNamesSanityCheck = []
    #create a variable to store submaster children when the script couldn' identify the associated margin
    noMarginFoundChildNames = []
    #initialize a new dict to reorganize the information
    submasters = {};
    # ------------------------------ iterate through results; build pseudo database ----------------------------
    # loop through the submasters and populate a new entry in the submasters dict 
    percentComplete = 0
    for jj,result in enumerate(results):
        #print a message every 10% of the results that has been analyzed
        if (jj % (floor(totalHits/10))) == 0:
            print(str(percentComplete) + '% of results processed')
            percentComplete+=10
        seqId = result['_source']['seqId']
        masterSol = int(result['_source']['masterSol'])
        uniqueID = 'sol' + str(masterSol)+'_' + seqId
        # initialize a new entry in the temporary submasters dict for this submaster sequence
        keepSeqId = True
        seqIdDict = {}
        # Skip all EKO's sub_00000; this should never happen so if it does, please warn user
        if seqId == 'sub_00000':
            print('')
            print('ERROR: Found an unexpected sub_00000; this should not be possible with the query.  It will be ignored.')
            print('')
            keepSeqId = False
            continue
        # the user can define keep out sols, such as Conjunction or holiday plannning.  Immediately ignore these sols from analysis as they will skew our data.
        elif masterSol in keepOutSols:
            if verbose:
                print('')
                print('ERROR: Submaster ' + seqId + ' on sol' + str(masterSol) +' falls in the user defined keepOutSols.  It will be ignored.')
                print('')
            keepSeqId = False
            numKeepOutSolsErrors += 1
            continue
        else:
            try:
                # calculate and initialize the planned duration fields
                seqIdDict['seqId'] = seqId
                seqIdDict['masterSol'] = masterSol
                seqIdDict['backboneType'] = []
                seqIdDict['planTotalDur'] = result['_source']['Duration'] 
                seqIdDict['planMarginDur'] = 0
                seqIdDict['uniqueID'] = uniqueID
                # calculate and initialize the seqgen duration fields
                #seqIdDict['totalSeqgenDuration'] = result['_source']['seqgenDuration'] 
                #seqIdDict['totalSeqgenDurationMinutes'] = round(result['_source']['seqgenDuration']/60, 2)
            except:
                if verbose:
                    print('')
                    print('ERROR: Could not identify  Duration field for the submaster ' + seqId)
                    print('Excluding submaster ' + seqId + ' from results')
                    print('')
                keepSeqId = False
                numSubDatabaseErrors+=1
                continue
            # loop through children to identify the backbone type, 
            marginsFound = 0
            # if we find a margin, query for it's duration
            for ii, child in enumerate(result['_source']['Children']):  
                # see if this child has margin in its string identifier
                if 'margin' in child.lower():
                    # there is a templated activity called: APXS Short Standalone with margin + cleanup
                    # If it is that ignore it
                    if 'apxs' in child.lower():
                        seqIdDict['backboneType'].append('unidentified')
                    else:
                        marginsFound+=1
                        # if margin is in the name, identify and extract the id
                        idRegex = r"\(sol\d{5}_tap_end_of_sol_.{22}\)$"
                        idMatch = re.search(idRegex, child)
                        # if you can successfully identify the id, then break it out, else print error message
                        if idMatch:
                            #if you need the name it is here:
                            childName = child[:idMatch.start()]
                            if childName not in marginNamesSanityCheck:
                                marginNamesSanityCheck.append(childName)
                            #grab the child Id, remove the parentheses, so we can identify it in the database
                            childId = child[idMatch.start()+1:idMatch.end()-1]
                            #get margin information with a direct query
                            marginEntry = es.get(id=childId, index=index)
                            try:
                                #store the margin duration as a running sum (for when there are multiple margins associated with a single submaster)
                                seqIdDict['planMarginDur'] += marginEntry['_source']['Duration']
                                continue
                            except: 
                                if verbose:
                                    print('')
                                    print('ERROR: Could not identify a duration for the identified margin activity for submaster ' + seqId)
                                    print('Excluding submaster ' + seqId + ' from results.')
                                    print('Margin activity results were: ')
                                    print(marginEntry)
                                    print('')
                                keepSeqId = False
                                numMarginDatabaseErrors += 1
                                continue
                        else: 
                            if verbose:
                                print('')
                                print('ERROR: Unable to identify an id for the child:' + child + '. Removing submaster ' + seqId + ' from results')
                                print('Child string that was searched:')
                                print(child)
                                print('')
                            keepSeqId = False
                            numMarginDatabaseErrors += 1
                            continue
                # if I can successfully identify a Science Block, then identify that as the type
                elif (('science block' in child.lower()) or ('sb' in child.lower())) and 'SB' not in seqIdDict['backboneType']:
                    seqIdDict['backboneType'].append('SB')
                # if I can successfully identify Post Drive imaging, then identify that as the type
                elif (('pdi' in child.lower()) or ('post-drive imaging' in child.lower())) and 'PDI' not in seqIdDict['backboneType']:
                    seqIdDict['backboneType'].append('PDI') 
                # if I can successfully identify a mobility backbone, then identify that as the type
                elif 'mobility backbone' in child.lower() and 'drive' not in seqIdDict['backboneType']:
                    seqIdDict['backboneType'].append('drive')
                # if I can successfully identify an arm backbone, then identify that as the type
                elif 'arm' in child.lower() and 'arm' not in seqIdDict['backboneType']:
                    seqIdDict['backboneType'].append('arm')
                # identify ECAM imaging
                elif (('slip assessment' in child.lower()) or ('ecam trending' in child.lower())) and 'ECAM' not in seqIdDict['backboneType']:
                    seqIdDict['backboneType'].append('ECAM')
                # ignore dan actives, mahli merges, SAPP_RIMU_DATA_Collection, and SAM activities (for now).
                elif ('dan_active' in child.lower()) or ('mahli merges' in child.lower())or ('sapp_rimu_data_collection' in child.lower()) or ('sam' in child.lower()):
                    seqIdDict['backboneType'].append('otherSci')
                # if I can't identify it as one of the above, then print to screen to help find other problems, and also flag it as unidentified. 
                else:
                    unidentifiedBackbones.append(child)       
                    if 'unidentified' not in seqIdDict['backboneType']:
                        seqIdDict['backboneType'].append('unidentified')
                # if I couldn't find a margin, then throw an error
                if (ii == (len(result['_source']['Children'])-1) and marginsFound == 0):
                    if verbose:
                        print('')
                        print('ERROR: Unable to find a margin associated with ' + seqId + '. Removing submaster ' + seqId + ' from results')
                        print('List of children for ' + seqId + ':')
                        print(result['_source']['Children'])
                        print('')
                    keepSeqId = False
                    noMarginFoundChildNames += result['_source']['Children']
                    numMissingMarginErrors += 1
                    continue
            if keepSeqId:
                # now query for actuals
                hits, _ = spazzObj.get_as_run_sequences(seqids=[seqId])
                if (len(hits) >= 1):
                    actual_found = False
                    for kk, hit in enumerate(hits):
                        #actuals database doesn't have master sol.  It has master seqID and execution start time. Can backsolve with those to determine mastersol:
                        # mstr00XXX is either sol 0XXX,1XXX, or 2XXX.  execution times on 2164 or 2165 may be associated with master sol 2164. 
                        # so borrow the first digit from execution time, and the last three from master sequence ID, and voila, a master sol number
                        actuals_temp_execution_sol = int(hits[kk]['start_lmst'][4:8])
                        mstrSeqId = int(hits[kk]['parent'][4:])
                        actuals_temp_master_sol = mstrSeqId+(actuals_temp_execution_sol//1000*1000)
                        #Now correlate 
                        if actuals_temp_master_sol == seqIdDict['masterSol']:
                            actual_found = True
                            seqIdDict['actActivityDur'] = hits[kk]['dur_earth']
                            #calculate actual margin
                            seqIdDict['actMarginDur'] = seqIdDict['planTotalDur'] - seqIdDict['actActivityDur']
                            break
                    if not actual_found:
                        if verbose:
                            print('')
                            print('ERROR: Found one or more as run durations associated with submaster: ' + seqId + ' on sol ' +str(masterSol)+', ')
                            print('but could not find a corresponding actual duration on this sol. Removing submaster ' + seqId + ' from results')
                            print('')
                        keepSeqId = False
                        numMultipleActualsErrors += 1
                        continue
                else:
                    if verbose:
                        print('')
                        print('ERROR: Unable to find an actual execution duration for submaster:  ' + seqId + '. Removing submaster ' + seqId + ' from results')
                        print('')
                    keepSeqId = False
                    numMissingActualsErrors += 1
                    continue
            if keepSeqId:
                #calculate the activity duration
                seqIdDict['planActivityDur'] = seqIdDict['planTotalDur']-seqIdDict['planMarginDur']                
                submasters[uniqueID] = seqIdDict
    # --------------------------------------- Print Errors and summaries of dropped entries -----------------------------------------            
    print('')
    print('Kept ' + str(len(submasters)) + ' of ' + str(totalHits) + ' for analysis.')
    print('Removed ' + str(numDuplicateSubsErrors) + ' submasters because of duplication in the databse.')
    print('Removed ' + str(numKeepOutSolsErrors) + ' submasters because of user defined keep out sols.')
    print('Removed ' + str(numSubDatabaseErrors) + ' submasters because of errors associated with reading expected fields in the database.')
    print('Removed ' + str(numMissingMarginErrors) + ' submasters because script could not identify the associated margin.')
    print('Removed ' + str(numMarginDatabaseErrors) + ' submasters because there were database issues with the identified margin.')
    print('Removed ' + str(numMultipleActualsErrors) + ' submasters because there were database issues with the identified actual durations (implying it may not have executed).')
    print('Removed ' + str(numMissingActualsErrors) + ' submasters because there were no actuals for the submaster (implying it did not execute).')
    with open(filename + '.json', 'w') as fp:
        json.dump(submasters, fp, sort_keys=True, indent=4, encoding = 'utf-8')
    with open('unidentifiedChildren.json', 'w') as fp2:
        json.dump(unidentifiedBackbones, fp2, sort_keys=True, indent=4)    
    with open('differentNamesforMargin.json', 'w') as fp3:
        json.dump(marginNamesSanityCheck, fp3, sort_keys = True, indent= 4)
    with open('childNamesWhenMissingMargins.json', 'w') as fp3:
        json.dump(noMarginFoundChildNames, fp3, sort_keys = True, indent= 4)
    print('Successfully wrote output to ' + filename + '.json')
    print('Script Complete')
    
    #print(submasters)
        
###############################################################################
#def index_docs(docs):
#    helpers.bulk(es,docs)

###############################################################################
def usage(): #Prints out usage statement
    print("")
    print(sys.argv[0])
    print("Analyzes the durations of Submasters and associated parameters for the Margin Workging Group\n")
    print("USAGE:")

###############################################################################
if __name__ == "__main__":
    main()