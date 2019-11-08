#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:40:14 2018

@author: udit
"""
import face_recognition
import cv2
import time
import dlib
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import numpy as np



# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
# Load a sample picture and learn how to recognize it.
video_capture = cv2.VideoCapture(1)
video_capture.set(3, 1920)
video_capture.set(4, 1080)
final_faces = []


def alignface(all_images,all_locations):
    predictor = dlib.shape_predictor("ModelData/shape_predictor_68_face_landmarks.dat")
    fa = FaceAligner(predictor, desiredFaceWidth=256)
     
    faces_in_one_frame = []
    for box in all_locations:
        face_rect = dlib.rectangle(box[3], box[0], box[1], box[2])
        gray = cv2.cvtColor(all_images[0], cv2.COLOR_BGR2GRAY)
        faceAligned = fa.align(all_images[0], gray, face_rect)
        faceAligned = cv2.cvtColor(faceAligned, cv2.COLOR_BGR2RGB)
        cv2.imshow('aligned',faceAligned)
        faces_in_one_frame.append(faceAligned)
    return faces_in_one_frame
	
	
def faceRecogniser(id):
   
    person_image = face_recognition.load_image_file(r"DataBase//Registered Person Images//"+id+".jpg")
    person_image = cv2.cvtColor(person_image,cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(person_image)
    person_face_encoding = face_recognition.face_encodings(person_image,face_locations)[0]
    # Create arrays of known face encodings and their names
    known_face_encodings = [
        person_face_encoding,
    ]
    known_face_names = [
        id,

    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    ts = time.time()
    while ((time.time()-ts)<10):
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        scale_percent = 100 # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        small_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
 
          # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = np.array(small_frame[:, :, :])
        '''
      
        new_image = np.zeros(rgb_small_frame.shape, rgb_small_frame.dtype)
        for y in range(rgb_small_frame.shape[0]):
            for x in range(rgb_small_frame.shape[1]):
                for c in range(rgb_small_frame.shape[2]):
                    new_image[y,x,c] = np.clip(3*rgb_small_frame[y,x,c] + 10, 0, 255)
        rgb_small_frame = new_image[:,:,:]
        '''
      
        #cv2.imshow('rg',rgb_small_frame)
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            '''aligned_face_in_one_frame = alignface([rgb_small_frame],face_locations)
            face_encodings = []
            for face in aligned_face_in_one_frame:
                face_encodings.append(face_recognition.face_encodings(face)[0])'''
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.47)
                name = "Mismatch"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                final_faces.append(name)
                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 1
            right *= 1
            bottom *= 1
            left *= 1

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Face ID', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    d = {final_faces.count(x) : x for x in final_faces}
    # print(d)
    k = list(d.keys())
    sorted(k)
    # print(k[0])
    video_capture.release()
    #cv2.destroyAllWindows()
    try:
        return d[k[0]]
    except:
        return "Not Detected"


#print(faceRecogniser("1822IT1034"))
