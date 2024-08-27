import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import imutils
import uuid
import os

# Inicializar la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo acceder a la cámara")
    exit()

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Reconocimiento")
root.configure(bg='lightblue')  # Cambiar el color de fondo de la interfaz

# Crear un frame para el video
frame_video = tk.Frame(root, bd=2, relief=tk.SUNKEN, bg='lightblue')
frame_video.grid(row=0, column=0, padx=10, pady=10)

# Crear un label para mostrar el video
lblVideo = tk.Label(frame_video)
lblVideo.pack()

# Crear un frame para los botones y la caja de texto
frame_controls = tk.Frame(root, bd=2, relief=tk.SUNKEN, bg='lightblue')
frame_controls.grid(row=0, column=1, padx=10, pady=10)

# Cargar el clasificador de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Función para mostrar el video en el label
def Log_Biometric():
    global cap
    ret, frame = cap.read()
    if ret:
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Mostrar el nombre de la persona si coincide con una foto existente
            for file in os.listdir("fotos_guardadas"):
                if file.endswith(".png"):
                    name = file.split("_")[0]
                    cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    break
        
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, Log_Biometric)
    else:
        cap.release()

# Función para tomar una foto y guardarla
def take_photo():
    global cap
    ret, frame = cap.read()
    if ret:
        # Crear la carpeta si no existe
        save_path = "fotos_guardadas"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # Obtener el nombre de la caja de texto
        photo_name = entry_name.get()
        if not photo_name:
            print("El nombre no puede estar vacío")
            return
        
        # Verificar si el nombre ya existe
        for file in os.listdir(save_path):
            if file.startswith(photo_name):
                print("Este usuario ya está registrado")
                return
        
        # Nombre personalizado para la foto
        filename = os.path.join(save_path, f"{photo_name}_{uuid.uuid4()}.png")
        cv2.imwrite(filename, frame)
        print(f"Foto guardada como {filename}")
        
        # Limpiar la caja de texto
        entry_name.delete(0, tk.END)

# Función para cerrar la aplicación y liberar la cámara
def on_closing():
    cap.release()
    root.destroy()

# Añadir caja de texto para el nombre de la foto
lbl_name = tk.Label(frame_controls, text="Nombre de la foto:", bg='lightblue')
lbl_name.pack(pady=5)
entry_name = tk.Entry(frame_controls)
entry_name.pack(pady=5)

# Añadir botones para tomar foto y cerrar la aplicación
btnPhoto = tk.Button(frame_controls, text="Tomar Foto", command=take_photo)
btnPhoto.pack(pady=5)

btnClose = tk.Button(frame_controls, text="Cerrar", command=on_closing)
btnClose.pack(pady=5)

# Iniciar la función de captura de video
Log_Biometric()

# Ejecutar la ventana Tkinter
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
