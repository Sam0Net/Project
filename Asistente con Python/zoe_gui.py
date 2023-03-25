# ----------------------Importación de librerias--------------------------
import speech_recognition as sr # Tomar lo que digamos por voz a texto.
import subprocess as sub
import pyttsx3 # Va permitir a la computadora a hablar.
import pywhatkit # Permite enviar msjs por wsp, reproducir musica en YT, etc.
import wikipedia # Permite buscar en google.
import datetime # Fechas y horas.
import keyboard # Detectar la pulsación del teclado
import os # Nos permite acceder a funcionalidades del S.O
import cam # Detección de colores
import tkinter 
from tkinter import * # Crear interfaces graficas.
from tkinter import filedialog 
import customtkinter # mejorar tkinder 
from PIL import Image, ImageTk # Edición de imagenes.
from pygame import mixer # Crear juegos
import threading as tr # Programación con hilos
import whatsapp as whapp # Nuestro modulo de Whatsapp para mandar mensaje 
import database # Nuestro modulo de conexión a nuestra base de datos 
from chatterbot import ChatBot # Permite crear un chatbot 
from chatterbot.trainers import ListTrainer # Entrenar Chatbot
import pyjokes # Chistes
import weather # modulo para saber el clima 
import shutil # mover carpeta 
from moviepy.editor import VideoFileClip 
from pytube import YouTube # descargar videos  
# -------------------------------------------------------------------------

# Creamos una ventana en Tkinder 
main_window = customtkinter.CTk() 
# Le damos un titulo 
main_window.title("Asistente Virtual ZOE") 

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("dark-blue") 

main_window.geometry("780x520") 
main_window.resizable(0,0) 
icono = ImageTk.PhotoImage(file="asistente.png")  
main_window.iconphoto(True, icono) 
comandos = """
     Comandos Utilizables:  
    -Reproduce (Música en YT)
    -Busca (Wikipedia) 
    -Abre (Página Web o App) 
    -Alarma (Formato 24H) 
    -Archivo (Nombre)
    -Colores (Rojo, Azul, Amarillo)
    -Escribe(Una nota) 
    -Mensaje(contacto) 
    -Conversar(hablar con Zoe) 
    -Clima(ciudad) 
    -Chiste(de programación) 
    -Termina (Fin del programa)
""" 

label_title = customtkinter.CTkLabel(master=main_window, text="ASISTENTE ZOE", text_color="white",
                        font=('Cascadia Mono', 40, 'bold'))  
label_title.pack(pady=10)                        

# canvas_comandos = customtkinter.CTkFrame(master=main_window,height=200, width=200) 
# canvas_comandos.place(x=0, y=1) 
comandos_text = customtkinter.CTkLabel(master=main_window, text=comandos, text_color="white",
                        font=('Arial',11, 'bold')) 
comandos_text.place(x=0, y=0) 
# canvas_comandos.(86, 80, text=comandos, fill="white", font='Arial 9 bold')

text_info = customtkinter.CTkTextbox(master=main_window, text_color='white') 
text_info.place(x=0, y=206, height=313, width=198) 

# Con este pedazo de código agregamos un gif a la pantalla.
zoe_gif = "gif_imagen.gif" 
info_gif = Image.open(zoe_gif) 
gif_nframes = info_gif.n_frames 
zoe_gif_list = [PhotoImage(file=zoe_gif, format=f'gif -index {i}') for i in range(gif_nframes)]
label_gif = Label(main_window) 
label_gif.pack() 

def animate_gif(index):
    frame = zoe_gif_list[index] 
    index += 1
    if index == gif_nframes:
        index = 0 
    label_gif.configure(image=frame) 
    main_window.after(50, animate_gif, index) 
animate_gif(0) 
 

# Voces Diponibles, Español España, México y EE.UU 
def mexican_voice():
    change_voice(0)
def spanish_voice():
    change_voice(1)
def english_voice():
    change_voice(2) 
def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola, bienvenido") 

# Nombre del Asistente
name = "zoe"  
# Empezar a reconocer nuestra voz
listener = sr.Recognizer() 
# Nuestra pc hable 
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 145) 


def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",") 
                val = val.rstrip("\n")
                name_dict[key] = val
    except FileNotFoundError as e:
            pass 

# Almacenar información, páginas, rutas, contactos
sites = dict()
charge_data(sites, "pages.txt")   
files = dict()
charge_data(files, "archivos.txt")
programs = dict()
charge_data(programs, "apps.txt")
contacts = dict()
charge_data(contacts, "contacts.txt")

