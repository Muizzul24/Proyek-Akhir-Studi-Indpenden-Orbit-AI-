import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import numpy as np
import cv2

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Ganti dengan host server Anda
            user="root",       # Username MySQL
            password="",  # Ganti dengan password MySQL Anda
            database="facebase"        # Nama database yang baru saja dibuat
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Kesalahan koneksi database: {err}")
        return None

def register_new_user(user_id, name, age, address, college, hog_features):
    conn = connect_to_database()
    
    if not conn:
        return "Koneksi ke database gagal. Mohon periksa konfigurasi database Anda."
    
    try:
        cursor = conn.cursor()
        
        # Query untuk menyimpan data
        cursor.execute(
            "INSERT INTO users (id, nama, umur, alamat, kuliah, hog_features) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, name, age, address, college, hog_features.tobytes())  # Simpan fitur HOG sebagai bytes
        )
        
        conn.commit()  # Simpan perubahan ke database
        return "Registrasi berhasil!"
    except Exception as e:
        return f"Error saat menyimpan data: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def verify_user(hog_features):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nama, umur, alamat, kuliah, hog_features FROM user")
    results = cursor.fetchall()
    
    for row in results:
        user_id, name, age, address, college, stored_hog_features = row
        stored_hog_features = np.frombuffer(stored_hog_features, dtype=np.float64)  # Memastikan dtype sesuai
        
        # Hitung jarak antara fitur HOG login dan fitur yang disimpan
        distance = np.linalg.norm(hog_features - stored_hog_features)
        
        if distance < 10:  # Misalnya threshold 10
            return user_id, name, age, address, college  # Kembalikan informasi pengguna

    return 'unknown_person'

