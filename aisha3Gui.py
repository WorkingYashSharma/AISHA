from aisha3Ui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import pyttsx4
import datetime
import webbrowser
import os
import wikipedia
import speech_recognition as sr
from requests import get
import random
import pywhatkit as kit
import smtplib
import pyjokes
import pyautogui
import time
import pywikihow
import speedtest
# import wolframalpha
import winshell
# from ecapture import ecapture as ec
import psutil
import sys
import numpy as np
import cv2
import openai
import cv2
import requests
from googletrans import Translator
import json

engine = pyttsx4.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty("rate", 180)

current_rate = engine.getProperty('rate')
new_rate = 172
engine.setProperty('rate', new_rate)

chatStr = ""
folder_path = 'Camera'
# path = "Pictures"

# def type_in_notepad(text):
#     pyautogui.hotkey("win", "r")
#     pyautogui.typewrite("notepad")
#     pyautogui.press("enter")

#     pyautogui.typewrite(text)


def takePicture(folder_path):
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    camera.release()
    
    image_path = folder_path + '/captured_image.jpg'
    cv2.imwrite(image_path, frame)

    print(f"Picture taken and saved as {image_path}")

def cleanup():
    camera.release()
    cv2.destroyAllWindows()

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = "############################"
    chatStr += f"Yash: {query}\n AISHA: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )    
    
    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def aiImg(prompt):
    openai.api_key = "############################"
    text = f"AISHA Responses : {prompt} \n *************************\n\n"
    
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    image_response = requests.get(image_url)
    # image_path = os.path.join(path, ".jpg")
    
    
    with open(f"Pictures/{''.join(prompt.split('of')[1:]).strip() }.jpg", "wb") as f:
        f.write(image_response.content)
        
    print("Image saved")

def ai(prompt):
    openai.api_key = "############################"
    text = f"AISHA Responses : {prompt} \n *************************\n\n"
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    text += response["choices"][0]["text"]
    if not os.path.exists("Responses"):
        os.mkdir("Responses")
        
    with open(f"Responses/{''.join(prompt.split('about')[1:]).strip() }.txt", "w") as f:
        f.write(text)
        
        
def aiProgram(prompt):
    openai.api_key = "############################"
    text = f"AISHA Responses : {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    text += response["choices"][0]["text"]
    if not os.path.exists("Program"):
        os.mkdir("Program")
        
    with open(f"Program/{''.join(prompt.split('to')[1:]).strip() }.txt", "w") as f:
        f.write(text)
        
# def translate(audio_path,):
#     recognizer = sr.Recognizer()
    
#     with sr.AudioFile(audio_path) as source:
#         audio_data = recognizer.record(source)
        
#         text = recognizer.recognize_google(audio_data)
    
#     return text

def reminder():
    recognizer = sr.Recognizer()
    engine = pyttsx4.init('sapi5')

    with sr.Microphone() as source:
        speak("What would you like to be reminded of")
        audio = recognizer.listen(source)

    try:
        reminder_text = recognizer.recognize_google(audio)
        speak("When would you like to be reminded")
        engine.runAndWait()

        with sr.Microphone() as source:
            # print("Listening...")
            audio = recognizer.listen(source)

        reminder_time = recognizer.recognize_google(audio)
        reminder_datetime = datetime.datetime.strptime(reminder_time, "%H:%M")
        current_datetime = datetime.datetime.now()
        time_difference = reminder_datetime - current_datetime

        reminder = datetime.datetime.now() + time_difference
        speak(f"Reminder set for {reminder_time}.")

        speak(f"Reminder: {reminder_text}")
        engine.runAndWait()

        while datetime.datetime.now() < reminder:
            pass

        print(f"Reminder: {reminder_text}")

        reminder(f"Reminder: {reminder_text}")
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Unable to understand speech. Please try again.")

    except sr.RequestError as e:
        print(f"Speech recognition request error: {str(e)}")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            speak("Good Morning Sir")

        elif hour>=12 and hour<16:
            speak("Good Afternoon Sir")

        elif hour>=16 and hour<20:
            speak("Good Evening Sir")

        else:
            speak("Good Night Sir")


