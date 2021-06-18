import face_recognition
import cv2
import numpy as np

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
print("face started")
base_path = "face_system/images/"
# Load a sample picture and learn how to recognize it.
serveur_image = face_recognition.load_image_file(base_path+"serveur.jpeg")
serveur_face_encoding = face_recognition.face_encodings(serveur_image)[0]

aurel_image = face_recognition.load_image_file(base_path+"aurel.jpeg")
aurel_face_encoding = face_recognition.face_encodings(aurel_image)[0]

roxane_image = face_recognition.load_image_file(base_path+"roxane.jpeg")
roxane_face_encoding = face_recognition.face_encodings(roxane_image)[0]

leonce_image = face_recognition.load_image_file(base_path+"leonce.jpeg")
leonce_face_encoding = face_recognition.face_encodings(leonce_image)[0]

vassindou_image = face_recognition.load_image_file(base_path+"vass.jpeg")
vassindou_face_encoding = face_recognition.face_encodings(vassindou_image)[0]

wodie_image = face_recognition.load_image_file(base_path+"wodie.jpg")
wodie_face_encoding = face_recognition.face_encodings(wodie_image)[0]

habib_image = face_recognition.load_image_file(base_path+"habib.jpeg")
habib_face_encoding = face_recognition.face_encodings(habib_image)[0]
# Create arrays of known face encodings and their names
known_face_encodings = [
    serveur_face_encoding,
    aurel_face_encoding, 
    roxane_face_encoding,
    leonce_face_encoding,
    wodie_face_encoding,
    habib_face_encoding,
    vassindou_face_encoding
]
known_face_names = [
    "Serveur",
    "Aurel",
    "Roxane",
    "Léonce Kone , Manager Senior ODA",
    "Franck Wodie , Manager Senior ODC",
    "Habib Bamba , DTDM",
    "Vassindou Toure , Manager ODA",
    
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        if len(face_encodings)>0 :
            with open("detecter","w") as f : f.write("True")
        face_names = []
        for face_encoding in face_encodings:
            print("visage trouvé")
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
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

            face_names.append(name)
            if(name!="inconnu"):  
                with open("known","w") as f : f.write("{'percent':50,'name':'"+name+"'}")
            else : 
                with open("unknown","w") as f : f.write("{'inconnu':70}")
            print(name)
    process_this_frame = not process_this_frame


    
    # Display the resulting image
    #cv2.imshow('Video', frame)
    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
