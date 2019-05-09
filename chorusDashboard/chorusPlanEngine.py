# Import Libraries
from openpyxl import load_workbook
import csv
import os
#import requests
import urllib
import cgi
import re
import urllib.request
from urllib.request import urlopen
from urllib.request import urlretrieve
import base64
import uuid
import http.client
from http.client import HTTPSConnection
import json
from datetime import datetime, date, timedelta
import dateutil
from dateutil import parser
from dateutil.parser import parse
import couchdb

# Global Variables
#unplannedIncidents_list = []
currentImpactsID_list = []
cgwImpact_list = []
rowList_list2 = []
eventID_list = [] ## <----- for HTML Output aswell

# Current Incident Variables
#currentCustomer = "-"
currentEventDur = "-"
currentEventStart = "-"
currentEventEnd = "-"
currentReason = "-"
currentStatus = "-"
currentArea = "-"

# Database setup
#couch = couchdb.client.Server('http://tailsdb.vocusgroup.co.nz:5984')
#tailsDB = couch['tails']
#outageDB = couch['outage']
#servicesDB = couch['services']

# Chorus Events Overview Pull
def vocusOverview(event_id):
    # Generate X-ID
    xID = uuid.uuid4()
    # Encode userID and client secret
    encode = base64.b64encode(b'9ddf0e5cebee45d89458ef782ce73d2e:2f70008670Ac4a409e7811468459b859')

    headers = {'Authorization': 'basic' + str(encode), 'X-Transaction-Id': str(xID)}

    # This sets up the https connection
    conn = http.client.HTTPSConnection("api.chorus.co.nz")

    conn.request('GET', '/network-events/v1/events/'+event_id, headers=headers)

    res = conn.getresponse()

    data = res.read()
    #print(res.status, res.reason)
    #print(data.decode('utf-8'))
    #print(res.getheaders())
    jsonParsed = json.loads(data.decode('utf-8'))
    global currentEvent
    currentEvent = event_id
    if res.status == 404:
        print("No Vocus Impact")
        ## Needed for table
        global currentEventDur
        currentEventDur = "N/A"
        global currentEventStart
        currentEventStart = "N/A"
        global currentEventEnd
        currentEventEnd = "N/A"
        global currentReason
        currentReason = "N/A"
        #start_List.append(dateConverter(currentEventStart))
        #start_List.append(currentEventStart)
        #end_List.append(dateConverter(currentEventEnd))
        #end_List.append(currentEventEnd)
        #duration_List.append(currentEventDuration)
        #reason_List.append(currentReason)
    else:
        currentEventDur = jsonParsed["outageDuration"]
        currentEventStart = dateConverter(jsonParsed["startTime"]) #convert date/time
        currentEventEnd = dateConverter(jsonParsed["endTime"])     #convert date/time
        currentReason = jsonParsed["updates"]
        global currentStatus
        currentStatus = jsonParsed["status"]
        #currentNetworkImpactSummary = jsonParsed["networkImpactSummary"]
        global currentArea
        currentArea = jsonParsed["networkImpactSummary"][0]["location"] ## Won't work for events an multiple locations. Will use this for now.

def vocusImpacts(event_id):
    # Generate X-ID
    xID = uuid.uuid4()
    # Encode userID and client secret
    encode = base64.b64encode(b'9ddf0e5cebee45d89458ef782ce73d2e:2f70008670Ac4a409e7811468459b859')

    headers = {'Authorization':'basic'+str(encode), 'X-Transaction-Id':str(xID)}
    #headers = {'Basic OWRkZjBlNWNlYmVlNDVkODk0NThlZjc4MmNlNzNkMmU6MmY3MDAwODY3MEFjNGE0MDllNzgxMTQ2ODQ1OWI4NTk=': '', '14878r9hkjabdnfkajnfvp01834': ''}

    # This sets up the https connection
    #conn = http.client.HTTPSConnection("api.sandbox.chorus.co.nz")
    conn = http.client.HTTPSConnection("api.chorus.co.nz")

    # then connect
    # Impact Download
    conn.request('GET','/network-events/v1/events/'+event_id+'/impactDownload?organisation=Vocus+Communications+Ltd&impactType=Direct', headers=headers)
    # Impact
    #conn.request('GET', '/network-events/v1/events/INC000003709818/impact', headers = headers)

    # get the response back
    res = conn.getresponse()

    # Output
    data = res.read()
    #print(res.status, res.reason)
    #print(data.decode('utf-8'))
    #print(res.getheaders())

    output = str(data.decode('utf-8'))
    output2 = output.replace(",", " ")

    # Add to CurrentImpacts List
    if data.decode('utf-8') != '':
        for i,line in enumerate(output2.splitlines()):
            #print(line)
            if i != 0:
                for i2,word in enumerate(line.split()):
                    if i2 == 0:
                        currentImpactsID_list.append(stripID(word))
                        #print(word)
                        break

