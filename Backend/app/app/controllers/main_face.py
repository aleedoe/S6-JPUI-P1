from flask import request, jsonify
import face_recognition
from app.models.student import Student
from app import db
import numpy as np
import base64
import cv2
from datetime import datetime
from app.models.student_image import StudentImage
import os

# Fungsi untuk menyimpan wajah siswa ke database
def register_face():
    data = request.json
    name = data["name"]
    nis = data["nis"]
    face_image = base64.b64decode(data["face_image"])  # Decode base64 ke gambar

    # Cek apakah siswa sudah terdaftar
    student = Student.query.filter_by(nis=nis).first()
    if not student:
        student = Student(name=name, nis=nis)
        db.session.add(student)
        db.session.commit()

    # Buat folder dataset jika belum ada
    student_folder = f"dataset/{nis}"
    os.makedirs(student_folder, exist_ok=True)

    # Simpan gambar
    image_count = len(os.listdir(student_folder)) + 1
    image_path = f"{student_folder}/photo_{image_count}.jpg"
    with open(image_path, "wb") as img_file:
        img_file.write(face_image)

    # Simpan path gambar ke database
    new_image = StudentImage(student_id=student.id, image_path=image_path)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "✅ Wajah berhasil disimpan!", "name": name, "image_path": image_path})


def recognize_face():
    face_image = base64.b64decode(request.json["face_image"])  # Decode gambar dari base64
    np_arr = np.frombuffer(face_image, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Load data siswa dari database
    cursor.execute("SELECT id, name, face_encoding FROM students")
    students = cursor.fetchall()

    # Ambil encoding wajah dari input
    face_locations = face_recognition.face_locations(frame)
    if not face_locations:
        return jsonify({"error": "Tidak ada wajah terdeteksi"}), 400

    face_encoding_input = face_recognition.face_encodings(frame, face_locations)[0]

    # Loop semua siswa dan bandingkan wajah
    for student in students:
        student_id, name, face_encoding_str = student
        known_encoding = np.array(list(map(float, face_encoding_str.split(","))))  # Konversi string ke array

        match = face_recognition.compare_faces([known_encoding], face_encoding_input, tolerance=0.5)
        if match[0]:
            # Simpan presensi ke database
            cursor.execute("INSERT INTO attendance (student_id) VALUES (%s)", (student_id,))
            db.commit()

            return jsonify({"message": "✅ Presensi berhasil!", "name": name, "timestamp": datetime.now().isoformat()})

    return jsonify({"error": "❌ Wajah tidak dikenali"}), 400