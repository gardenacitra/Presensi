import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess

def run_face_recognition():
    subprocess.Popen(['python', 'main.py'])

def open_output_folder():
    output_dir = 'Output'
    if os.path.exists(output_dir):
        subprocess.Popen(['explorer', output_dir])

def open_attendance_result():
    subprocess.Popen(['python', 'export.py'])

def register_face():
    subprocess.Popen(['python', 'opencam.py'])

def exit_program():
    root.destroy()

def main():
    global root
    root = tk.Tk()
        
    style = ttk.Style(root)
        
    style.theme_use("clam")

    root.title("Face Recognition App")
 
    window_width = 500 
    window_height = 350
        
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
        
    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))  

    label_text_color="#FF5733" 
    button_bg_color="#FFC300"

    style.configure('TLabel', foreground=label_text_color, font=("Helvetica", 16, "bold"))
    style.configure('TButton', background=button_bg_color)

    label = ttk.Label(root, text="Face Recognition App", background=root.cget("background"))
    label.pack(pady=35)

    button_frame = ttk.Frame(root)
    button_frame.pack(padx=10, pady=30)

    register_button = ttk.Button(button_frame, text="Register", command=register_face, width=30)
    register_button.grid(row=0, column=0, padx=5, pady=10)

    start_button = ttk.Button(button_frame, text="Start Face Recognition", command=run_face_recognition, width=30)
    start_button.grid(row=0, column=1, padx=5, pady=10)

    open_folder_button = ttk.Button(button_frame, text="Open Output Folder", command=open_output_folder, width=30)
    open_folder_button.grid(row=1, column=0, padx=5, pady=10)

    open_attendance_button = ttk.Button(button_frame, text="Get Attendance Result", command=open_attendance_result, width=30)
    open_attendance_button.grid(row=1, column=1, padx=5, pady=10)

    exit_button = ttk.Button(root, text="Exit", command=exit_program, width=30)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()