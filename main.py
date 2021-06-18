import sys
import os
import threading
import logging
import subprocess
import time
import socketio
from dialog import Dialog
from audioManager import AudioRecorder
#from faceManager import FaceRecognition
logging.basicConfig(filename='voice-assistant.log', level=logging.INFO)

#Connect to Socket
sio = socketio.Client()
#listen en pitch event
#sio.connect('http://192.168.252.216:9400', namespaces=['/service','/speech'])
@sio.on('pitch', namespace='/speech')
def on_pitch(data):
    tt=data['content']
    dialog.SpeakText(tt)
    time.sleep(6)
    sio.emit("home", "AKW@BA",namespace='/speech')

def main():
    print("socket")    
    #Connexion au serveur
    sio.connect('http://192.168.252.216:9400', namespaces=['/speech'])
    print('my sid is', sio.sid)
    sio.emit("requests-count", "1",namespace='/speech')
    #sio.on("pitch",message,namespace=['/speech'])

#    sio.wait()

if __name__ == "__main__":
    logging.info('debut')
    #main()
    dialog = Dialog(sio)
#    main()
    audio_recorder = AudioRecorder(dialog)
    # face = FaceRecognition(audio_recorder)
#    main()
