import pyttsx3
import random
from gtts import gTTS
from playsound import playsound
tts = gTTS('Openning the door')
tts.save('hello.mp3')
 # lazy loading
            #print("playsound")
playsound(r'Opening the door.mp3')
