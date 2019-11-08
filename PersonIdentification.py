
from QrScanner.qr import qrscan
from facerecognition import faceRecogniser
import pyrebase
import cv2
import time
from imutils.video import VideoStream
from IoT import adaIO
from playsound import playsound



config ={
   "apiKey": "**************",
   "authDomain": "**************.firebaseapp.com",
   "databaseURL": "https://**************.firebaseio.com",
   "storageBucket": "****************.appspot.com",

 }

firebase = pyrebase.initialize_app(config)
db = firebase.database()
# md = db.child("mode").get()
# print(md.val())

def clickImage():
    vs = VideoStream(src=1).start()
    time.sleep(2.0)
    frame = vs.read()
    cv2.imwrite("Person.jpg",frame)
    time.sleep(2.0)
    vs.stop()
    return frame


def send_alert(id = "Unknown"):
    img = "Person.jpg"
    print("Sending an alert to the device")
    # db.child("mode").set("0")
    db.child("Cam").child("Ping2").set("1")
    db.child("Cam").child("QRId").set(id)
    storage = firebase.storage()
    storage.child("images").child("Person.jpg").put(img)

def accessControl():
    qrid = qrscan()
    if len(qrid) == 1:
        qrid = qrid[0]
    print(qrid)
    if qrid == "1620IT1110":
            faceID = faceRecogniser(qrid)
            print(faceID)
            if faceID == "Mismatch":
                img = clickImage()
                playsound(r'Sounds/Mismatch Alert.mp3')
                send_alert()
                adaIO.playAlarm()
            elif faceID == "Not Detected":
                print("Not Detected")
                playsound(r'Sounds/Not Detected.mp3')
            else:
                print("Opening the door...")
                playsound(r'Sounds/Opening the door.mp3')
                adaIO.openDoor()
    else:
        try:
            faceID = faceRecogniser(qrid)
            print(faceID)
            if faceID == "Mismatch":
                    img = clickImage()
                    playsound(r'Sounds/Mismatch Alert.mp3')
                    send_alert()
                    adaIO.playAlarm()
            elif faceID == "Not Detected":
                    print("Not Detected")
                    playsound(r'Sounds/Not Detected.mp3')
            else:
                    img = clickImage()
                    print("Requesting for the access...")
                    playsound(r'Sounds/Requesting for access.mp3')
                    send_alert(qrid)
                    time.sleep(3.0)
        except:
            print("You are not registered yet")
            playsound(r'Sounds/Not Registered.mp3')

accessControl()