# Función hablar
def talk(text):
    engine.say(text) 
    engine.runAndWait() 

# Función leer y hablar 
def read_and_talk():
    text = text_info.get("1.0", "end")
    talk(text)
# Función escribir texto 
def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)
# Función escuchar 
def listen(phrase=None):
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk(phrase)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError: 
        print("No te entendi, intenta de nuevo")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return rec

#Funciones asociadas a las palabras claves

def reproduce(rec):
    music = rec.replace('reproduce', '')
    print("Reproduciendo " + music)
    talk("Reproduciendo " + music)
    pywhatkit.playonyt(music)

def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ": " + wiki)


def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()

def colores(rec): 
    talk("Enseguida") 
    t = tr.Thread(target=cam.capture()) 
    t.start() 

def abre(rec):
    task = rec.replace('abre', '').strip()

    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start msedge.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}') 
    elif task in programs: 
        for task in programs: 
            if task in rec:
                    talk(f'Abriendo {task}')
                    os.startfile(programs[task]) 
    else:
        talk("Lo siento, parece que no has agregado esta app o página web, \
            usa los botones de agregar!") 

def archivo(rec):
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk("Lo siento, parece que no has agregado ese archivo, \
                        usa los botones de agregar!")                    
               
def escribe(rec):
    try: 
        with open("nota.txt", 'a') as f:
            write(f)

    except FileNotFoundError as e:
        file = open("nota.txt", 'w')
        write(file) 


def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num) 
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
                print("Alarma activa!")  
                mixer.init()
                mixer.music.load("auronplay.mp3")
                mixer.music.play() 

        else:
            continue 
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break

# Función para enviar mensaje por Whatsapp
def enviar_mensaje(rec):
    talk("¿A quién quieres enviar el mensaje?") 
    contact = listen("Te escucho") 
    contact = contact.strip()

    if contact in contacts:
        for cont in contacts:
            if cont == contact:
                contact = contacts[cont]
                talk("¿Qué mensaje quieres enviarle?")
                message = listen("Te escucho")
                talk("Enviando mensaje...")
                whapp.send_message(contact, message)
    else:
        talk("Parece que aún no has agregado a ese contacto, usa el botón de agregar!")

# Cerrar apps 
def cierra(rec):
    for task in programs:
        kill_task = programs[task].split('\\')
        kill_task = kill_task[-1]
        if task in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}')
        if 'todo' in rec:
            sub.call(f'TASKKILL /IM {kill_task} /F', shell=True)
            talk(f'Cerrando {task}') 
    if 'ciérrate' in rec:
        talk(f'Adiós') 
        # para cerrar nuestro programa 
        sub.call('TASKKILL /IM zoe_asistent.exe /F', shell=True) 


def conversar(rec):
    chat = ChatBot("zoe") 
    trainer = ListTrainer(chat)
    trainer.train(database.get_preguntas_respuestas()) 
    talk("Okey, conversemos...") 
    while True:
        try:
            request = listen("") 
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo")
            continue 
        print("Tú: ", request) 
        answer = chat.get_response(request) 
        print("Zoe: ", answer) 
        talk(answer) 
        if 'adiós' in request:
            break 
# Función para contar chistes 
def say_jokes(rec):
    jokes = pyjokes.get_joke(language='es', category='all')
    talk(jokes) 

# función para saber el clima
def say_weather(rec):
    talk("El clima de qué ciudad deseas saber?")
    ciudad = listen("Te escucho") 
    clima = weather.main_weather(ciudad) 
    talk(clima) 
    


#Diccionario con palabras claves:
key_words = {
    'reproduce': reproduce,
    'busca': busca,
    'alarma': thread_alarma,
    'colores': colores,
    'abre': abre,
    'archivo': archivo,
    'escribe': escribe,
    'mensaje': enviar_mensaje,
    'cierra': cierra, 
    'ciérrate': cierra,
    'conversar': conversar,
    'chiste': say_jokes,
    'clima': say_weather
} 

# Función Principal 
def run_zoe(): 
    while True: 
        try:
            rec = listen("Te escucho")
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo")
            continue
        if 'busca' in rec:
            key_words['busca'](rec)
            break
        else:
            for word in key_words:
                if word in rec:
                    key_words[word](rec)
        if 'termina' in rec:
            talk("Adiós!")
            break

    main_window.update()

# Función escribir 
def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen("Te escucho")
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

