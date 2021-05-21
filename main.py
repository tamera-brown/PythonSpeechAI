import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
import datetime
import requests
import math
import wikipedia
from gtts import gTTS




r=sr.Recognizer()

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio=r.listen(source)
        voice_data=''
        try:
            voice_data=r.recognize_google(audio)
         
        except sr.UnknownValueError:
            speak('Sorry, I did not get that')
        except sr.RequestError:
            speak('Sorry, service is down')
        return voice_data

def speak(audio_string):
    tts=gTTS(text=audio_string, lang='en')
    r=random.randint(1,1000000)
    audio_file='audio-' +str(r) +'.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):

    if 'what is your name' in voice_data:
        speak('My name is Tamera')

    if "what's today's date" in voice_data:
        today_date=datetime.datetime.today().strftime('%a %b %d %Y')
        speak(today_date)

    if 'what time is it' in voice_data:
        current_time=datetime.datetime.now().strftime('%I:%M %p')
        speak("It's " + current_time)

    if 'search web' in voice_data:
        search=record_audio('What do you want to search for on google?')
        url='https://google.com/search?q=' + search
        webbrowser.get().open(url)
        speak('Here is what I found for ' + search)

    if 'videos' in voice_data:
        search=record_audio('What do you want to search for on youtube?')
        url='https://youtube.com/results?search_query=' + search
        webbrowser.get().open(url)
        speak('Here is what I found for' + search)

    if 'find location' in voice_data:
        location=record_audio('What is the location')
        url='https://google.nl/maps/place/'+location+'/&map;'
        webbrowser.get().open(url)
        speak('Here is the location')

    if 'summary' in voice_data:
        wiki=record_audio('What would you like to look up on Wikipedia')
        results=wikipedia.summary((str(wiki)),sentences=2)
        speak("According to Wikipedia, " + results)


    if "what's the weather" in voice_data:
        base_url="https://api.openweathermap.org/data/2.5/weather?"
        api_key="daa1bb6563c9cd0fc44fdd52043bf959"
        city=record_audio('for what city')
        url=base_url + 'q=' + city + '&units=imperial&appid=' + api_key
        response=requests.get(url)
        if response.status_code==200:
            data=response.json()
            main=data['main']
            temp=main['temp']
            speak("It is currently " + str(math.ceil(temp))+ " degrees, in " + city)

    if 'thank you' in voice_data:
        speak("You’re Welcome")

    if 'goodbye' in voice_data:
        speak('Bye')
        exit()

time.sleep(0.5)
speak('How can I help you?')
while 1:
    voice_data=record_audio()
    respond(voice_data)