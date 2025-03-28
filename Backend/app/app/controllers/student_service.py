from flask import request, jsonify
from models import db, Student, StudentImage
from .storage_service import StorageService
import face_recognition
import numpy as np
import json
import os

def register_student():
    if 'photos' not in request.files or 'name' not in request.form or 'nis' not in request.form or 'class_id' not in request.form:
        return jsonify({'error': 'Missing required data'}), 400
        
    photos = request.files.getlist('photos')
    name = request.form['name']
    nis = request.form['nis']
    class_id = request.form['class_id']
    
    if len(photos) < 3:
        return jsonify({'error': 'At least 3 photos are required'}), 400
        
    try:
        # Proses semua foto untuk mendapatkan encoding
        encodings = []
        for photo in photos:
            temp_path = StorageService.save_temp(photo)
            image = face_recognition.load_image_file(temp_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                StorageService.delete_temp(temp_path)
                return jsonify({'error': f'No face detected in one of the photos'}), 400
                
            encodings.append(face_encodings[0])
            StorageService.delete_temp(temp_path)
            
        # Rata-rata encoding untuk mendapatkan template wajah
        avg_encoding = np.mean(encodings, axis=0)
        encoding_str = json.dumps(avg_encoding.tolist())
        
        # Buat record siswa
        student = Student(
            name=name,
            nis=nis,
            class_id=class_id,
            face_encoding=encoding_str
        )
        
        db.session.add(student)
        db.session.commit()
        
        # Simpan foto-foto siswa
        for photo in photos:
            image_url = StorageService.save_student_photo(photo, student.id)
            student_image = StudentImage(
                student_id=student.id,
                image_url=image_url
            )
            db.session.add(student_image)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Student registered successfully',
            'student_id': student.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500