def open_w_files():
    global namefiles_entry, pathf_entry
    windows_files = Toplevel() 
    windows_files.configure(bg="#222629") 
    windows_files.title("Agrega archivos")
    windows_files.geometry("300x200")
    windows_files.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_files)} center')

    title_label = customtkinter.CTkLabel(master=windows_files, text="Agrega un archivo", text_color="white", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3) 
    name_label = customtkinter.CTkLabel(master=windows_files, text="Nombre del archivo", text_color="white", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2) 

    namefiles_entry = customtkinter.CTkEntry(master=windows_files,width=260) 
    namefiles_entry.pack(pady=1) 

    path_label = customtkinter.CTkLabel(master=windows_files, text="Ruta del archivo", text_color="white", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2) 

    pathf_entry = customtkinter.CTkEntry(master=windows_files, width=260) 
    pathf_entry.pack(pady=1)
    save_button = customtkinter.CTkButton(master=windows_files, text="Guardar",text_color="white", width=30, height=20, command=add_files, corner_radius=50)
    save_button.pack(pady=8) 


def open_w_apps():
    global nameapps_entry, patha_entry
    windows_apps = Toplevel()
    windows_apps.title("Agrega Apps") 
    windows_apps.configure(bg="#222629")  
    windows_apps.geometry("300x200")
    windows_apps.resizable(0,0) 
    main_window.eval(f'tk::PlaceWindow {str(windows_apps)} center')

    title_label = customtkinter.CTkLabel(master=windows_apps, text="Agrega una App", text_color="white", font=('Arial', 15, 'bold')) 
    title_label.pack(pady=3)
    name_label = customtkinter.CTkLabel(master=windows_apps, text="Nombre de la App", text_color="white", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2) 

    nameapps_entry = customtkinter.CTkEntry(master=windows_apps, width=260)  
    nameapps_entry.pack(pady=1)

    path_label = customtkinter.CTkLabel(master=windows_apps, text="Ruta de la App", text_color="white", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2)

    patha_entry = customtkinter.CTkEntry(master=windows_apps, width=260) 
    patha_entry.pack(pady=1)
    save_button = customtkinter.CTkButton(master=windows_apps, text="Guardar", text_color="white", width=30, height=20, command=add_apps, corner_radius=50) 
    save_button.pack(pady=8) 

def open_w_pages():
    global namepages_entry, pathp_entry
    windows_pages = Toplevel()
    windows_pages.title("Agrega Páginas Web")
    windows_pages.configure(bg="#222629") 
    windows_pages.geometry("300x200")
    windows_pages.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_pages)} center')

    title_label = customtkinter.CTkLabel(master=windows_pages, text="Agrega una Página Web", text_color="white", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)
    name_label = customtkinter.CTkLabel(master=windows_pages, text="Nombre de la Página", text_color="white", font=('Arial', 10, 'bold'))
    name_label.pack(pady=2)

    namepages_entry = customtkinter.CTkEntry(master=windows_pages, width=260)
    namepages_entry.pack(pady=1)

    path_label = customtkinter.CTkLabel(master=windows_pages, text="URL de la Página", text_color="white", font=('Arial', 10, 'bold'))
    path_label.pack(pady=2) 

    pathp_entry = customtkinter.CTkEntry(master=windows_pages, width=260) 
    pathp_entry.pack(pady=1)

    save_button = customtkinter.CTkButton(master=windows_pages, text="Guardar", text_color="white", width=30, height=20, command=add_pages, corner_radius=50)
    save_button.pack(pady=8) 

