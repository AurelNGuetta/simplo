import sys
import os,time
import random
import numpy as np
import queue
import threading
import logging
import speech_recognition as sr
import pyttsx3
import subprocess
from dialog import Dialog

class AudioRecorder():
    def __init__(self, dialog):
        super(AudioRecorder, self).__init__()
        self.value = "inconnu"
        self.dialog = dialog
        self.pause = False
        
        self.recognizer=sr.Recognizer()
        self.microphone=sr.Microphone()
        with open("is_lecture","w") as f : f.write(str(self.pause))
        threading.Thread(target=lambda : self.verif_ecoute()).start()
        
        self.th=threading.Thread(target=lambda : self.recognize_speech_from_mic()).start()
    

    def verif_ecoute(self):
        while 1:
            # time.sleep(0.5)
            with open("is_lecture", "r") as f : self.pause = eval(f.read())
            
    def recognize_speech_from_mic(self): 
        """Transcrit la parole à partir de l'enregistrement du `microphone`.

        Retourne un dictionnaire avec trois clés :
        "success" : un booléen indiquant si la requête API a été ou non
                réussie
        "error" :   `None` si aucune erreur ne s'est produite, sinon une chaîne de caractères contenant
                un message d'erreur si l'API n'a pu être atteinte ou si la
                la parole n'était pas reconnaissable
        "transcription" : `None` si la parole n'a pas pu être transcrite,
                sinon, une chaîne contenant le texte transcrit
        """

        
        # vérifier que les arguments du reconnaissant et du microphone sont de type approprié
        if not isinstance(self.recognizer, sr.Recognizer):
            logging.info('ERROR : recognizer doit être une instance de `Recognizer')
            #raise TypeError("`recognizer doit être une instance de `Recognizer`.")
            self.th.join()
        if not isinstance(self.microphone, sr.Microphone):
            
            logging.info('ERROR : microphone doit être une instance de Microphone')
            self.th.join()
            #raise TypeError("`microphone` doit être une instance de `Microphone` ")

        # régler la sensibilité du recognizer au bruit ambiant et enregistrer l'audio
        # du microphone
        while(True):
            if not self.pause :
            
                print("Je vous écoute...")
                with self.microphone as source:
                
                    if self.pause : break
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    audio = self.recognizer.listen(source)


                # essayer de reconnaître la parole dans l'enregistrement
                # si une exception RequestError ou UnknownValueError est détectée,
                # mettez à jour l'objet réponse en conséquence
                try:
                    print("transcription en cours...")
                    logging.info("transcription en cours")
                    tps1 = time.time()
                    reponse = self.recognizer.recognize_google(
                        audio, language='fr-FR').lower()
                    tps2 = time.time()
                    print("temps de reponse google : "+str(tps2-tps1)+" seconde")
                    self.value=reponse
                    if("sortie" in reponse.lower() or "stop" in reponse.lower() ) :
                        break
                    logging.info("transcription:"+reponse)
                    print(reponse) 
                    if not self.pause :
                        # os.system("python3 dialog.py --input \""+reponse+"\"")
                        self.dialog.process_init(reponse)
                    # os.subprocess()
                    # subprocess.Popen("python3 dialog.py --input \""+reponse+"\"", shell=True)
                    # os.system("python3 dialog.py --input \""+reponse+"\"")
                    print("ok")
                    # time.sleep(1000)
                    

                
                except sr.RequestError:
                    reponse = "que dites vous ?"
                    logging.info("API non disponible")
                    print("non dispo")
                    # self.dialog.SpeakText(reponse)
                except sr.UnknownValueError:
                    reponse = "desolé je n'est pas bien compris"
                    logging.info("Impossible de reconnaître la parole")
                    #self.dialog.SpeakText(reponse)
                
            else : 
                time.sleep(1)
                
                print("voice principale en pause")

            
    def simple_recognize(self, message):
        s=False
        t=0
        reponse =None
        
        while(not s and t<2):

            try:
                # print("votre nom, je vous écoute...")
                with self.microphone as source:
                    
                    print(message)
                    # if self.attente_isplein : 
                    #     time.sleep(1)
                    #     pass 
                    # else :  
                    # self.add_file_attente(message)
                    # time.sleep(2000)
                    self.dialog.SpeakText(message)
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source)
                print("transcription en cours...")
                logging.info("transcription en cours")
                reponse = self.recognizer.recognize_google(
                    audio, language='fr-FR').lower()
                print(reponse) 
               
                if("sortie" in reponse.lower() or "stop" in reponse.lower() ) :
                    break
                logging.info("transcription:"+reponse)
                s= True
                t=t+1
            
            except sr.RequestError:
                t=t+1
                #logging.info("API non disponible")
                print("je vous ai pas compris")
                # self.dialog.SpeakText(reponse)
            except sr.UnknownValueError:
                print("je vous ai pas compris")
                t=t+1
                #logging.info("Impossible de reconnaître la parole")
                #self.dialog.SpeakText(reponse)
            except Exception as e: 
                print("ereur: "+str(e))
                
        return reponse
            
    def getValue(self):
        return self.value