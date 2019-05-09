from flask import Flask, render_template, jsonify, request
from unplannedEngine import *
from circuitIDParser import *
from chorusPlanEngine import *

app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/', methods=["GET", "POST"])
def home():
    #vocusUnplanned()
    #loopImpacts()
    #print("lastupdate from app.py "+lastUpdate)
    #lastUpdate1 = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Delay in getting lastUpdate via this method. Threading issue??
    #print("lastupdate from app.py 2 "+lastUpdate_1)
    #return render_template('chorus_unplanned.html', rowList_list = rowList_list, lastUpdate1 = lastUpdate1)
    return render_template('chorus_planned.html')

@app.route('/chorus_unplanned', methods=["GET", "POST"])
def chorusUnplanned():
    clearUnplanned()
    vocusUnplanned()
    loopImpactsUnplanned()
    lastUpdate1 = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Delay in getting lastUpdate via this method. Threading issue??
    return render_template('chorus_unplanned.html', rowList_list=rowList_list, lastUpdate1=lastUpdate1)
    #return render_template('chorus_unplanned.html')  # render a template

@app.route('/cid_filter', methods=["GET", "POST"])
def cidFilter():
    clearStorageCIDParser()
    if request.method == 'POST':
        text = request.form.get('leftOne')
        if text:
            # Calling circuitIDParser Functions
            #clearStorage()
            circuitIDIn("circuitID.txt")
            circuitIDPuller(text)
            populateV1NoID()
            printOutput()
            # Rebuild Print Function for Webpage O/P
            line1 = ("=====================\nDetected IDs\n=====================")
            line2 = ""
            for element in final_lineID_list:
                line2 = line2 + "\n" + element
            line3 = ("\n===========================\nV1 No Circuit ID: \n===========================")
            line4 = ""
            for element in V1NoID_list:
                line4 = line4 + "\n" + element
            line5 = ("\n===========================\nNo Circuit ID: \n===========================")
            line6 = ""
            for element in noCIDLessV1_list:
                line6 = line6 + "\n" + element
            line7 = "\n===========================\nNon CGW: \n==========================="
            line8 = ""
            for element in nonCGW_list:
                line8 = line8 + "\n" + element
            lineTotal = line1 + line2 + "\n" + line3 + line4 + "\n" + line5 + line6 + "\n" + line7 + line8
            # return jsonify(text=text)
            # return flask.jsonify(**text)
            #return lineTotal
            return render_template('cid_filter.html', lineTotal=lineTotal, text=text)
        else:
            return render_template('cid_filter.html', lineTotal="", text="")
    else:
        return render_template('cid_filter.html', lineTotal="", text="")

@app.route('/chorus_planned', methods=["GET", "POST"])
def chorusPlanned():
    if request.method == 'POST':
        text = request.form.get('textbox')
        if text:
            clearStoragePlan()
            LoadIncidentListFromUserInput(str(text).strip())
            loopImpacts()
        #else:
            #return jsonify(text='Input Needed')
        #print(rowList_list)
        return render_template('chorus_planned_out.html', rowList_list2 = rowList_list2)
    return render_template('chorus_planned.html')  # render a template

if __name__ == '__main__':
    app.run(debug=True)