def download_video(): 
    def select_path():
        # Función que permite seleccionar una ruta desde el explorador 
        path = filedialog.askdirectory()
        path_label.config(text=path)

    def download_file():
        # Obtenemos la ruta 
        get_link = link_field.get()
        user_path = path_label.cget("text")
        download_video_now.title('Descargando...') 
        # Descarga del video 
        mp4_video = YouTube(get_link).streams.get_highest_resolution().download()
        vid_clip = VideoFileClip(mp4_video) 
        vid_clip.close()
        # Movemos el archivo a la ruta seleccioanda 
        shutil.move(mp4_video, user_path)
        download_video_now.title('Descarga Completa!') 

    global namepages_entry, pathp_entry
    download_video_now = Toplevel()
    download_video_now.title("Descarga De Videos") 
    download_video_now.configure(bg="#0a5483")
    canvas = Canvas(download_video_now, width=500, height=500) 
    download_video_now.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(download_video_now)} center')
    canvas.pack()

    # Logo 
    logo_img = PhotoImage(file='yt.png')
    #resize
    logo_img = logo_img.subsample(2, 2)
    canvas.create_image(250, 80, image=logo_img)

    # Link del video 
    link_field = Entry(download_video_now, width=40, font=('Arial', 15) )
    link_label = Label(download_video_now, text="Ingresa el link del video: ", font=('Arial', 15)) 

    # Seleccionar ruta y guardar archivo 
    path_label = Label(download_video_now, text="Selecciona la ruta para descargar", font=('Arial', 15))
    select_btn =  Button(download_video_now, text="Seleccionar ruta", bg='red', padx='22', pady='5',font=('Arial', 15), fg='#fff', command=select_path)
    
    canvas.create_window(250, 280, window=path_label)
    canvas.create_window(250, 330, window=select_btn)

    canvas.create_window(250, 170, window=link_label)
    canvas.create_window(250, 220, window=link_field)

    # Botón descargar 
    download_btn = Button(download_video_now, text="Descargar Video",bg='green', padx='22', pady='5',font=('Arial', 15), fg='#fff', command=download_file)

    canvas.create_window(250, 390, window=download_btn)

    download_video_now.mainloop() 

def add_files():
    name_file = namefiles_entry.get().strip()
    path_file = pathf_entry.get().strip()
    
    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefiles_entry.delete(0, "end")
    pathf_entry.delete(0, "end")

def add_apps():
    name_file = nameapps_entry.get().strip()
    path_file = patha_entry.get().strip()

    programs[name_file] = path_file
    save_data(name_file, path_file, "apps.txt")
    nameapps_entry.delete(0, "end")
    patha_entry.delete(0, "end")

def add_pages():
    name_page = namepages_entry.get().strip()
    url_pages = pathp_entry.get().strip()

    sites[name_page] = url_pages
    save_data(name_page, url_pages, "pages.txt")
    namepages_entry.delete(0, "end")
    pathp_entry.delete(0, "end")

def add_contacs():
    name_contact = namecontact_entry.get().strip()
    phone = phone_entry.get().strip()

    contacts[name_contact] = phone
    save_data(name_contact, phone, "contacts.txt") 
    namecontact_entry.delete(0, "end")
    phone_entry.delete(0, "end") 

def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError:
        file = open(file_name, 'a')
        file.write(key + "," + value + "\n") 

def talk_pages():
    if bool(sites) == True:
        talk("Has agregado las siguientes páginas web")
        for site in sites:
            talk(site)
    
    else:
        talk("Aún no has agregado páginas web!")

def talk_apps():
    if bool(programs) == True:
        talk("Has agregado las siguientes apps")
        for app in programs:
            talk(app)
    
    else:
        talk("Aún no has agregado apps!")

def talk_files():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    
    else:
        talk("Aún no has agregado archivos!")

def talk_contacts():
    if bool(contacts) == True:
        talk("Has agregado los siguientes contactos")
        for cont in contacts:
            talk(cont)
    else:
        talk("Aún no has agregado contactos!")


def give_me_name(): 
    talk("Hola, ¿cómo te llamas?")
    name = listen("Te escucho")
    name = name.strip()
    talk(f"Bienvenido {name}")

    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(name)

def say_hello():
    if os.path.exists("name.txt"):
        with open ("name.txt") as f:
            for name in f:
                talk(f"Hola, bienvenido {name}")
    else:
        give_me_name()

def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()

thread_hello()

def open_w_contacts():
    global namecontact_entry, phone_entry
    windows_contacts = Toplevel()
    windows_contacts.title("Agrega un contacto")
    windows_contacts.configure(bg="#0a5483") 
    windows_contacts.geometry("300x200")
    windows_contacts.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_contacts)} center')

    title_label = customtkinter.CTkLabel(master=windows_contacts, text="Agrega un contacto", 
                        text_color="white", font=('Arial', 15, 'bold')) 
    title_label.pack(pady=3)
    name_label = customtkinter.CTkLabel(master=windows_contacts, text="Nombre del contacto",
                        text_color="white", font=('Arial', 10, 'bold')) 
    name_label.pack(pady=2)

    namecontact_entry = customtkinter.CTkEntry(master=windows_contacts, width=260) 
    namecontact_entry.pack(pady=1)

    phone_label = customtkinter.CTkLabel(master=windows_contacts, text="Número celular (con código del país).",
                        text_color="white", font=('Arial', 10, 'bold')) 
    phone_label.pack(pady=2) 

    phone_entry = customtkinter.CTkEntry(master=windows_contacts, width=260)
    phone_entry.pack(pady=1)
    
    save_button = customtkinter.CTkButton(master=windows_contacts, text="Guardar", text_color="white", width=30, height=20, command=add_contacs, corner_radius=50) 
    save_button.pack(pady=8)                    

