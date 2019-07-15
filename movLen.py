from subprocess import  check_output, CalledProcessError, STDOUT 
import math

def getDuration(filename):

    command = [
        'ffprobe', 
        '-v', 
        'error', 
        '-show_entries', 
        'format=duration', 
        '-of', 
        'default=noprint_wrappers=1:nokey=1', 
        filename
      ]

    try:
        output = check_output( command, stderr=STDOUT ).decode()
    except CalledProcessError as e:
        output = e.output.decode()

    return float(output)

if __name__ == "__main__":
	fn = '/home/pi/Documents/Adds/1555394752815-cero.mp4'
	print getDuration(fn)
