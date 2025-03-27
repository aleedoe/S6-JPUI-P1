from flask import request, jsonify
import face_recognition
from app.models.student import Student
from app import db
import numpy as np
import base64
import cv2
from datetime import datetime


# Fungsi untuk menyimpan wajah siswa ke database
def register_face():
    data = request.json
    name = data["name"]
    nis = data["nis"]
    face_images = data["face_images"]  # Menerima list gambar base64

    # Cek apakah siswa sudah ada di database
    cursor.execute("SELECT id FROM students WHERE nis = %s", (nis,))
    student = cursor.fetchone()

    if student:
        student_id = student[0]
    else:
        # Jika belum ada, tambahkan siswa ke database
        cursor.execute("INSERT INTO students (name, nis) VALUES (%s, %s)", (name, nis))
        db.commit()
        student_id = cursor.lastrowid  # Ambil ID siswa yang baru dimasukkan

    # Loop setiap gambar wajah yang dikirimkan
    for face_image in face_images:
        face_bytes = base64.b64decode(face_image)
        np_arr = np.frombuffer(face_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Deteksi dan encode wajah
        face_locations = face_recognition.face_locations(frame)
        if not face_locations:
            return jsonify({"error": "Tidak ada wajah terdeteksi dalam salah satu gambar"}), 400

        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        face_encoding_str = ",".join(map(str, face_encoding))

        # Simpan encoding ke tabel student_faces
        cursor.execute("INSERT INTO student_faces (student_id, face_encoding) VALUES (%s, %s)", (student_id, face_encoding_str))
        db.commit()

    return jsonify({"message": "✅ Semua wajah berhasil disimpan!", "name": name})


def register_face():
    data = request.json
    name = data["name"]
    nis = data["nis"]
    face_image = base64.b64decode(data["face_image"])  # Decode gambar dari base64

    # Convert ke array numpy untuk diproses
    np_arr = np.frombuffer(face_image, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Deteksi wajah & ambil encoding
    face_locations = face_recognition.face_locations(frame)
    if not face_locations:
        return jsonify({"error": "Tidak ada wajah terdeteksi"}), 400
    
    face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
    face_encoding_str = ",".join(map(str, face_encoding))  # Simpan sebagai string

    # Simpan ke database
    new_student = Student(name=name, nis=nis, face_encoding=face_encoding_str)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "✅ Wajah berhasil disimpan!", "name": name})