button_voice_mx = customtkinter.CTkButton(main_window, text="Voz México", text_color="white", fg_color="#348F50",
                        font=("Arial", 11, "bold"), command=mexican_voice, corner_radius=20)
button_voice_mx.place(x=625, y=80, width=100,height=30) 

button_voice_es = customtkinter.CTkButton(main_window, text="Voz España", text_color="white", fg_color="#ED213A",
                        font=("Arial", 11, "bold"), command=spanish_voice, corner_radius=20)
button_voice_es.place(x=625, y=115, width=100,height=30)

button_voice_us = customtkinter.CTkButton(master=main_window, text="Voz USA", text_color="white", fg_color="#2948ff",
                        font=("Arial", 11, "bold"), command=english_voice, corner_radius=20)
button_voice_us.place(x=625, y=150, width=100,height=30)

button_listen = customtkinter.CTkButton(master=main_window, text="Escuchar", text_color="white", fg_color="#132166",
                        font=("Arial", 25, "bold"), width=200, height=40, command=run_zoe, corner_radius=20)  
button_listen.pack(side=BOTTOM, pady=10)  

button_speak = customtkinter.CTkButton(main_window, text="Hablar", text_color="white", fg_color="#132166",
                        font=("Arial", 11, "bold"), command=read_and_talk,corner_radius=20)
button_speak.place(x=625, y=185, width=100,height=30) 


button_add_files = customtkinter.CTkButton(main_window, text="Agregar archivos", text_color="white", fg_color="#181419",
                        font=("Arial", 10, "bold"), command=open_w_files, corner_radius=20)
button_add_files.place(x=613, y=220, width=125,height=30)

button_add_apps = customtkinter.CTkButton(main_window, text="Agregar Apps", text_color="white", fg_color="#181419",
                        font=("Arial", 11, "bold"), command=open_w_apps, corner_radius=20)
button_add_apps.place(x=613, y=255, width=125,height=30)

button_add_pages = customtkinter.CTkButton(main_window, text="Agregar Páginas", text_color="white", fg_color="#181419",
                        font=("Arial", 10, "bold"), command=open_w_pages, corner_radius=20)
button_add_pages.place(x=613, y=290, width=125,height=30)

button_download_video = customtkinter.CTkButton(main_window, text="Descargar Videos", text_color="white", fg_color="#181419",
                        font=("Arial", 10, "bold"), command=download_video, corner_radius=20) 
button_download_video.place(x=613, y=360, width=125,height=30) 

button_tell_pages = customtkinter.CTkButton(main_window, text="Páginas Agregadas", text_color="white", fg_color="#181419",
                        font=("Arial", 10, "bold"), command=talk_pages, corner_radius=20)
button_tell_pages.place(x=205, y=390, width=125, height=30)

button_tell_apps = customtkinter.CTkButton(main_window, text="Apps Agregadas", text_color="white", fg_color="#181419",
                        font=("Arial", 10, "bold"), command=talk_apps, corner_radius=20)
button_tell_apps.place(x=335, y=390, width=125, height=30)

button_tell_files = customtkinter.CTkButton(main_window, text="Archivos Agregados", text_color="white", fg_color="#181419",
                        font=("Arial", 9, "bold"), command=talk_files, corner_radius=20)
button_tell_files.place(x=465, y=390, width=125, height=30) 

button_add_contacts = customtkinter.CTkButton(main_window, text="Agregar contactos", text_color="white", fg_color="#181419", 
                        font=("Arial", 10, "bold"), command=open_w_contacts, corner_radius=20)
button_add_contacts.place(x=613, y=325, width=125, height=30)

button_tell_contact = customtkinter.CTkButton(main_window, text="Contactos Agregados", text_color="white", fg_color="#181419",
                        font=("Arial", 9, "bold"), command=talk_contacts, corner_radius=20) 
button_tell_contact.pack(side=BOTTOM, pady=3) 
button_tell_contact.place(x=335, y=430, width=125, height=30) 

main_window.mainloop()