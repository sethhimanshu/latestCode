import cv2
import datetime

sourcePath = "/home/pi/Documents/"

#Given an image below function returns rectangle for face detected alongwith gray scale image
def faceDetection(test_img):
    gray_img=cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)#convert color image to grayscale
    face_haar_cascade=cv2.CascadeClassifier('/home/pi/Documents/intelisa/haarcascade_frontalface_default.xml')#Load haar classifier
    faces=face_haar_cascade.detectMultiScale(gray_img,scaleFactor=1.32,minNeighbors=5)#detectMultiScale returns rectangles

    return faces,gray_img


def main():
    try:
        cam = cv2.VideoCapture(0)
        ret, image = cam.read()
        __image = cv2.resize(image, (1280,720))
        
        cam.release()
        
        faces_detected,gray_img=faceDetection(__image)
		#print "Total time taken:{0} Sec".format(math.ceil(time.time() - start)) 
        print("faces_detected:",len(list(faces_detected)))
		#return len(list(faces_detected))

        for (x,y,w,h) in faces_detected:
            cv2.rectangle(__image,(x,y),(x+w,y+h),(255,0,0),thickness=5)


        resized_img=cv2.resize(__image,(1000,1000))
        #cv2.imshow("face dtecetion tutorial",__image)
        #cv2.waitKey(0)#Waits indefinitely until a key is pressed
        #cv2.destroyAllWindows
        cv2.imwrite(sourcePath + 'pics/' + str(datetime.datetime.now()) + '.jpg',__image)
        return len(list(faces_detected))
        
    except Exception as e:
        print e
        return 0

if __name__ == "__main__":
    main()

