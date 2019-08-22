
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 01:01:37 2019

@author: HRS
"""

from __future__ import division
from collections import OrderedDict
from datetime import datetime, timedelta
import requests
import os
import json
import math
import datetime
import logging
import config


#==============================================================================
# Define the gap between two slots in minutes 
#==============================================================================

slotTimeGapMinute = 60

#screenID = "5d26c7975a22f73faaab24f5"  #BLR
#screenID = "5cbc85b0d556d14bbe8a5e15"  #Hdrbad
screenID = " "  #Delhi
deviceIMEI = " "
awsIP = 'https://login.intelisa.in'     #For Mahindra
#awsIP = 'http://3.14.137.73:3000'      #For Demo

dayCount = 1
playList = {}

#==============================================================================
# Video Download path
#==============================================================================
vdoDwnPath = "https://s3.ap-south-1.amazonaws.com/rahuls4u/"
addpath = "/home/pi/Documents/Adds/"
sourcePath = "/home/pi/Documents/intelisa/"

logging.basicConfig(filename='/home/pi/Documents/intelisa/log/intelisaLog.log',
                        level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')




adGroup = {}

currentAdData = {
                      "adName": " ",
                      "adGroup": " ",
                      "starttime": " "

                       }

lastAdData = {
                      "adName": " ",
                      "adGroup": " ",
                      "starttime": " ",
                      "endTime": " ",
                      "impressions": " ",
                      "status":"1",
                      "duration":"30"
                    }

report_Data = {
  "screenID": "",
  "scheduleDate": datetime.datetime.now().strftime('%Y-%m-%d'),
  "deviceIMEI": "",
  "nowPlaying": "",
  "lastPlayed" : ""
}


def findAdGroup(adName):
    for adG in adGroup:
        if adName in  adGroup[adG]:
            return adG


def postData(loginfo):  #logInfo =  [[current],[last]]  ==> [[Add Name, Starting Time],[Add Name, Starting Time, End Time, Impressions]] 


    postURL = awsIP + '/api/savePlayReport'

    currentAd = dict(currentAdData)
    lastAd = dict(lastAdData)
    tempReport = dict(report_Data)

    currentAd['adName'] = loginfo[0][0]
    currentAd['adGroup'] = findAdGroup(loginfo[0][0])
    currentAd['starttime'] = loginfo[0][1]

    if (len(loginfo[1]) > 0 ):

        lastAd['adName'] = loginfo[1][0]
        lastAd['adGroup'] = findAdGroup(loginfo[1][0])
        lastAd['starttime'] = loginfo[1][1]
        lastAd['endTime'] = loginfo[1][2]
        lastAd['impressions'] = loginfo[1][3]

    else:
        lastAd['adName'] = '0'
        lastAd['adGroup'] = '0'
        lastAd['starttime'] = '0'
        lastAd['endTime'] = '0'
        lastAd['impressions'] = '0'


    tempReport['nowPlaying'] = currentAd
    tempReport['lastPlayed'] = lastAd
    tempReport['screenID'] = screenID
    tempReport['deviceIMEI'] = deviceIMEI


    #print "Temp Data",tempReport
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post(postURL,data = json.dumps(tempReport),headers = headers,timeout=5)
        #print "Responce===>>>",res.text

    except Exception as e:
        logging.info('Report Post Error==>' +str(e))
        pass


#=========================================================================================
# The 'dwnVideo' definition will ensure the Adds in currentSlotPlaylist are there in local
# memory. If it is not there then it will download the required file from cloud   
#=========================================================================================
deltaslot = 0
deltatime = 0

def dwnVideo():
    #print "Playlist==>",currentSlotPlaylist
    print "Going to download!!!"
    webservice_url_st = awsIP + '/api/updateAdScreenStatus'
    print "Going to download!678!!"
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
    currentSlot = getCurrentSlot()

    currentSlotPlaylist = getPlayList(currentSlot,currentTime)

    global deltatime
    global deltaslot
    global screenID
    print screenID
    deltaslot = deltaslot + 1
    print "Going to download!67289!!"
    if(deltaslot >= 24) :
        deltaslot = 0
        deltatime = deltatime + 1
        if(deltatime > 30) :
            deltatime = 0
    print "Going to download!67289!!"
    NextTime = (datetime.datetime.now() + timedelta(days = deltatime)).strftime('%Y-%m-%d')
    print "Going to download!67189!!"
    NxtSlotPlaylist = getPlayList(deltaslot,NextTime)

    print "Going to 21download!6789!!"
    tempAds = []

    for item in currentSlotPlaylist:
    	for recurItem in item:
        	recurItem[0] = str(recurItem[0])
		tempAds.append(recurItem[0])
    print "Going to download!6789!!"
    print tempAds
    for ads in tempAds:
    	if((os.path.exists(addpath + str(ads)))):
            pass
        else:
            try:
                if(config.checkInternet()):
                    data = {"screenID":screenID,"adName":ads,"status":"1"}
                    print data
                    response = requests.post(webservice_url_st,data,timeout = 100)
                    r = requests.get(vdoDwnPath + str(ads),timeout = 900) ###################
                    if r.status_code == 200:
                        with open(addpath + str(ads),'wb') as f:
                            f.write(r.content)
                        data = {"screenID":screenID,"adName":ads,"status":"2"}
                        response = requests.post(webservice_url_st,data,timeout = 100)
                    else:
                        data = {"screenID":screenID,"adName":ads,"status":"0"}
                        response = requests.post(webservice_url_st,data,timeout = 100)
                        pass
            except Exception as e:
                logging.info('Video Download Error==>' +str(e))
                pass

    tempAds = []
    for item in NxtSlotPlaylist:
    	for recurItem in item:
        	recurItem[0] = str(recurItem[0])
		tempAds.append(recurItem[0])
    #print "Current Ads to Check==>",tempAds

    for ads in tempAds:

	if((os.path.exists(addpath + str(ads)))):
            pass
        else:
            try:
                if(config.checkInternet()):
                    data = {"screenID":screenID,"adName":ads,"status":"1"}
                    response = requests.post(webservice_url_st,data,timeout = 100)
                    r = requests.get(vdoDwnPath + str(ads),timeout = 900) ###################
                    if r.status_code == 200:
                        with open(addpath + str(ads),'wb') as f:
                            f.write(r.content)
                        data = {"screenID":screenID,"adName":ads,"status":"2"}
                        response = requests.post(webservice_url_st,data,timeout = 100)
                    else:
                        data = {"screenID":screenID,"adName":ads,"status":"0"}
                        response = requests.post(webservice_url_st,data,timeout = 100)
                        pass
            except Exception as e:
                logging.info('Video Download Error2==>' +str(e))
                pass


    return 


#==============================================================================
# This definition will download and save the playlist of next 10 days.
#==============================================================================

def updateLocalPlaylist_numDays(numDays):
        playList_local = {}
        try:
            with open(sourcePath + 'playListData.txt') as json_file:
                    global playList
                    playList = json.load(json_file)
                    #print playList
        except Exception as e:
            print "File Error==>",e
            pass

        if(config.checkInternet()):
            webservice_url = awsIP + '/api/fetchSchedule'
	    #print "URL",webservice_url 
            for i in range(numDays):
                    __date = (datetime.datetime.now() + timedelta(days = i)).strftime('%Y-%m-%d')
                    data = {"screenID": screenID,"scheduleDate":__date}
                    #print data
                    try:
                            response = requests.post(webservice_url,data,timeout=5)
                            __data = json.loads(response.text)
                            #print "Json Data", __data
                            playList[__date] = __data
                            playList_local[__date] = __data
                            

                    except Exception as e:
                            logging.info('Update Local Playlist Error==>' +str(e))
                            return
            
            with open(sourcePath + 'playListData.txt', 'w') as outfile:  
                    json.dump(playList_local, outfile)
                    playList = playList_local
        else:
            logging.info('No InterNet in Local Playlist update!!!!')
            print "NoNet Sorry, Cann't Update"
	return
    
    
def updateLocalPlaylist():
        #playList = {}
        print "Entering Updating Local Playlist,updateLocalPlaylist()!!!! "
        logging.info("Entering Updating Local Playlist,updateLocalPlaylist()!!!! ")
        
        webservice_url = awsIP + '/api/fetchSchedule'
                
        __date = (datetime.datetime.now().strftime('%Y-%m-%d'))
        data = {"screenID": screenID,"scheduleDate":__date}
        try:
                response = requests.post(webservice_url,data,timeout=5)
                __data = json.loads(response.text)
                global playList
                playList[__date] = __data
                #save Playlist
                
        except Exception as e:
                logging.info('Update Local Playlist Error==>' +str(e))
                return
                
	global dayCount                                
        __date = (datetime.datetime.now() + timedelta(days = dayCount)).strftime('%Y-%m-%d')
        data = {"screenID": screenID,"scheduleDate":__date}
	#print "SCREEN ID==>",screenID
        try:
                response = requests.post(webservice_url,data,timeout=5)
                __data = json.loads(response.text)
                playList[__date] = __data
                dayCount = dayCount + 1
                if(dayCount > 30):
                    dayCount = 1
                   
        except Exception as e:
                logging.info('Update Local Playlist Error==>' +str(e))
                return

        with open(sourcePath + 'playListData.txt', 'w') as outfile:  
                json.dump(playList, outfile)
	return

#==============================================================================
#This definition will return the updated playlist for current slot from local JSON. 
#==============================================================================      

def getPlayList(slotNumber,currentTime):
    
    if(config.checkInternet()):
        print "Updating Local Playlist, getPlaylist()!!!"
        updateLocalPlaylist()
        print "Updating Local Playlist Done, getPlaylist()!!!"
        #currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        logging.info('No Internet!!! in getPlayList')
        print "Cann't Update!!!!"

    try:
        #with open(sourcePath + 'playListData.txt') as json_file:
                #playListData = json.load(json_file)
        #print 'data==>',data
        global playList
        playListData = playList
        print "Hey Playlist==>",playListData

        data = playListData[currentTime]
	print "Current Data:",data
        i = 0
        j = 0
        RRlist = []
        Schdlist = []

        while(i < len(data["schedule"]["roundRobin"])) :
            if (data["schedule"]["roundRobin"][i]["adGroup"] not in adGroup ):
                adGroup[data["schedule"]["roundRobin"][i]["adGroup"]] = []
            RRlist.append([data["schedule"]["roundRobin"][i]["adName"] , data["schedule"]["roundRobin"][i]["iteration"]])
            adGroup[data["schedule"]["roundRobin"][i]["adGroup"]].append(data["schedule"]["roundRobin"][i]["adName"])
            i = i + 1


        while(j < len(data["schedule"]["slot"+str(slotNumber)])) :

            if (data["schedule"]["slot"+str(slotNumber)][j]["adGroup"] not in adGroup ):
                adGroup[data["schedule"]["slot"+str(slotNumber)][j]["adGroup"]] = []
            Schdlist.append([data["schedule"]["slot"+str(slotNumber)][j]["adName"],data["schedule"]["slot"+str(slotNumber)][j]["iteration"]])
            adGroup[data["schedule"]["slot"+str(slotNumber)][j]["adGroup"]].append(data["schedule"]["slot"+str(slotNumber)][j]["adName"])
            j = j + 1

        #print adGroup
        print "Current Playlist==>", [Schdlist,RRlist]
        return [Schdlist,RRlist]    

    except Exception as e:
        print "Error in Get Playlist", e
        logging.info('Get Playlist Error==>' +str(e))
        return [[],[]]



def getCurrentSlot():
    currentTime = datetime.datetime.now()
    return int(math.ceil((currentTime.hour * 60 + currentTime.minute + 0.001) / slotTimeGapMinute))


def setScreenID(__screenID):
	global screenID
	screenID = __screenID




#if __name__ == "__main__":
    
    
    #with open(sourcePath + 'metaData.txt') as json_file:
    	#metaData = json.load(json_file)
    #print metaData 
    
    #screenID = metaData["_id"]
   #dwnVideo()
   # updateLocalPlaylist_numDays(3)
    
    #print "===>>>>>>"
    #updateLocalPlaylist()
    
    #currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
    #rint getPlayList(getCurrentSlot(),currentTime)
    #dwnVideo()
    #dwnVideo('1548595413733-tutorial123.mp4')
