from collections import OrderedDict
from datetime import datetime, timedelta
import requests
import json
import socket
import os
import time


sourcePath = "/home/pi/Documents/intelisa/"

awsIP = 'https://login.intelisa.in/'   #For Mahindra
#awsIP = 'http://3.14.137.73:3000/'   #For Demo
addpath = "/home/pi/Documents/Adds/"
vdoDwnPath = "https://s3.ap-south-1.amazonaws.com/rahuls4u/"

def checkInternet():
  REMOTE_SERVER = "www.google.com"
  try:
    # see if we can resolve the host name -- tells us if there is a DNS listening
    print "Checking for Internet, checkInternet()!!!!"
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except Exception as e:
     print e
     return False
     #pass


def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return str(cpuserial)

def getIP():
	import socket    
	hostname = socket.gethostname()    
	IPAddr = socket.gethostbyname(hostname + '.local')    
	#print("Your Computer Name is:" + hostname)    
	#print("Your Computer IP Address is:" + IPAddr)
	return str(IPAddr) 


def dwnLoad(ads):
	print ads
	try:
		if((os.path.exists(addpath + 'ss/' + str(ads)))):
            		pass
		else:
			if(checkInternet()):
				r = requests.get(vdoDwnPath + str(ads),timeout = 20) ###################
				if r.status_code == 200:
					os.system('rm -rf' + ' ' + addpath + 'ss/*')
					#os.system('mkdir ss')
					with open(addpath + 'ss/' + str(ads),'wb') as f:
						f.write(r.content)
						time.sleep(0.5)
						os.system('cp' + ' ' + addpath + 'ss/' + str(ads) + ' ' + addpath + 'ss/'+ 'logo1.jpg')
						os.system('reboot')
			else:
				pass
	except Exception as e:
		#logging.info('Video Download Error==>' +str(e))
		print "Bhaiya Ye Error Hai===>",e
		pass


def setWalpaper(data):
	#print "Entering 1+++++++"
	if('screenSaver' in data):
		print "Checking for ScreenSaver"
		dwnLoad(data['screenSaver'])
		"""
		try:
			#print "Done Checking"
			#os.system('pcmanfm --set-wallpaper /home/pi/Documents/Adds/logo1.jpg')

		except Exception as e:
			print e
			pass
		"""
	else:
		return



def getMetaData():
	msgBody = {
	"deviceIMEI":getserial(),
	"deviceIP":getIP()
	}
	print msgBody
	try:
		url = awsIP + 'api/device/updateDeviceIP'
		response = requests.post(url,msgBody)
		__data = json.loads(response.text)
		#print __data

		with open(sourcePath + 'metaDataV2.txt', 'w') as outfile:  
                	json.dump(__data, outfile)

		#print __data
		setWalpaper(__data)
		return __data
	except:
		pass


if __name__ == "__main__":
	print getMetaData()['_id']
	print checkInternet()
	#getIP()
