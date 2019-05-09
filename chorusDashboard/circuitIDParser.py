# coding=utf-8
###################
#   Version 1.0   #
###################

## Global Variables
circuitID_list = []
V1NoID_list = []
nonCGW_set = set()
nonCGW_list = []
noCID_set = set()
noCID_list = []
noCIDLessV1_list = []
noDup_set = set()
final_lineID_set = set()
final_lineID_list = []

def readText(input):
    ## Open Text File to Parse
    #file = open(file_name, "r")
    ## Loop Through Each Line Add to Corresponding List
    for line1 in input.splitlines():
      # remove leading and trailing quote marks and hidden character
        line = line1.replace('"',"").replace(','," ").strip()
        # Non CGW Customers
        if(isCGW(line) == False):
           nonCGW_set.add(line.strip())
           #print(line.strip())
        else:
            noDup_set.add(line.strip())
            #print(line)

def circuitIDIn(file_name):
  f1 = open(file_name, "r")
  for line1 in f1:
      # Skip Commented Lines
      if not line1.startswith('#'):
	         #print(line1.strip())
	         circuitID_list.append(line1.strip())

def chorusCheck(input):
    ## 1206, 1207, 1005, 1006, 1636 , 162 - Chorus HSNS & Bitstream
    if((len(input) == 10 or len(input) == 9) and (input.startswith("1206") or input.startswith("1207")
        or input.startswith("1005") or input.startswith("1006") or input.startswith("163") or input.startswith("162")
          or input.startswith("1684") or input.startswith("1694"))):
        return True
    else:
        return False

def chorusCheck2(input):
    ## 181XXX and 183XXX - Chorus DFAS and POL and DFAS-ICAB
    if(len(input) == 6 and (input.startswith("178") or input.startswith("179") or input.startswith("180") or input.startswith("181") or input.startswith("182") or input.startswith("183"))):
        return True
    else:
        return False

def isServiceID(input):
    if((len(input) == 9 or len(input) == 11) and (input.startswith('VCT') or input.startswith('IPW')
        or input.startswith('MET') or input.startswith('NEA') or input.startswith('INE') or input.startswith('VIE')
          or input.startswith('IPT') or input.startswith('DKF'))):
       return True
    else:
        return False

def isCGW(line):
    if (('B+#' in line) or (line.startswith("TN-HSN") | line.startswith("CUST:") | line.startswith("CCCT:") | line.startswith("CCC:")
        | line.startswith("CCC -") | line.startswith("COSMOS:") | line.startswith("Cosmos:") | line.startswith("COSMOS#") | line.startswith("Cosmos#")
            | line.startswith("OR-CLO") | line.startswith("HSNS-") | line.startswith("HSNSp-") | line.startswith("B#") | line.startswith("BP#")
                | line.startswith("Maxnet -") | line.startswith("Maxnet") | line.startswith("MAXNET") | line.startswith("ORCON") | line.startswith("ORCON:"))):
        return False

def isLineV1(input):
    for index, word in enumerate(input.split()):
        if(index == 0 and (word == 'V1' or isServiceID(word) == True)):
           return True
        else:
            return False

def populateV1NoID():
    for line in noCID_set:
        if (isLineV1(line) == True):
           V1NoID_list.append(line)
           #print(line)
        else:
            noCIDLessV1_list.append(line)

def stripID(input):
    ## Strip input of brackets, quote marks, colons and leading identifier
    stripped = input.replace(':', '').replace('(','').replace(')','').replace('[','').replace(']','').replace('"','') \
               .replace('ASID', '').replace('B3a','').replace('Bitstream 2','').replace('Bitstream3','').replace('BS2-','').replace('BS2a','').replace('BS2b','').replace('BS2','')\
                .replace('BS3a','').replace('BS3b','').replace('BS3A', '').replace('BS3', '').replace('DFAS-ICAB','').replace('IDA','').replace('HSNS','').replace('POL','') \
                 .replace('VDSL', '').replace('DFAS','').replace(';','').replace('EUBA','') #.replace('ï¼š','').replace('Â','')
   ## stripped2 = stripped.replace('：', '')
    return stripped.strip()

def clearStorageCIDParser():
    # Python 2.7
    #del circuitID_list[:]
    #del V1NoID_list[:]
    #nonCGW_set.clear()
    #del nonCGW_list[:]
    #noCID_set.clear()
    #del noCID_list[:]
    #del noCIDLessV1_list[:]
    #noDup_set.clear()
    #final_lineID_set.clear()
    #del final_lineID_list[:]

    # Python3+
    circuitID_list.clear()
    V1NoID_list.clear()
    nonCGW_set.clear()
    nonCGW_list.clear()
    noCID_set.clear()
    noCID_list.clear()
    noCIDLessV1_list.clear()
    noDup_set.clear()
    final_lineID_set.clear()
    final_lineID_list.clear()

