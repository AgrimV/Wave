# Wave

An attempt to create a virtual PA in Python.

It can open applications, open YouTube search result page, fetch results from the web using DuckDuckGo search engine (*Selenium*) and *Wikipedia API* and also perform some calculations using the *WolfRamAlpha API*.
Opening the browser to display the result is the last resort in case it does not find any results from above sources.

It accepts typed searches as well as voice input using *SpeechRecognition* library of Python.
The result is printed to screen as well as spoken (wherever possible) using *gTTS* and *PyGame* libraries.

It has two different UIs using - *Kivy* and *wxPython*.
