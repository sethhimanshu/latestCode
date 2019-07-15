from collections import OrderedDict
from datetime import datetime, timedelta
import requests
import json
import socket
sourcePath = "/home/pi/Documents/intelisa/"

awsIP = 'https://login.intelisa.in/'   #For Mahindra
#awsIP = 'http://3.14.137.73:3000/'   #For Demo


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



def getMetaData():
	msgBody = {
	"deviceIMEI":getserial()
	}
	print msgBody
	try:
		url = awsIP + 'api/device/getScreenMetadata'
		response = requests.post(url,msgBody)
		__data = json.loads(response.text)

		with open(sourcePath + 'metaData.txt', 'w') as outfile:  
                	json.dump(__data, outfile)

		#print __data
		return __data
	except:
		pass


if __name__ == "__main__":
	print getMetaData()['_id']
	print checkInternet()
