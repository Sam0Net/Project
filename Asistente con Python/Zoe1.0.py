import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os
from pygame import mixer
import cam 

name = "sx8dx" 
listener = sr.Recognizer() 
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id) 
engine.setProperty('rate', 145)

sites={
                'google':'google.com',
                'youtube':'youtube.com',
                'facebook':'facebook.com',
                'whatsapp':'web.whatsapp.com',
                'cursos':'https://senati.blackboard.com/'
            }
files = {
    'carta':'document.pdf', 
    'word':'hola.docx',
    'foto':'luna.jpg'
}
programs = {
    'telegram': r"C:\Users\sandr\AppData\Roaming\Telegram Desktop\Telegram.exe",
    'steam': r"C:\Program Files (x86)\Steam\steam.exe",
    'discord': r"C:\Users\sandro\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
}


def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen ():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...") 
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)

    try:
        rec = listener.recognize_google(pc,language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendi, intenta de nuevo")
        if name in rec:
            rec = rec.replace(name, '')
    return rec

def run_sx8dx():
    while True:
        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce','')  
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca','')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search +": " + wiki)
            talk(wiki)
        elif 'alarma' in rec:
            num = rec.replace('alarma', '')
            num = num.strip()
            talk("Alarma activada a las " + num + " horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') ==num:
                    print("DESPIERTA JOPUTA!!!")
                    mixer.init()
                    mixer.music.load("auronplay.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
        elif 'colores' in rec:
            talk("Enseguida")
            cam.capture() 
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo {app}')  
                    os.startfile(programs[app])

        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)

            except FileNotFoundError as e:
                file = open("nota.txt", 'w') 
                write(file)

        elif 'termina' in rec:
            talk('Adiós!')
            break
def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)


if __name__ == '__main__':
    run_sx8dx()
    
    