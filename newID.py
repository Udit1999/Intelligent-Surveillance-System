import cv2
import time


def idAdder():
    id=input('Enter your ID: ')
    time.sleep(0.3)
    cam = cv2.VideoCapture(1)
    cam.set(3, 1920)
    cam.set(4, 1080)
    while True:
        ret, im =cam.read()
        im = cv2.flip(im,1)
        cv2.imshow('im',im)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cv2.imwrite(r"DataBase/Registered Person Images/"+id+".jpg",im)
            break
    cam.release()
    cv2.destroyAllWindows()

idAdder()
