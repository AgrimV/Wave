"""
wxPython implementation of a PA
"""
import wx
import wx.adv
import wolframalpha
import wikipedia
import pygame
import os
import re
import speech_recognition as sr
from selenium import webdriver
from gtts import gTTS

import random
import time

pygame.init()
time_greet = {'morning': 'good morning', 'anoon': 'good afternoon',
              'eve': 'good evening'}
clock = time.localtime(time.time())
if clock[3] < 12:
	clock = 'morning'
elif clock[3] < 17:
	clock = 'anoon'
else:
	clock = 'eve'
greet = ['welcome', 'hello', 'hello there',
         time_greet[clock], time_greet[clock]]
chaos = random.randint(0, len(greet) - 1)
speak = gTTS(greet[chaos])
speak.save("./gtts/welcome.mp3")


class MyTaskBarIcon(wx.adv.TaskBarIcon):
    """
    Class to create taskbar icon
    """
    def __init__(self, frame):

        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        img = wx.Bitmap("./icons/wavei2.png", wx.BITMAP_TYPE_ANY)
        self.icon = wx.Icon()
        self.icon = wx.Icon(img)
        self.SetIcon(self.icon, tooltip="{0} {1}".format("WAVE", "0.0.2"))
        # print(self.IsOk())
        # print(self.IsIconInstalled())


