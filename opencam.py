import cv2
import os
import random
import tkinter as tk
from tkinter import ttk
import subprocess

def rekamWajah(nama):
    kRandom = random.randint(0, 999999)
    faceDir = 'Assets/Dataset/'
    camera = cv2.VideoCapture(0)
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    camera.set(6, codec)
    camera.set(5, 60)
    camera.set(3, 1280)
    camera.set(4, 720)

    cascade = cv2.CascadeClassifier('Assets/Model/haarcascade_frontalface_default.xml')
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        wajah = cascade.detectMultiScale(gray, 1.1, 4)
        for (x,y,w,h) in wajah:
            frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (107, 235, 52), 2)
            namaFile = str(entry_nama.get()) + '.jpg'
            cv2.imwrite(faceDir +'/'+ namaFile , gray[y:y+h, x:x+w])
            cv2.putText(frame,'Tekan ENTER untuk Ambil Gambar', (360, 640),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Face image captured', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 13:
            print("Face image captured and saved!")
            camera.release()
            cv2.destroyAllWindows()
            break

def start_recording():
    nama = entry_nama.get()
    rekamWajah(nama)

    subprocess.run(['python', 'train.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    back_to_menu()

def back_to_menu():
    root.destroy()

root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")

root.title("Face Capture")

window_width = 500 
window_height = 350

title = ttk.Label(root, text="Daftar Face Recognition", background=root.cget("background"))
title.pack(pady=50)

label_nama = ttk.Label(root, text="Masukkan Nama", font=("Helvetica", 12), background=root.cget("background"), foreground="black")
label_nama.pack()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
    
x_coordinate = int((screen_width/2) - (window_width/2))
y_coordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))  

label_text_color="#FF5733" 
button_bg_color="#FFC300"

style.configure('TLabel', foreground=label_text_color, font=("Helvetica", 16, "bold"))
style.configure('TButton', background=button_bg_color)

entry_nama = ttk.Entry(root, width=40)
entry_nama.pack(pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(pady=65)

button_start = ttk.Button(button_frame, text="Start", command=start_recording, width=20)
button_start.pack(side="left", padx=5)

button_back = ttk.Button(button_frame, text="Back", command=back_to_menu, width=20)
button_back.pack(side="left", padx=5)

root.mainloop()

if __name__ == "__main__":

    os.system('python train.py')