class MainThread(QThread):

    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def cpu():
        usage = str(psutil.cpu_percent())
        speak("CPU is at"+usage)

        battery = psutil.sensors_battery()
        speak("battery is at")
        speak(battery.percent) 

    def screenshot():
        img = pyautogui.screenshot()
        img.save("C:\\Users\\Yash Sharma\\Pictures\\Screenshots.png")

    def sendEmail(to, content):
        server = smtplib.SMTP("smtp.gmial.com", 587)
        server.ehlo()
        server.starttls()
        server.login("test@gmail.com", "test@123")
        server.sendmail("test@gmail.com", to, content)
        server.close()

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # print("Listening..")
            # r.pause_threshold = 0.8
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            self.query = r.recognize_google(audio, language = "en-IN")
            print(f"{self.query}\n")

        except Exception as e:
            #print(e)
            speak("Could you please repeat Sir")
            return "None"
        return self.query
   
    def TaskExecution(self): 

        speak("Importing all preferences from home interface. system is now fully operationable.")

        wishMe()

        while True:
            self.query = self.takeCommand().lower()

            # if "bare" in self.query:
            #     speak("Ok Sir, searching")
            #     self.query = self.query.replace("wikipedia", "")
            #     results = wikipedia.summary(self.query,sentences=5)
            #     speak("Alright, according to wikipedia")
            #     speak(results)
                
            if "about" or "can you" in self.query:
                ai(prompt=self.query)
                
            elif "create" in self.query:
                aiImg(prompt=self.query)
                
            elif "reminder" in self.query:
                reminder()
                
            elif "take" in self.query:
                takePicture(folder_path=folder_path)
                
            elif "program" or "code" in self.query:
                aiProgram(prompt=self.query)

            elif "youtube" in self.query:
                speak("Ok Sir")
                webbrowser.open("youtube.com")
                
                if "and" in self.query:
                    video_id = self.query.split("play", 1)[1].strip()
                    
                    if video_id:
                        video_url = f"https://www.youtube.com/results?search_query={video_id}"
                        webbrowser.open(video_url)
                    else:
                        speak("Please provide a valid channel or a video.")
                        
                else:
                    speak("Sorry, I didn't understand.")
                    
            # elif "write" in self.query:
            #     type_in_notepad(text=self.query)

            elif "google"in self.query:
                speak("Ok Sir")
                webbrowser.open("google.com")

            elif "gmail" in self.query:
                speak("Ok Sir")
                webbrowser.open("gmail.com")

            elif "fb" in self.query:
                speak("Ok Sir")
                webbrowser.open("facebook.com")

            elif "instagram" in self.query:
                speak("Ok Sir")
                webbrowser.open("instagram.com")

            elif "time" in self.query:
                strTime = datetime.datetime.now().strftime("%H %M")
                speak(f"It's{strTime}")

            elif "twitter" in self.query:
                speak("Ok Sir")
                webbrowser.open("twitter.com")

            elif "amazon" in self.query:
                speak("Ok Sir")
                webbrowser.open("amazon.in")

            elif "flipkart" in self.query:
                speak("Ok Sir")
                webbrowser.open("flipkart.com")

            elif "myntra" in self.query:
                speak("Ok Sir")
                webbrowser.open("myntra.com")

            elif "india map" in self.query:
                speak("Ok Sir")
                webbrowser.open("india map.com")

            elif "weather" in self.query:
                speak("Telling")
                webbrowser.open("weatherlive.co")

            elif "cricket score" in self.query:
                speak("Ok Sir")
                webbrowser.open("cricket score.com")

            elif "documents" in self.query:
                speak("Ok Sir")
                documentsPath = "Documents"
                os.startfile(documentsPath)

            elif "downloads"in self.query:
                speak("Ok Sir")
                downloadsPath = "Downloads"
                os.startfile(downloadsPath)

            elif "bye" in self.query:
                speak("Ok Sir, enjoy your day")
                exit()

            elif "full form" in self.query:
                speak("Apparently Intelligent System and Highly Adavnced")

            elif "send message" in self.query:
                    kit.sendwhatmsg("+919625641703", "this is a test message",17,13)

            elif "mail" in self.query:
                try:
                    speak("what shall i say")
                    content = self.takeCommand().lower()
                    to = "coolboyjack437@gmail.com"
                    sendEmail(to, content)
                    speak("email has been sent")

                except Exception as e:
                        print(e)
                        speak("sorry sir, i was unable to send this email")

            elif "notepad" in self.query:
                speak("Ok Sir")
                notepadPath = "C:\\Windows\\notepad.exe"
                os.startfile(notepadPath)

            elif "close" in self.query:
                    os.system("taskkill /f /im notepad.exe")

            #    elif  "set alarm" in self.query:
            #        nn = int(datetime.datetime.now().hour)
            #        if nn == 22:
            #            music_dir = 
            #            songs = os.listdir(music_dir)
            #            os.startfile(os.path.join(music_dir, songs[0]))

            elif "joke" in self.query:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif "shutdown" in self.query:
                os.system("shutdown /s")

            elif "restart" in self.query:
                os.system("shutdown /r")

            elif "where i am" in self.query:
                speak("let me check sir")
                try:
                    ipAdd = requests.get("https://api.ipify.org").text
                    print(ipAdd)
                    url = "https://get.geojs.io/v1/ip/geo/" + ipAdd + ".json"
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data["city"]
                    country = geo_data["country"]
                    speak("sir i guess we are in {city} city of {country} country")
                
                except Exception as e:
                        speak("sorry sir, due to network issue i am not able to find where we are")
                        pass

            elif "how to" in self.query:
                speak("ok sir")
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query,sentences=5)
                speak("Alright, according to wikipedia")
                print(results)
                speak(results)

            elif "internet" in self.query:
                st = speedtest.Speedtest()
                dl = st.download()
                up = st.upload()
                speak("sir we have {dl} bit per second downloading speed and {up} bit per second uploading speed")    

            elif "volume up" in self.query:
                pyautogui.press("volumeup")

            elif "volume down" in self.query:
                pyautogui.press("volumedown")    

            elif "mute" in self.query:
                pyautogui.press("volumemute")     

            elif "copy" in self.query:
                pyautogui.hotkey("ctrl", "c")   

            elif "select all" in self.query:
                pyautogui.hotkey("ctrl", "a")    

            elif "paste" in self.query:
                pyautogui.hotkey("ctrl", "v")       

            elif "undo" in self.query:
                pyautogui.hotkey("ctrl", "z")

            elif "screenshot" in self.query:
                speak("taking screenshot")
                screenshot()    

            elif "calculate" in self.query:
                app_id = "Wolframe Alpha API"
                client = wolframalpha.Client(app_id)
                indx = self.query.lower().split().index('calculate')
                self.query = self.query.split()[indx + 1:]
                res = client.self.query(' '.join(self.query))
                answer = next(res.results).text
                print("The answer is " + answer)
                speak("The answer is " + answer)    

            elif 'empty recycle bin' in self.query:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                speak("Recycle Bin Recycled")

            elif "don't listen" in self.query or "stop listening" in self.query:
                speak("for how long sir")
                a=int(takeCommand())
                time.sleep(a)
                print(a)   

            elif "kahan" in self.query:
                self.query=self.query.replace("kahan","")
                location = self.query
                speak(location)
                speak("searching")
                webbrowser.open("https://www.google.nl/maps/place/" + location + "")

            elif "camera" in self.query or "take a photo" in self.query:
                ec.capture(0,"AISHA Camera ","img.jpg")

            elif "count" in self.query:
                self.query = int(self.query.replace("count"," "))
                count(self.query)

            elif "note" in self.query:
                speak("What should i write , sir")
                note= takeCommand()
                file = open('AISHA.txt','w')
                speak("Sir, Shall i include date and time")
                snfm = takeCommand()
                if 'yes' in snfm or 'sure' in snfm:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)
            
            elif "show note" in self.query:
                speak("Showing Notes")
                file = open("AISHA.txt", "r") 
                print(file.read())
                speak(file.read(6))

            elif 'cpu' in self.query:
                cpu()
                
            elif "forget everything" in self.query:
                chatStr = ""
                
            else:
                chat(self.query)