def fxNetworksImpacts(event_id):
    # Generate X-ID
    xID = uuid.uuid4()
    # Encode userID and client secret
    encode = base64.b64encode(b'78d96f4de7084c45ba9c60b6d1a717b1:328eD749f184463f9a492DABF924614f')

    headers = {'Authorization':'basic'+str(encode), 'X-Transaction-Id':str(xID)}

    # This sets up the https connection
    # conn = http.client.HTTPSConnection("api.sandbox.chorus.co.nz")
    conn = http.client.HTTPSConnection("api.chorus.co.nz")

    # then connect
    # Impact Download
    conn.request('GET','/network-events/v1/events/'+event_id+'/impactDownload?organisation=FX+Networks+Ltd&impactType=Direct', headers=headers)
    #conn.request('GET', '/network-events/v1/events/'+event_id+'/impact', headers=headers)

    # get the response back
    res = conn.getresponse()

    # Output
    data = res.read()
    #print(res.status, res.reason)
    #print(data.decode('utf-8'))
    #print(res.getheaders())

    output = str(data.decode('utf-8'))
    output2 = output.replace(",", " ")

    # Add to CurrentImpacts List
    if data.decode('utf-8') != '':
        for i, line in enumerate(output2.splitlines()):
            # print(line)
            if i != 0:
                for i2, word in enumerate(line.split()):
                    if i2 == 0:
                        currentImpactsID_list.append(stripID(word))
                        # print(word)
                        break

def maxnetImpacts(event_id):
    # Generate X-ID
    xID = uuid.uuid4()
    # Encode userID and client secret
    encode = base64.b64encode(b'8e6550a89af740439ab963f7c9dd3d3e:51a898F04B49420792f462c0B272672D')

    headers = {'Authorization': 'basic' + str(encode), 'X-Transaction-Id': str(xID)}

    # This sets up the https connection
    # conn = http.client.HTTPSConnection("api.sandbox.chorus.co.nz")
    conn = http.client.HTTPSConnection("api.chorus.co.nz")

    # then connect
    # Impact Download
    conn.request('GET',
                 '/network-events/v1/events/' + event_id + '/impactDownload?organisation=Maxnet&impactType=Direct',
                 headers=headers)

    # get the response back
    res = conn.getresponse()

    # Output
    data = res.read()
    #print(res.status, res.reason)
    #print(data.decode('utf-8'))
    #print(res.getheaders())

    output = str(data.decode('utf-8'))
    output2 = output.replace(",", " ")

    # Add to CurrentImpacts List
    if data.decode('utf-8') != '':
        for i, line in enumerate(output2.splitlines()):
            # print(line)
            if i != 0:
                for i2, word in enumerate(line.split()):
                    if i2 == 0:
                        currentImpactsID_list.append(stripID(word))
                        # print(word)
                        break

def callplusImpacts(event_id):
    # Generate X-ID
    xID = uuid.uuid4()
    # Encode userID and client secret
    encode = base64.b64encode(b'59fc1749a8054a5bb2b2a9c050dc85d0:AD43cDED844F43F6983DC133acadb957')

    headers = {'Authorization':'basic'+str(encode), 'X-Transaction-Id': str(xID)}

    # This sets up the https connection
    # conn = http.client.HTTPSConnection("api.sandbox.chorus.co.nz")
    conn = http.client.HTTPSConnection("api.chorus.co.nz")

    # then connect
    # Impact Download
    conn.request('GET','/network-events/v1/events/'+event_id+'/impactDownload?organisation=Callplus+Limited&impactType=Direct',headers=headers)
    #conn.request('GET', '/network-events/v1/events/'+event_id+'/impact', headers = headers)

    # get the response back
    res = conn.getresponse()

    # Output
    data = res.read()
    #print(res.status, res.reason)
    #print(data.decode('utf-8'))
    #print(res.getheaders())

    output = str(data.decode('utf-8'))
    output2 = output.replace(",", " ")

    # Add to CurrentImpacts List
    if data.decode('utf-8') != '':
        for i, line in enumerate(output2.splitlines()):
            # print(line)
            if i != 0:
                for i2, word in enumerate(line.split()):
                    if i2 == 0:
                        currentImpactsID_list.append(stripID(word))
                        # print(word)
                        break

