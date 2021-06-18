
import random
import threading
import subprocess
import time,os
from dialog import Dialog
from audioManager import AudioRecorder
from pathlib import Path
import face_recognition
import cv2
import numpy as np
from subprocess import PIPE, run

from dialog import Dialog

class FaceRecognition(object):
    def __init__(self, audio_recorder):
        """if audio_recorder is None:
            print("none param")
            self.audio_recorder = AudioRecorder(Dialog())
        else :"""
        self.audio_recorder = audio_recorder
        threading.Thread(target=self.run).start()

    def run(self):
        
        self.detecter = False
  
        self.discute = False
        self.dialog = Dialog()
        self.unknown_file = {"inconnu":0}
        self.known_file = {"percent":0,"name":"inconnu"}
        self.existe = {}
        self.pre_nom_detecter = ""
        self.new=False
        with open("unknown","w") as f : f.write(str(self.unknown_file))
        with open("known","w") as f : f.write(str(self.known_file))
        with open("existe","w") as f : f.write(str(self.existe))
        with open("new","w") as f : f.write(str(self.new))
        threading.Thread(target=lambda: subprocess.Popen("python3 face_system/facerec.py",shell=True)).start()
        self.check_unknown()

        

    def check_unknown(self):
        # print("ici")
        
        while True :
            if (self.discute==False) : 
                with open("known", "r") as f :  self.known_file = eval(f.read())
                with open("existe","r") as f : self.existe=eval(f.read())
                self.detecter=self.known_file["percent"]>40
                name=self.known_file["name"]
                if self.detecter and self.pre_nom_detecter !=name : 
                # if self.detecter and self.pre_nom_detecter !=name and name not in self.existe: 
                    self.pre_nom_detecter = self.known_file["name"]
                    if self.dialog.attente_isplein: continue 
                    else :
                        print("envoi de message ...")
                        self.dialog.process_init("salut je suis " + self.pre_nom_detecter)
                        # self.dialog.send_user_msg_to_chatbot("salut je suis " + self.pre_nom_detecter)
                        # self.dialog.add_file_attente(self.dialog.response)
                        #self.dialog.add_file_attente("Bonjour "+self.pre_nom_detecter)

                        # self.dialog.SpeakText("Bonjour "+self.pre_nom_detecter)
                        if name not in self.existe : 
                            self.existe[name]=self.detecter
                            with open("existe","w") as f : f.write(str(self.existe))
                    # subprocess.Popen("py -3.5 dialog.py --input \"je suis "+self.known_file["name"]+"\"", shell=True)
                    continue

                with open("unknown","r") as f : self.unknown_file=eval(f.read())
                # if self.unknown_file["inconnu"] > 60 :
                #     self.discute=True
                #     self.train_model()

                #     self.discute=False
                
            time.sleep(1)

    def train_model(self):
        if self.dialog.attente_isplein: return 
        else : 
            # self.audio_recorder.pause=True
            with open("is_lecture", "w") as f : f.write("True")
            self.dialog.add_file_attente("Bonjour, je ne vous connais pas")
            # self.dialog.SpeakText("Bonjour, je ne vous connais pas")
            time.sleep(1000)
            # nom="lol"
            nom = self.audio_recorder.simple_recognize("quel est votre nom ?")
            if nom is None : print("entrainement incomplet")
            else:
                print("son nom : "+str(nom))
                if nom=="inconnu" or nom =="" or len(nom)<2 or nom is None:
                    if self.dialog.attente_isplein : return 
                    else : self.dialog.add_file_attente("desolé je n'est pas saisie votre nom")
                    # if not self.dialog.en_lecture :  self.dialog.SpeakText("desolé je n'est pas saisie votre nom")
                else :
                    if not self.dialog.en_lecture : self.dialog.SpeakText("enchanté "+nom)
                    self.take_photo(nom,time.time())
                time.sleep(1000)
                # self.audio_recorder.pause=False
                with open("is_lecture", "w") as f : f.write("False")
                self.unknown_file ={"inconnu":0}
                with open("unknown","w") as f : f.write(str(self.unknown_file))
                print("entrainement terminé")
    def take_photo(self,name, date):
        print("enregistrement de "+name+"\ndate: "+str(date))
        # video_capture = cv2.VideoCapture(0)
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("saving")
        directory = "face_system/images/" + name + "/"
        t = 0
        take = False
        while t < 4 or take == False:
            ret, frame = cam.read()
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
                    self.new=True
                    take = True

                else:
                    print("Image not OK to save ")
            time.sleep(2)
            t += 2
        if self.new==True : 
            with open("new","w") as f : f.write(str(self.new)) 
        cam.release()
        cv2.destroyWindow("saving")
        print("sauvé")

#s=FaceRecognition()
