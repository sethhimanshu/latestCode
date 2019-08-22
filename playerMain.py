# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 19:37:57 2019

@author: Himanshu Ranjan Seth 
"""

from omxplayer.player import OMXPlayer
#from logging.handlers import TimedRotatingFileHandler
import movLen as ml
import time
import random
import playlistScheduling
import threading
import datetime
import socket
import logging
import os
import faceRecognition as fr
import RPi.GPIO as GPIO
import csv
import config
import json


pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


addsPath = "/home/pi/Documents/Adds/"
sourcePath = "/home/pi/Documents/intelisa/"

try:
	logging.basicConfig(filename= '/home/pi/Documents/intelisa/log/intelisaLog.log',
				level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')
	print "Log File created"

except Exception as e:
	logging.info("Log File Creation Error==>" + str(e))
	pass

schedulePlaylist = []
RRPlaylist = []
companyAdds = ['1.mp4']

def pinValue():
        time.sleep(1)
        try:
                return GPIO.input(pin)
        except Exception as e:
                logging.info("GPIO Read Error==>" + str(e))
                pass 


def checkInternet():
  REMOTE_SERVER = "www.google.com"
  try:
    # see if we can resolve the host name -- tells us if there is a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except Exception as e:
     logging.info('Check Net Error==>' + str(e))
     pass
  return False



def captureImage():
	start = time.time()
	time.sleep(2)
	logging.info("Capturing the Image!!!")
	faces = fr.main()
	logging.info("Done Face Detection!!!")
	done = time.time()
	return (done - start), faces


#==================================================================================================
#To Create Log file of played adds with time and date
#==================================================================================================

def createLog(data):
	try:
		with open( sourcePath + 'log/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv','ab') as __logFile:
                	writer=csv.writer(__logFile)
                	writer.writerows(data)
	except Exception as e:
		logging.info('Report Writting Error' + str(e))
		pass

#==================================================================================================
#This definition simply play the adds and hold the details of current playing adds in currentLogDetails
#    currentLogDetails = [Add Name, Starting Time, End Time]
#==================================================================================================



def killFeh():
	tempPid = os.popen('pidof feh').read()
	fehPid = tempPid.split(" ")
	pidCount = len(fehPid)
	while(pidCount > 1):
		#os.system('kill -9 ' + str(fehPid[len(fehPid)]))
		pidCount = pidCount - 1
		os.system('kill -9 ' + str(int(fehPid.pop())))

lastLogDetails = []

def playVideo(fileName,loop):


	print '*****************************************************************',fileName
	#print "Loop Value==>",loop
	for iteration in range(int(loop)):

		global lastLogDetails
		currentLogDetails = []
		currentLogDetails.append(fileName)
		currentLogDetails.append(datetime.datetime.now().strftime("%I:%M:%S %p"))
        	'''if (config.checkInternet()):
			playlistScheduling.postData([currentLogDetails,lastLogDetails])
		else:
			pass'''

		logging.info(currentLogDetails)
		lastLogDetails = []


		if('https://' in fileName or 'http://' in fileName):

                        try:
                                print ("Going To Play HTTP:")
                                os.system('pkill feh')
                                os.system('killall  omxplayer.bin')
				txt = 'timeout ' + str(30)+' chromium-browser -incognito -kiosk --disable-infobars --no-sandbox ' + fileName
				#print "Finla URL$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",txt
                                os.system(txt)
                                #Add Log Details
                                break

                        except Exception as e:
                                logging.info('Web Page Error==>' + str(e))
                                pass
		
		elif('.mp4' in fileName):

			try:
				print "going to play"
        	                os.system('pkill feh')
				#time.sleep(3)

				player = OMXPlayer(addsPath + fileName)
        			player.set_aspect_mode('stretch')
				#timeElapsed, faces = captureImage()
				#time to run add
				duration = ml.getDuration(addsPath + fileName)
				if (config.checkInternet()):
					playlistScheduling.postData([currentLogDetails,lastLogDetails])
				else:
					pass
        			time.sleep(duration) # - timeElapsed )
				print "player quit"
        			player.quit()


				currentLogDetails.append(datetime.datetime.now().strftime("%I:%M:%S %p"))
				faces = 0
				currentLogDetails.append(faces)
				#print currentLogDetails
				logging.info(currentLogDetails)
				createLog([currentLogDetails])
				lastLogDetails = list(currentLogDetails)
				os.system('killall omxplayer.bin')


			except Exception as e:
				logging.info('OMX Player Error' + str(e))
				faces = 0
				pass
				#return



		elif('.jpg' in fileName or '.jpeg' in fileName or '.png' in fileName):
			
			try:
		        	os.system('('"feh -Z -F -Y " + addsPath + fileName + '&)')# + '&&(sleep ' + str(loop) + ')')
				faces = 0
				time.sleep(2)
				killFeh()
				#os.system('pkill feh')
				if (config.checkInternet()):
					playlistScheduling.postData([currentLogDetails,lastLogDetails])
				else:
					pass
				
				time.sleep(int(loop) - 2)
				
				currentLogDetails.append(datetime.datetime.now().strftime("%I:%M:%S %p"))
				currentLogDetails.append(faces)
				#print currentLogDetails
				logging.info(currentLogDetails)
				createLog([currentLogDetails])
				lastLogDetails = list(currentLogDetails)
				break

			except Exception as e:
				logging.info('Feh Error==>' + str(e))
				pass

		elif('.gif' in fileName):
			try:
				os.system('pkill feh')
				os.system('killall  omxplayer.bin')
				os.system("mplayer -fs -loop "+ str(loop) + " "  + addsPath + fileName)

				#Add Log Details
				break

			except Exception as e:
                                logging.info('Gif Player Error==>' + str(e))
                                pass
		"""
		elif('https://' in fileName or 'http://' in fileName):

			try:
				print ("Going To Play HTTP:")
                                os.system('pkill feh')
                                os.system('killall  omxplayer.bin')
				os.system('timeout 20 chromium-browser -kiosk ' + fileName)
                                #Add Log Details
                                break

                        except Exception as e:
                                logging.info('Web Page Error==>' + str(e))
                                pass

		"""

	"""
	try:
                print "going to play"
                os.system('pkill feh')
        except:
                pass
	"""
	#print "Going to update !! Video Player"
	#updatePlaylist()
	#time.sleep(2)
        return


#==================================================================================================
# This definition will schedule the next Add to paly based on the follwoing conditions:
# 1). if Scheduled Playlist if empty then it will play the Adds from RRplaylist randomply
# 2). if RRPlaylist is also empty then it will play the Adds from company paly list. Company play list 
#     contains our company's ad which will never be empty because Ads are stored in local memory   
#==================================================================================================

def playAdds():

    while True:
	updatePlaylist()
	print "SchedulePlaylist==>",schedulePlaylist
	print "RR Playlist==>",RRPlaylist
	
        if(len(schedulePlaylist) <> 0 ):
	    i = 0
	    while(i < len(schedulePlaylist)):
		playVideo(schedulePlaylist[i][0],schedulePlaylist[i][1])
		i = i+1

	    if (len(RRPlaylist) <> 0):
		randIndex = random.randrange(0,len(RRPlaylist))
               	playVideo(RRPlaylist[randIndex][0],RRPlaylist[randIndex][1])


        elif(len(schedulePlaylist) == 0):
            if (len(RRPlaylist) <> 0):
		tempLen = len(schedulePlaylist)
		for rrAdds in RRPlaylist:
			print 'now playing==>',rrAdds
                	playVideo(rrAdds[0],rrAdds[1])

                	if(len(schedulePlaylist) <> tempLen):
				print 'Checking for Scheduled Playlist'
				break
			else:
				continue
            else:
		#updatePlaylist()
		#os.system("mplayer -fs /home/pi/Documents/Adds/default.gif &")
		#time.sleep(5)
		#playVideo(' ',1)
		try:
			os.system('pkill feh')
		except:
			print "No Video is Scheduled"
		try:
			os.system('killall  omxplayer.bin')
		except:
			print "No Video is Scheduled"


#==========================================================================================
# The updatePlaylist definition will update schedulePlaylist and RRplaylist whenever called
# according to current slot
#==========================================================================================

def updatePlaylist():
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d')
    mixedPlayList = playlistScheduling.getPlayList(playlistScheduling.getCurrentSlot(),currentTime)
    
    logging.info("Mixed Playlist")
    logging.info(mixedPlayList)
    
    global schedulePlaylist
    schedulePlaylist = list(mixedPlayList[0])
    #logging.info("SChedul Playlist")
    #logging.info(schedulePlaylist)
    #if(len(mixedPlayList[1]) <> 0):
    global RRPlaylist
    RRPlaylist = list(mixedPlayList[1])
    #logging.info("RR Playlist")
    #logging.info(RRPlaylist)
    #print "RR List has been updated"
    #else:
    #print "RR list is empty==>{0}".format(RRPlaylist)

#==========================================================================================
# The ListUpdateNextSlot keep ready the playlist for next slot before 15 minutes of the
# starting of that slot. If minutes is in between 45 to 55 then it will fetch the playlist
# for next slot and download it as thread.
# As this definition detects the change of the slot immediately update the both playlist.
#==========================================================================================

def LocalListUpdate():

	currentTime = datetime.datetime.now()

	if(currentTime.minute > 45 and currentTime.minute < 59):
		print "Checking for update for Next Slot"
		playlistScheduling.updateLocalPlaylist()
		logging.info("Updating the local List, slot about to change")
	else:
		print "Condition Invalid"
		return


def ListUpdatePerMinute():
	sleepTime = 5
	while True:
		logging.info("!!!!Updating the List !!!!!!!")
		if(len(schedulePlaylist) == 0 and len(RRPlaylist) == 0):
			sleepTime = 5
		else:
			sleepTime = 5

		#LocalListUpdate()
		updatePlaylist()
		time.sleep(sleepTime)



def SetTime():
	while(True):
		if(config.checkInternet()):
			os.system("sudo /etc/init.d/ntp stop")
			time.sleep(0.5)
			os.system("sudo ntpd -q -g")
			time.sleep(0.5)
			logging.info('Server Time update==>' + datetime.datetime.now().strftime('%Y-%m-%d#%I:%M:%S %p'))
			time.sleep(18000)
		else:
			time.sleep(18000)

def dwnVdo():
	while True:
		try:
			print "Going to download!12!!"
			playlistScheduling.dwnVideo()
		except Exception as e:
			logging.info('VDO DWN thread Error==>' + e)
			pass
		time.sleep(5)



if __name__ == "__main__":
	try:
		if(config.checkInternet()):
			metaData = config.getMetaData()
		else:
			with open(sourcePath + 'metaData.txt') as json_file:
				metaData = json.load(json_file)
		#print metaData 
		screenID = metaData["_id"]
		#screenID = "5d26c7975a22f73faaab24f5"
		print screenID
		playlistScheduling.setScreenID(str(screenID))
		if(pinValue()):
		#if(checkInternet()):
			logging.info('Script Start Time==>' + datetime.datetime.now().strftime('%Y-%m-%d#%I:%M:%S %p'))
			time.sleep(0.5)
			#playlistScheduling.updateLocalPlaylist()
			#updatePlaylist_10Days()

			playlistScheduling.updateLocalPlaylist_numDays(10)



			playerThread = threading.Thread(target=playAdds)
			updateThread = threading.Thread(target=dwnVdo)


			updateThread.start()
			playerThread.start()



			updateThread.join()
			playerThread.join()


		else:
			print "Jumper is Set to Low, Exiting the program"
			exit()


	except Exception as e:
		print "MainError", e
		pass