def orconImpacts(event_id):
    # Generate X-ID
    xID = uuid.uuid4()
    # Encode userID and client secret
    encode = base64.b64encode(b'clientID:clientSecret')

    headers = {'Authorization': 'basic' + str(encode), 'X-Transaction-Id': str(xID)}

    # This sets up the https connection
    # conn = http.client.HTTPSConnection("api.sandbox.chorus.co.nz")
    conn = http.client.HTTPSConnection("api.chorus.co.nz")

    # then connect
    # Impact Download
    conn.request('GET',
                 '/network-events/v1/events/' + event_id + '/impactDownload?organisation=Orcon&impactType=Direct',
                 headers=headers)

    # get the response back
    res = conn.getresponse()

    # Output
    data = res.read()
    # print(res.status, res.reason)
    # print(data.decode('utf-8'))
    # print(res.getheaders())
    output = str(data.decode('utf-8'))
    output2 = output.replace(",", " ")

    # Add to CurrentImpacts List
    if data.decode('utf-8') != '':
        for i, line in enumerate(output2.splitlines()):
            # print(line)
            if i != 0:
                for i2, word in enumerate(line.split()):
                    if i2 == 0:
                        currentImpactsID_list.append(stripID(word))
                        # print(word)
                        break

def loopImpacts():
    for event in eventID_list:
        currentCGWImpact_List = []
        currentCGWImpactSpace_List = []
        CGW_Count = 0

        # Clear id list
        currentImpactsID_list.clear()
        # Load Change Details
        vocusOverview(event)
        # Call each entity for impacts
        vocusImpacts(event)
        fxNetworksImpacts(event)
        callplusImpacts(event)
        # maxnetImpacts(event) #(need to register with Chorus / mulesoft)
        # orconImpacts(event) #(need to register with Chorus / mulesoft)

        # CGW Impact Yes or No?
        for id in currentImpactsID_list:
            CGW = False
            currentCID = id.strip()
            ############################
            # Using couchDB
            ############################
            #rows = tailsDB.view("_design/reconcile/_view/tails_by_service_id", key=currentCID.lower()).rows
            rows = 1  # for testing without couchDB
            #currentCustomer = rows[0].value['customer']['name']
            #if len(rows) >= 1:
            if rows >= 1:
               CGW = True
               currentCGWImpact_List.append(id)
               CGW_Count += 1
               #print(id)
        # Add space to currentCGWImpact_List
        for cid in currentCGWImpact_List:
            currentCGWImpactSpace_List.append(" "+cid)

        # Build List of Row Objects
        if CGW_Count > 0:
           ## Create row object(list of list))
           row = (event, "Yes", CGW_Count, currentCGWImpactSpace_List, currentEventStart, currentEventEnd, currentEventDur, currentReason)
           rowList_list2.append(row)
        else:
            ## Create row object(list of list))
            row = (event, "No", "0", "N/A", "N/A", "N/A", "N/A", "N/A")
            rowList_list2.append(row)

# Helper Methods
def stripID(input):
    stripped = input.replace('PDL', '').replace('IDA', '').replace('POL', '')
    return stripped.strip()

def dateConverter(input):
    if is_date(input) == True:
       datetime_object = datetime.strptime(input, '%Y-%m-%dT%H:%M:%S+12:00')
       converted = datetime_object.strftime("%d-%m-%Y %H:%M:%S")
       return converted
    else:
        return "-"

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    # Check for None type / null
    if string is None:
        return False
    else:
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

def clearStoragePlan():
    #eventID_list.clear()
    #tailsDB_list.clear()
    currentImpactsID_list.clear()
    cgwImpact_list.clear()
    eventID_list.clear()
    rowList_list2.clear()
    #rowList_list.clear()
    #noCGWImpact_list.clear()

    #start_List.clear()
    #end_List.clear()
    #cgwImpactList_List.clear()
    #cgwImpactYesNo_List.clear()
    #cgwCount_List.clear()
    #duration_List.clear()
    #reason_List.clear()

def incidentIDPuller(input):
    for word in input.split(" "):
        #if ('INC' or 'CRQ') in word:
        if "CRQ" in word:
            return word.strip()
        elif "INC" in word:
            return word.strip()
        elif word.startswith('FRE'):# and len(word) == 11:
            return word.strip()
        #else:
            #return "No Incident Found"

def LoadIncidentListFromUserInput(input):
    for word in input.split():
        if incidentIDPuller(word) is None:
           print("Not a valid Chorus ref")
        else:
           eventID_list.append(incidentIDPuller(word))
        #print(incidentIDPuller(word))

# Function Call
