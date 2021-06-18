import os
from pathlib import Path
import face_recognition
import cv2
import numpy as np
import time
import subprocess
from subprocess import PIPE, run



users = []
img = []
face_encoding = []
known_face_encodings = []
names = []

basepath = Path('../images/')
def init():
    for folder in basepath.iterdir():
        if folder.is_dir():
            folderName = str(folder.name)
            # Liste des dossiers 
            basepath2 = Path('../images/' + folderName)
            nbre = 0
            
            with os.scandir(basepath2) as files:
                for file in files:
                    if file.is_file() and file.name[0] != ".":
                        nbre += 1
                        imagePath = "../images/" + folderName + "/" + file.name
                        image = face_recognition.load_image_file(imagePath)
                        faceEncodings = face_recognition.face_encodings(image)
                        # face_encoding[folderName + "_" + str(nbre) + "_encoding"] = face_recognition.face_encodings(image)[0]
                        if len(faceEncodings)>0 :
                            face_encoding.append(faceEncodings[0])
                        else:
                            print("Unavailable to load the image "+imagePath)
                        
                        names.append(folderName)

init()
known_face_names = names
for face in face_encoding:
    known_face_encodings.append(face)


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)

video_capture = cv2.VideoCapture(0)

def getImage():
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    users = []
    
    # saveUser("Gerson", "001")
    # getUserImagesNumber("Marc-Aurel")
    
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        with open("new","r") as f : new=eval(f.read())
        if new==True: init()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
                # See how far apart the test image is from the known faces
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                name = "inconnu"
                

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    # print(name)
                    # for i, face_distance in enumerate(face_distances):
                    #     print("L'image de test a une distance de {: .2} de l'image connue #{}".format(face_distance, i))
                    #     print("- Avec un seuil normal de 0,6, l'image de test correspondrait-elle à l'image connue? {}".format(face_distance < 0.6))
                    #     print("Avec un seuil très strict de 0,5, l'image de test correspondrait-elle à l'image connue? {}".format(face_distance < 0.5))
                    #     print()

                face_names.append(name)
                if(name!="inconnu"): 
                    # save(name,'50')
                    with open("known","w") as f : f.write("{'percent':50,'name':'"+name+"'}")
                else : 
                    with open("unknown","w") as f : f.write("{'inconnu':70}")
                # return face_names

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 121, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 121, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

# def save(name,percent):
#     with open("../existe","r") as f : existe=eval(f.read())
#     if name not in existe : existe[nom]=percent
def saveUser(name, date):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("saving")
    directory = "../images/" + name + "/"
    t = 0
    take = False
    while t < 4 or take == False:
        ret, frame = video_capture.read()
        if not ret:
            print("Echec de la capture ")
        else:
            cv2.imshow("test", frame)
            img_name = "image_{}.png".format(date)
            # Path(directory).mkdir(parents=True, exist_ok=True)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=False)
                run("chown -R oda03 " + directory, stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True).stdout
                run("chmod -R 755 " + directory, stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True).stdout
                # run("chmod 755 " + directory, stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True).stdout
            
            if face_recognition.face_encodings(frame):
                cv2.imwrite(directory + img_name, frame)
                run("chown -R oda03 " + directory, stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True).stdout
                run("chmod -R 755 " + directory, stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True).stdout
                # run("chmod -R 777 " + directory + "*", stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True).stdout
                # run("chown ${USER:=$(/usr/bin/id -run)}:$USER " + directory + "*", stdout=PIPE,stderr=PIPE, universal_newlines=True, shell=True).stdout
                print("{} written!".format(img_name))
                take = True
            else:
                print("Image not OK to save ")
        time.sleep(2)
        t += 2
    cam.release()
    cv2.destroyWindow("saving")

def getUserImagesNumber(name):
    directory = "../images/" + name + "/"
    count = 0
    with os.scandir(directory) as files:
        for file in files:
            if file.is_file() and file.name[0] != ".":
                count += 1
    if (count > 0):
        count+=1
    if (count <= 10):
        saveUser(name, "00" + str(count))

def haveUser():
    users = getImage()
    print(users[0])
    #return users[0]

haveUser()
