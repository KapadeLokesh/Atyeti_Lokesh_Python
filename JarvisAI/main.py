import os
import platform
import webbrowser
import speech_recognition as sr
import datetime
import openai
from wikipedia import languages

def say(text):
        system = platform.system()
        if system == "Windows":
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        else:
            print("Text-to-speech not supported on this OS.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio,language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error Occured."

if __name__ == '__main__':
    print('PyCharm')
    say("Hello i am jarvis. How may i help you?")
    while True:
        print("Listening....")
        query = takeCommand()
        sites = [["youtube","https://www.youtube.com/"],["google","https://www.google.com/"],
                 ["wikipedia","https://www.wikipedia.org/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}..")
                webbrowser.open(site[0])

            elif "open music" in query:
                musicPath = "C:/Users/LokeshKapde/Downloads/filename.mp3"
                os.system(f"open{musicPath}")

            elif "the time" in query:
                curTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Current time is: {curTime}")

            elif "open camera".lower() in query.lower():
                os.system("start microsoft.windows.camera:")

            else:
                pass
            # say(text)




