import speech_recognition as sr
from gtts import gTTS
from selenium import webdriver
import wolframalpha
import wikipedia
import pygame
import re
import os

import random
import time

# Use Kivy for the GUI
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.config import Config

Config.set('kivy','window_icon','./icons/wave.png')

pygame.init()

time_greet = {'morning' : 'good morning', 'anoon' : 'good afternoon', 'eve' : 'good evening'}
clock = time.localtime(time.time())
if clock[3] < 12:
	clock = 'morning'
elif clock[3] < 17:
	clock = 'anoon'
else:
	clock = 'eve'
greet = ['welcome', 'hello', 'hello there', time_greet[clock], time_greet[clock]]
chaos = random.randint(0, len(greet) - 1)
try:
	speak = gTTS(greet[chaos])
	speak.save("./gtts/welcome.mp3")
except:
	pass


class  WaveApp(App, GridLayout):

	def build(self):
		self.title = 'Wave'
		try:
			# os.system("play ./gtts/welcome.mp3")
			pygame.mixer.music.load("./gtts/welcome.mp3")
			pygame.mixer.music.play()
			os.remove("./gtts/welcome.mp3")
		except:
			pass

		return WaveApp()


	def OnEnter(instance):
		# question = # User Input
		# Set TextBox to null
		question = instance.ids.input.text
		instance.ids.input.text = ''
		if not fix_answer(question):
			reply(question)


class ImageButton(ButtonBehavior, Image):

	def __init__(self, **kwargs):
		super(ImageButton, self).__init__(**kwargs)
		self.source = './icons/microphoneo.png'


	def on_press(instance):
		# Change image source -> instance.source
		instance.source = './icons/sound.png'
		listener()

	def on_release(instance):
		instance.source = './icons/sound.png'
		time.sleep(2)
		instance.source = './icons/microphoneo.png'


def listener():

	ear = sr.Recognizer()

	with sr.Microphone() as source:
	    # print("Say something!")
	    audio = ear.listen(source)

	try:
	    # print("Google Speech Recognition thinks you said " + ear.recognize_google(audio))
	    question = ear.recognize_google(audio)
	    if not fix_answer(question):
	    	reply(question)
	except sr.UnknownValueError:
	    error = gTTS("Google Speech Recognition could not understand audio")
	    error.save("./gtts/error.mp3")
	    os.system("play ./gtts/error.mp3")
	    os.remove("./gtts/error.mp3")
	    return

	except sr.RequestError as e:

		pop("\n\n\n\n\n\nCould not request results from Google Speech Recognition service; {0}\n\n\n\n\n\n".format(e))
		# os.system("play ./gtts/ni.mp3")
		pygame.mixer.music.load("./gtts/ni.mp3")
		pygame.mixer.music.play()
		return


def fix_answer(question):

	if "who are you" in question: # "define yourself" in question
		itself = gTTS("I am Wave. V A V. Here to help automate your tasks. I can answer your queries, surf the web, do calculations and open other apps and more!")
		itself.save("./gtts/intro.mp3")
		os.system("play ./gtts/intro.mp3")
		os.remove("./gtts/intro.mp3")
		return True

	elif "who made you" in question or "created you" in question:
		make = gTTS("I have been created by a grin Vats.")
		make.save("./gtts/creator.mp3")
		os.system("play ./gtts/creator.mp3")
		os.remove("./gtts/creator.mp3")
		return True

	elif open_application(question):
		return True

	return False


def reply(question):
	speak = gTTS("showing result for " + question)
	speak.save("./gtts/question.mp3")
	os.system("play ./gtts/question.mp3")
	os.remove("./gtts/question.mp3")
	tospeak = ''
	answer = False
	try:
		# WolfRamAlpha
		if 'wikipedia' in question:
			print(commit_error)
		app_id = "96YA8G-HTYUVU3GTX"

		client = wolframalpha.Client(app_id)
		res  = client.query(question)
		answer = next(res.results).text
		tospeak = answer

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
			speak = gTTS(tospeak)
			speak.save("./gtts/answer.mp3")
			pop(answer)
			# os.system("play answer.mp3")
			pygame.mixer.music.load("./gtts/answer.mp3")
			pygame.mixer.music.play()
			os.remove("./gtts/answer.mp3")
		else:
			speak = gTTS("no relevant data found")
			speak.save("./gtts/error.mp3")
			os.system("play ./gtts/error.mp3")
			os.remove("./gtts/error.mp3")


def search_web(question):

    if 'search youtube for' in question.lower():
    	driver = webdriver.Firefox()
    	driver.implicitly_wait(3)

    	speak = gTTS("Opening in youtube")
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

    	speak = gTTS("Opening in youtube")
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


def open_application(question):

	question = question.lower()
	opened = True

	if 'open' in question:
		opening = gTTS("trying to open the application")
		opening.save("./gtts/open.mp3")
		os.system("play ./gtts/open.mp3")
		os.remove("./gtts/open.mp3")
		flag = question.lower().split().index('open')
		query = question.split()[flag + 1:]
		app = question.split()

		for app_name in app:
			if not os.system(app_name):
				return True
			else:
				opened = False

	elif not opened:

		fail = gTTS("Application not found")
		fail.save("./gtts/fail.mp3")
		os.system("play ./gtts/fail.mp3")
		os.remove("./gtts/fail.mp3")
		return False


def pop(answer):

	content = Label(text='[ref=world] {0} [/ref]'.format(answer), text_size=(len(answer), None), markup=True)
	popup = Popup(title='Result', content=content, size_hint=(None, None), size=(600, 400), auto_dismiss=False)
	content.bind(on_ref_press=popup.dismiss)
	popup.open()


def main():
	wave = WaveApp()
	wave.run()


if __name__ == '__main__':
	main()