class MyFrame(wx.Frame):
    """
    Creating the frame for the App
    """
    def __init__(self):
        wx.Frame.__init__(self, None, pos=wx.DefaultPosition, size=wx.Size(450, 100), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, title="Wave")

        self.tbIcon = MyTaskBarIcon(self)

        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel, label="Hello I am Wave. What can I help you with?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        mic = wx.Bitmap("./icons/mic.png", wx.BITMAP_TYPE_ANY)
        wave = wx.Bitmap("./icons/wave.png", wx.BITMAP_TYPE_ANY)
        button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=mic, pos=(417, 28), size=(30, 30))
        button.SetBitmapPressed(wave)
        button.Bind(wx.EVT_BUTTON, self.onButton)
        self.Show()
        pygame.mixer.music.load("./gtts/welcome.mp3")
        pygame.mixer.music.play()
        os.remove("./gtts/welcome.mp3")


    def onButton(self, event):
        """
        Function to read the user audio input
        """
        ear = sr.Recognizer()

        with sr.Microphone() as source:
            # print("Say something!")
            audio = ear.listen(source)

        try:
            # print("Google Speech Recognition thinks you said " + ear.recognize_google(audio))
            question = ear.recognize_google(audio)
            if not self.fix_answer(question):
                self.reply(question)

        except sr.UnknownValueError:
            error = gTTS("Google Speech Recognition could not understand audio")
            error.save("./gtts/error.mp3")
            os.system("play ./gtts/error.mp3")
            os.remove("./gtts/error.mp3")
            return

        except sr.RequestError as e:
            # print("Could not request results from Google Speech Recognition service; {0}".format(e))
            error = gTTS(str(e) + "Could not request results from Google Speech Recognition service")
            error.save("./gtts/ni.mp3")
            os.system("play ./gtts/ni.mp3")
            return


    def OnEnter(self, event):
        """
        When enter is pressed on the query textbox
        """
        question = self.txt.GetValue()
        self.txt.SetValue('')
        if not self.fix_answer(question):
            self.reply(question)


    def search_web(self, question):
        """
        Function to search the web explicitly
        """
        if 'search youtube for' in question.lower():
            driver = webdriver.Firefox()
            driver.implicitly_wait(3)

            speak = gTTS("O pening in you tube")
            speak.save("./gtts/yt.mp3")
            os.system("play ./gtts/yt.mp3")
            os.remove("./gtts/yt.mp3")
            flag = question.lower().split().index('youtube for')
            query = question.split()[flag + 1:]
            driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
            return True

        elif 'youtube' in question.lower():#or 'play' in question.lower # might want spotipy bot

            driver = webdriver.Firefox()
            driver.implicitly_wait(3)

            speak = gTTS("O pening in you tube")
            speak.save("./gtts/yt.mp3")
            os.system("play ./gtts/yt.mp3")
            os.remove("./gtts/yt.mp3")
            flag = question.lower().split().index('youtube')
            query = question.split()[flag + 1:]
            driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
            return True

        else:

            if 'search for' in question:

                driver = webdriver.Firefox()
                driver.implicitly_wait(3)

                srch = gTTS("searching the web")
                srch.save("./gtts/srch.mp3")
                os.system("play ./gtts/srch.mp3")
                os.remove("./gtts/srch.mp3")

                flag = question.lower().split().index('search for')
                query = question.split()[flag + 1:]
                driver.get("https://duckduckgo.com/?q=" + '+'.join(query) + "&t=canonical&atb=v1-1&ia=web")
                return True

            elif 'search' in question:

                driver = webdriver.Firefox()
                driver.implicitly_wait(3)

                srch = gTTS("searching the web")
                srch.save("./gtts/srch.mp3")
                os.system("play ./gtts/srch.mp3")
                os.remove("./gtts/srch.mp3")

                flag = question.lower().split().index('search')
                query = question.split()[flag + 1:]
                driver.get("https://duckduckgo.com/?q=" + '+'.join(query) + "&t=canonical&atb=v1-1&ia=web")
                return True

            return False


    def open_application(self, question):
        """
        To open an installed app
        """
        question = question.lower()
        opened = 1

        if 'open' in question:
            opening = gTTS("trying to open the application")
            opening.save("./gtts/open.mp3")
            os.system("play ./gtts/open.mp3")
            os.remove("./gtts/open.mp3")
            flag = question.lower().split().index('open')
            query = question.split()[flag + 1:]
            app = question.split()

            if 'sublime' in question:
                os.system("subl")
                return True

            elif 'thunder' in question and 'bird' in question:
                os.system("thunderbird")
                return True

            elif 'gogole chrome' in question:
                os.system("google-chrome")
                return True

            for app_name in app:
                if not os.system(app_name):
                    return True
                else:
                    opened = 0

        elif not opened:

            fail = gTTS("Application not found")
            fail.save("./gtts/fail.mp3")
            os.system("play ./gtts/fail.mp3")
            os.remove("./gtts/fail.mp3")
            return False


    def fix_answer(self, question):
        """
        Some fixed answers for specific questions
        """
        if "who are you" in question: # "define yourself" in question
            itself = gTTS("I am Wave. V A V. Here to help automate your tasks. I can answer your queries, surf the web, do calculations and open other apps. And more.")
            itself.save("./gtts/intro.mp3")
            os.system("play ./gtts/intro.mp3")
            os.remove("./gtts/intro.mp3")
            return True

        elif "who made you" in question or "created you" in question:
            make = gTTS("I have been created by Agrim Vats.")
            make.save("./gtts/creator.mp3")
            os.system("play ./gtts/creator.mp3")
            os.remove("./gtts/creator.mp3")
            return True

        elif self.open_application(question):
            return True

        return False


    def reply(self, question):
        """
        Function to reply the user query
        """
        speak = gTTS("showing result for " + question)
        speak.save("./gtts/question.mp3")
        os.system("play ./gtts/question.mp3")
        os.remove("./gtts/question.mp3")
        answer = False

        if not self.search_web(question):

            try:
                # WolfRamAlpha
                app_id = "96YA8G-HTYUVU3GTX"

                client = wolframalpha.Client(app_id)
                res  = client.query(question)
                answer = tospeak = next(res.results).text

            except:
                # Wikipedia
                if re.search("(^.ho\s)|(^.hat\s)|(^.here\s)", question):
                    question = question.split(" ")
                    question = " ".join(question[2:])
                    tospeak = wikipedia.summary(question, sentences=1)
                    answer = wikipedia.summary(question, sentences=3)
                else:
                    tospeak = wikipedia.summary(question, sentences=1)
                    answer = wikipedia.summary(question, sentences=3)

            finally:

                if answer:
                    print(answer)
                    speak = gTTS(tospeak)
                    speak.save("./gtts/answer.mp3")
                    pygame.mixer.music.load("./gtts/answer.mp3")
                    pygame.mixer.music.play()
                    os.remove("./gtts/answer.mp3")
                else:
                    speak = gTTS("no relevant data found searching the web instead")
                    speak.save("./gtts/error.mp3")
                    os.system("play ./gtts/error.mp3")
                    os.remove("./gtts/error.mp3")
                    driver = webdriver.Firefox()
                    driver.implicitly_wait(3)
                    driver.maximize_window()
                    driver.get("https://duckduckgo.com/?q=" + '+'.join(question.split()) + "&t=canonical&atb=v1-1&ia=web")


if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
