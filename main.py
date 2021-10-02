from cmu_112_graphics import *
import math, random, time, copy, threading
# from pydub import AudioSegment
# from pydub.playback import play
from PIL import Image

from ta import *
from kos import *
from student2 import *
from test import * 
from classroom import *

class MyApp(ModalApp):
     def appStarted(self):
        self.battleMode = DerekApp()
        self.classRoomMode = myApp()
        self.setActiveMode(self.classRoomMode)

# class audioThread(threading.Thread):
#     def __init__(self, threadID):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#     def run(self):
#         song = AudioSegment.from_wav('/Users/tony/Desktop/15112/hack112/song.wav')
#         softer_song = song - 30
#         while True:
#             play(softer_song)
   
# audioThread = audioThread(2)
# audioThread.start()

MyApp(width = 544, height = 480)
