import pandas as pd
import datetime
import mysql.connector
import os

def get_attendance_data():
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
        print("Tabel untuk tanggal hari ini belum tersedia di database.")
        return None

    cursor.execute(f"SELECT * FROM {today}")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=['Nama', 'Waktu', 'Mata Kuliah', 'Jumlah Hadir'])

    return df

def save_to_excel(dataframe, file_path):
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    dataframe.to_excel(writer, index=False)
    writer.save()
    print("Data berhasil disimpan dalam file Excel.")

attendance_data = get_attendance_data()

if attendance_data is not None:
    today = datetime.date.today().strftime("%d %m %Y")
    folder_name = "Result"
    os.makedirs(folder_name, exist_ok=True)
    file_name = f'Attendance_{today}.xlsx'
    file_path = os.path.join(folder_name, file_name)
    save_to_excel(attendance_data, file_path)
    # print(f"File berhasil disimpan di folder {folder_name}.")
else:
    print("Tidak ada data attendance untuk disimpan.")