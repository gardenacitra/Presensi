from PIL import Image
from keras.models import load_model
import numpy as np
from numpy import asarray
from numpy import expand_dims
import pickle
import cv2
import os
import datetime
import mysql.connector
import tkinter as tk
from tkinter import ttk

def faceReg(mata_kuliah):
    HaarCascade = cv2.CascadeClassifier('Assets/Model/haarcascade_frontalface_default.xml')
    MyFaceNet = load_model('Assets/Model/facenet_keras.h5')

    with open("Assets/Train/data.pkl", "rb") as myfile:
        database = pickle.load(myfile)

    output_dir = 'Output'
    os.makedirs(output_dir, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video_base = 'output.mp4'
    output_video = os.path.join(output_dir, output_video_base)
    video_count = 0

    while os.path.exists(output_video):
        video_count += 1
        output_video = os.path.join(output_dir, f'output_{video_count}.mp4')

    out = cv2.VideoWriter(output_video, fourcc, 20.0, (640, 480))

    cap = cv2.VideoCapture(0)

    def verify_face(embedding, name, threshold=0.75):
        if name not in database:
            return False

        reference_embedding = database[name]
        similarity = np.dot(embedding, reference_embedding.T) / (np.linalg.norm(embedding) * np.linalg.norm(reference_embedding))
        
        if similarity > threshold:
            return True
        else:
            return False

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_attendance"
    )

    today = datetime.date.today().strftime("%d_%m_%Y")

    cursor = mydb.cursor()
    cursor.execute("Show TABLES LIKE %s", (today,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute(f"CREATE TABLE {today} (name VARCHAR(30), time VARCHAR(10), mata_kuliah VARCHAR(50), jumlah INTEGER(3))")
        cursor.execute(f"INSERT INTO {today} (name, time, mata_kuliah, jumlah) VALUES (%s, %s, %s, %s)", ('TOTAL', ' ',' ',' '))
        mydb.commit()

    cursor.close()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        recognized_names = []

        if len(recognized_names) > 0:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            cursor = mydb.cursor()

        frame = cv2.flip(frame, 1)

        wajah = HaarCascade.detectMultiScale(frame, 1.1, 4)
        num_faces_detected = len(wajah)

        for i, w in enumerate(wajah):
            x1, y1, width, height = w
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height

            gbr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gbr = Image.fromarray(gbr)
            gbr_array = asarray(gbr)

            face = gbr_array[y1:y2, x1:x2]
            face = Image.fromarray(face)
            face = face.resize((160, 160))
            face = asarray(face)

            face = face.astype('float32')
            mean, std = face.mean(), face.std()
            face = (face - mean) / std

            face = expand_dims(face, axis=0)
            signature = MyFaceNet.predict(face)

            min_dist = 100
            identity = 'unknown'
            for key in database.keys():
                if verify_face(signature, key):
                    identity = key
                    break

            cv2.putText(frame, identity, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            recognized_names.append(identity)

        if len(recognized_names) > 0:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            cursor = mydb.cursor()

            with open("Assets/Train/data.pkl", "rb") as myfile:
                database = pickle.load(myfile)

            for name in recognized_names:
                if name != 'unknown':
                    cursor.execute(f"SELECT * FROM {today} WHERE name = %s", (name,))
                    result = cursor.fetchone()

                    if result is None:
                        sql = f"INSERT INTO {today} (name, time, mata_kuliah) VALUES (%s,%s,%s)"
                        val = (name, current_time, mata_kuliah)
                        cursor.execute(sql, val)
                        mydb.commit()

                cursor.execute(f"SELECT * FROM {today} WHERE name != 'TOTAL'")
                rows = cursor.fetchall()
                row_count = len(rows)
                cursor.execute(f"UPDATE {today} SET jumlah = %s WHERE name = %s", (row_count, 'TOTAL'))
            mydb.commit()

        cv2.putText(frame, f"jumlah {num_faces_detected}", (25, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Face Recognition', frame)

        out.write(frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()

def start_recording():
    mata_kuliah = entry_nama.get()
    faceReg(mata_kuliah)

def back_to_menu():
    root.destroy()

root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")

root.title("Face Recognition")

window_width = 500 
window_height = 350

title = ttk.Label(root, text="Face Recognition", background=root.cget("background"))
title.pack(pady=50)

label_nama = ttk.Label(root, text="Masukkan Mata Kuliah", font=("Helvetica", 12), background=root.cget("background"), foreground="black")
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