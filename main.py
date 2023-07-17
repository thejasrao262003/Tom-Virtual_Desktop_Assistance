import datetime
import random
from AppOpener import open as op
import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import openai
from config import apikey
import time

chat_response = ''

news_api_key = "d1fbefc02d2c4c25ac91ef82254a3abc"

print("Desktop Assistant Tom")
def chat(prompt):
    global chat_response
    openai.api_key = apikey
    chat_response += f"Thejas: {prompt}\n Tom: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chat_response,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        say(response['choices'][0]['text'])
        chat_response += f"{response['choices'][0]['text']}\n"
        return response['choices'][0]['text']

    except Exception as e:
        return "There has occurred some error..."



def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt}\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        print(response['choices'][0]["text"])
        text += response['choices'][0]["text"]
        with open(f"Openai/{''.join(prompt.lower().split('tom'))[1:60].strip()}.txt", 'w+') as f:
            f.write(text)

    except Exception as e:
        return "There has occurred some error..."

    return response['choices'][0]["text"]

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occured..."


say("Hello I am Tom")
while True:
    print("Listening...")
    query = takeCommand()
    if "open" in query.lower():
        sites = [['youtube', "https://youtube.com"], ['google', 'https://google.com'],
                 ['wikipedia', "https://wikipedia.com"], ['chat gpt', 'https://chat.openai.com/']]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                webbrowser.open(f"{site[1]}")
                say(f"Opening {site[0]} sir")
        path = "C:/Users/theja/Downloads/smoke-143172.mp3"
        if 'open music' in query.lower():
            os.startfile(path)

        apps = [['brave', 'Brave'], ['chrome', "Google Chrome"], ['power b i', "Power BI Desktop"]]
        for app in apps:
            if f"open {app[0]}".lower() in query.lower():
                say(f"Opening {app[0]} boss...")
                op(app[1])
    #say(text)

    elif 'the time' in query.lower():
        strftime = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"Sir the time is {strftime}")

    # adding open AI features

    elif "AI Tom ".lower() in query.lower():
        response = ai(prompt=query)
        say(response)

    elif "a joke".lower() in query.lower():
        jokes = [["What’s the opposite of artificial intelligence?", "Natural stupidity!"],
                 ["Son asks his father why does he speak so lightly at home? Father replies because there is artificial intelligence that listens to everything we say.", "Son laughs, the dad laughs, Alexa laughs"],
                 ["Why can't AI (Artificial Intelligence) replace managers?", "because it’s not designed to be useless"],
                 ["What do you call a luxury automobile with a built in artificial intelligence?", "Alexus"],
                 ["What do you call a homosexual artificial intelligence", "Chat G B T"],
                 ["I bought several books on how to overcome artificial intelligence.", "I saw them advertised on my Facebook."],
                 ["Artificial Intelligence is really taking over our jobs, man.", "Just today, I asked Siri to change the tv channel, and it ended up calling my mother. Siri has now replaced my partially deaf grandma."],
                 ["One could argue that human beings are artificial intelligences", "But most people don’t think we’re smart enough to qualify."]]
        value = random.randint(0, 7)
        say(jokes[value][0])
        time.sleep(1)
        say(jokes[value][1])

    elif "Tom Quit".lower() in query.lower():
        exit()

    elif "reset chat".lower() in query.lower():
        chat_response += ''
    else:
        print("Chatting...")
        chat(query)