startFunction = MainThread()

class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.aisha3_ui = Ui_MainWindow()
        self.aisha3_ui.setupUi(self)

        self.aisha3_ui.pushButton.clicked.connect(self.startFunction)
        self.aisha3_ui.pushButton_2.clicked.connect(self.close)

    def showTime(self):
        t_ime = QTime.currentTime()
        time = t_ime.toString("hh:mm:ss")
        label_time = time
        self.aisha3_ui.textBrowser.setText(label_time)
    
    def startFunction(self):

        self.aisha3_ui.movies_label = QtGui.QMovie("D:\\Documents\\Programming\\Python\\AISHA\\GUI\\gui.gif")
        self.aisha3_ui.label.setMovie(self.aisha3_ui.movies_label)
        self.aisha3_ui.movies_label.start()

        self.aisha3_ui.movies_label_2 = QtGui.QMovie("D:\\Documents\\Programming\\Python\\AISHA\\GUI\\gui3.gif")
        self.aisha3_ui.label_2.setMovie(self.aisha3_ui.movies_label_2)
        self.aisha3_ui.movies_label_2.start()

        self.aisha3_ui.movies_label_3 = QtGui.QMovie("D:\\Documents\\Programming\\Python\\AISHA\\GUI\\gui8.gif")
        self.aisha3_ui.label_3.setMovie(self.aisha3_ui.movies_label_3)
        self.aisha3_ui.movies_label_3.start()

        self.aisha3_ui.movies_label_4 = QtGui.QMovie("D:\\Documents\\Programming\\Python\\AISHA\\GUI\\gui5.gif")
        self.aisha3_ui.label_4.setMovie(self.aisha3_ui.movies_label_4)
        self.aisha3_ui.movies_label_4.start()

        self.aisha3_ui.movies_label_5 = QtGui.QMovie("D:\\Documents\\Programming\\Python\\AISHA\\GUI\\gui7.gif")
        self.aisha3_ui.label_5.setMovie(self.aisha3_ui.movies_label_5)
        self.aisha3_ui.movies_label_5.start()

        self.aisha3_ui.movies_label_6 = QtGui.QMovie("D:\\Documents\\Programming\\Python\\AISHA\\GUI\\gui6.gif")
        self.aisha3_ui.label_6.setMovie(self.aisha3_ui.movies_label_6)
        self.aisha3_ui.movies_label_6.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(999)    
        
        startFunction.start()

App = QtWidgets.QApplication(sys.argv)
Gui_Aisha = Main()
Gui_Aisha.show()
exit(App.exec_())