def circuitIDPuller(input_text):
    ## File to Parse
    readText(input_text)
    ## Loop each line in no duplicate set
    for index, line2 in enumerate(noDup_set):
        foundIDCount = 0
        currentLineIDs = ""
        currentLine_list = []
        ## Loop each line and add to current lines list
        for word in line2.split():
            currentLine_list.append(word)
            #print(word)
        ## Loop Current Line from list
        for index1, word1 in enumerate(currentLine_list):
            #print(word1)
            ## Loop each ID in circuit ID List
            for id in circuitID_list:
                ## ID Space Colon eg ASID : 1005....
                #if (word1 == id and currentLine_list[index1+1] == ":"):
                if (word1 == id and index1 != len(currentLine_list)-1 and currentLine_list[index1 + 1] == ":"):
                    currentLineIDs = currentLineIDs + " " + word1 + currentLine_list[index1+1] + currentLine_list[index1+2]
                    foundIDCount += 1
                    #print(currentLineIDs)
                ## ID Colon Space eg DFAS: 183276
                elif(word1 == id+":" and index1 != len(currentLine_list)-1):
                     currentLineIDs = currentLineIDs + " " + word1 + currentLine_list[index1+1]
                     foundIDCount += 1
                     #print(currentLineIDs)
                ## ID Space eg DFAS 183999
                elif(word1 == id and index1 != len(currentLine_list)-1):
                     currentLineIDs = currentLineIDs + " " + word1 + currentLine_list[index1+1]
                     foundIDCount += 1
                     #print(currentLineIDs)
                ## Normal ID eg POL183052
                elif(id in word1):
                     currentLineIDs = currentLineIDs + " " + word1
                     foundIDCount += 1
                     #print(currentLineIDs)

            ## Condition for Kordia Fibre Circuit eg. Kordia 18062
            if(word1 == 'Kordia' and index1 != len(currentLine_list)-1 and currentLine_list[index1+1].startswith('18')):
               currentLineIDs = currentLineIDs + " " + currentLine_list[index1+1]
               foundIDCount += 1

            ## Condition for Araneo Circuits eg. Araneo Wireless 13047 & Araneo 13047
            if (word1 == 'Araneo' and ((index1 != len(currentLine_list)-1))):
               # for eg. Araneo Wireless 13047
               if(currentLine_list[index1+1] == 'Wireless') and (index1 != len(currentLine_list)-2) and currentLine_list[index1+2].startswith('13'):
                  currentLineIDs = currentLineIDs + " " + currentLine_list[index1+2]
                  foundIDCount += 1
               # for eg. Araneo 13047
               elif(currentLine_list[index1+1].startswith('13') or currentLine_list[index1+1].startswith('12')):
                   currentLineIDs = currentLineIDs + " " + currentLine_list[index1+1]
                   foundIDCount += 1

            ## Chorus IDs 1206, 1207, 1005, 1006 (9 Digits), 1636 (10 digits)
            if (chorusCheck(word1) == True and (currentLine_list[index1-1] != 'ASID' and currentLine_list[index1-1] != 'IDA' and currentLine_list[index1-1] != 'BS3' and currentLine_list[index1-1] != ':')):#(':' not in currentLine_list[index1-1]) )):
                currentLineIDs = currentLineIDs + " " + word1
                foundIDCount += 1
                #print(currentLineIDs)

            ## Chorus ID 183XXX, 6 Digits e.g 183248
            if (chorusCheck2(word1) == True and (currentLine_list[index1-1] != 'POL' and currentLine_list[index1-1] != 'DFAS' and currentLine_list[index1-1] != ':')):#(':' not in currentLine_list[index1-1]) )):
                currentLineIDs = currentLineIDs + " " + word1
                foundIDCount += 1
                #print(currentLineIDs)

        ## Add Circuit IDs to appropriate LIST
        if(currentLineIDs != ""):
           #final_lineID_set.add(currentLineIDs.strip())
           final_lineID_set.add(stripID(currentLineIDs))
           #print(currentLineIDs.strip())

        ## If no ID found add to noID list
        if(foundIDCount == 0 ):
           noCID_set.add(line2.strip())
           #print(line2.strip())

def printOutput():
    ## Print detected IDs
    #print("=====================\nDetected IDs\n=====================")
    for element in final_lineID_set:
        currentLine = ""
        ## Remove Line Duplicates
        for word in element.split():
            if(word not in currentLine):
               currentLine = currentLine + " " + word
        final_lineID_list.append(stripID(currentLine))
    final_lineID_list.sort()
    #for element in final_lineID_list:
        #print(element)
        #print(stripID(currentLine))
        #print(stripID(element))

    ## Print V1 No Circuit ID
    #print("\n===========================\nV1 No Circuit ID: \n===========================")
    V1NoID_list.sort()
    #for element in V1NoID_list:
        #print(element)
    ## Print No CID minus V1 NOCID
    #print("\n===========================\nNo Circuit ID: \n===========================")
    noCIDLessV1_list.sort()
    #for element in noCIDLessV1_list:
        #print(element)

    ## Print lines with no ID detected
    #print("\n=============================\nNo ID Detected(No duplicates):\n=============================")
    #for element in noCID_set:
        ## print(element)
        ## Sort by A-Z lines with no circuit ID detected
        #noCID_list.append(element)
    #noCID_list.sort()
    #for element in noCID_list:
        #print(element)

    ## Print non CGW List
    #print("\n===========================\nNon CGW: \n===========================")
    for element in nonCGW_set:
        #print(element)
        nonCGW_list.append(element)
    nonCGW_list.sort()
    #for element in nonCGW_list:
        #print(element)

# Function Call
#circuitIDIn("circuitID.txt")
#fname = input("Enter File Name:")
#circuitIDPuller(fname)
#populateV1NoID()
#printOutput()

#print(webOut("FXO9999 test"))
#circuitIDPuller("FXO9999")