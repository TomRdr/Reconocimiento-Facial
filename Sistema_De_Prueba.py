import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import imutils
import uuid
import os
import threading
import face_recognition

# Inicializar la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo acceder a la cámara")
    exit()

# Cargar el clasificador de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Ingreso")
root.geometry("1280x600")  # Ajustar el tamaño de la ventana

# Cargar la imagen de fondo
bg_image = Image.open("Elementos_graficoas/NOTAS.png")
bg_image = bg_image.resize((1280, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Crear un label para la imagen de fondo
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear un frame para los botones de registro e inicio de sesión
frame_main = tk.Frame(root, bd=2, relief=tk.SUNKEN, bg='lightblue')
frame_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Cargar las imágenes para los botones
img_register = ImageTk.PhotoImage(Image.open("Elementos_graficoas/4.png").resize((50, 50), Image.LANCZOS))
img_login = ImageTk.PhotoImage(Image.open("Elementos_graficoas/5.png").resize((50, 50), Image.LANCZOS))
img_exit = ImageTk.PhotoImage(Image.open("Elementos_graficoas/6.png").resize((50, 50), Image.LANCZOS))

# Función para abrir la ventana de registro
def open_register():
    print("Abriendo ventana de registro")  # Marcador
    register_window = tk.Toplevel(root)
    register_window.title("Registrar")
    register_window.configure(bg='lightblue')
    
    # Crear un frame para el video
    frame_video = tk.Frame(register_window, bd=2, relief=tk.SUNKEN, bg='lightblue')
    frame_video.grid(row=0, column=0, padx=10, pady=10)
    
    # Crear un label para mostrar el video
    lblVideo = tk.Label(frame_video)
    lblVideo.pack()
    
    # Crear un frame para los controles
    frame_controls = tk.Frame(register_window, bd=2, relief=tk.SUNKEN, bg='lightblue')
    frame_controls.grid(row=0, column=1, padx=10, pady=10)
    
    # Añadir caja de texto para el nombre de la foto
    lbl_name = tk.Label(frame_controls, text="Nombre de la foto:", bg='lightblue')
    lbl_name.pack(pady=5)
    entry_name = tk.Entry(frame_controls)
    entry_name.pack(pady=5)
    
    # Función para tomar una foto y guardarla
    def take_photo():
        ret, frame = cap.read()
        if ret:
            save_path = "fotos_guardadas"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            photo_name = entry_name.get()
            if not photo_name:
                print("El nombre no puede estar vacío")
                return
            
            for file in os.listdir(save_path):
                if file.startswith(photo_name):
                    print("Este usuario ya está registrado")
                    return
            
            filename = os.path.join(save_path, f"{photo_name}_{uuid.uuid4()}.png")
            cv2.imwrite(filename, frame)
            print(f"Foto guardada como {filename}")
            
            entry_name.delete(0, tk.END)
    
    # Añadir botones para tomar foto y cerrar la ventana de registro
    btnPhoto = tk.Button(frame_controls, text="Tomar Foto", command=take_photo)
    btnPhoto.pack(pady=5)
    
    btnClose = tk.Button(frame_controls, text="Cerrar", command=register_window.destroy)
    btnClose.pack(pady=5)
    
    # Función para mostrar el video en el label
    def show_video():
        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, show_video)
    
    show_video()

# Función para abrir la ventana de inicio de sesión
def open_login():
    print("Abriendo ventana de inicio de sesión")  # Marcador
    login_window = tk.Toplevel(root)
    login_window.title("Iniciar Sesión")
    login_window.configure(bg='lightblue')
    
    # Crear un frame para el video
    frame_video = tk.Frame(login_window, bd=2, relief=tk.SUNKEN, bg='lightblue')
    frame_video.grid(row=0, column=0, padx=10, pady=10)
    
    # Crear un label para mostrar el video
    lblVideo = tk.Label(frame_video)
    lblVideo.pack()
    
    # Crear un frame para los controles
    frame_controls = tk.Frame(login_window, bd=2, relief=tk.SUNKEN, bg='lightblue')
    frame_controls.grid(row=0, column=1, padx=10, pady=10)
    
    # Función para verificar la identidad del usuario
    def verify_identity():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                face_encodings = face_recognition.face_encodings(frame, [(y, x+w, y+h, x)])
                if face_encodings:
                    face_encoding = face_encodings[0]
                    known_faces = []
                    known_names = []
                    
                    for file in os.listdir("fotos_guardadas"):
                        if file.endswith(".png"):
                            image = face_recognition.load_image_file(os.path.join("fotos_guardadas", file))
                            encoding = face_recognition.face_encodings(image)[0]
                            known_faces.append(encoding)
                            known_names.append(file.split("_")[0])
                    
                    matches = face_recognition.compare_faces(known_faces, face_encoding)
                    name = "Desconocido"
                    
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_names[first_match_index]
                    
                    cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    if name != "Desconocido":
                        tk.Label(login_window, text=f"Bienvenido, {name}!", bg='lightblue', font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=10)
                    else:
                        tk.Label(login_window, text="Usuario no reconocido", bg='lightblue', font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=10)
    
    # Añadir botones para verificar identidad y cerrar la ventana de inicio de sesión
    btnVerify = tk.Button(frame_controls, text="Verificar Identidad", command=verify_identity)
    btnVerify.pack(pady=5)
    
    btnClose = tk.Button(frame_controls, text="Cerrar", command=login_window.destroy)
    btnClose.pack(pady=5)
    
    # Función para mostrar el video en el label
    def show_video():
        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, show_video)
    
    show_video()

# Añadir botones para abrir las ventanas de registro e inicio de sesión con imágenes
btnRegister = tk.Button(frame_main, image=img_register, text="Registrar", compound=tk.LEFT, command=open_register)
btnRegister.grid(row=0, column=0, padx=10, pady=10)

btnLogin = tk.Button(frame_main, image=img_login, text="Iniciar Sesión", compound=tk.LEFT, command=open_login)
btnLogin.grid(row=0, column=1, padx=10, pady=10)

# Añadir botón para cerrar la aplicación con imagen
btnExit = tk.Button(frame_main, image=img_exit, text="Cerrar", compound=tk.LEFT, command=lambda: (cap.release(), root.destroy()))
btnExit.grid(row=0, column=2, padx=10, pady=20)

# Ejecutar la ventana Tkinter
root.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), root.destroy()))
root.mainloop()
