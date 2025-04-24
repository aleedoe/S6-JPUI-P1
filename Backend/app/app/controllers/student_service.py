from flask import request, jsonify
from app.models import db, Student, StudentImage
from .storage_service import StorageService
import face_recognition
import numpy as np
import json
from PIL import Image
import io
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
        encodings = []
        for photo in photos:
            # Validasi file
            if not photo.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                return jsonify({'error': 'Only JPG/JPEG/PNG files are allowed'}), 400
            
            # Baca file sebagai bytes
            img_bytes = photo.read()
            
            try:
                # Coba buka gambar dengan PIL
                img = Image.open(io.BytesIO(img_bytes))
                
                # Konversi ke RGB jika diperlukan
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                # Simpan ke temporary file dalam format yang benar
                temp_path = os.path.join('temp', f"temp_{photo.filename}")
                img.save(temp_path, 'JPEG')
                
                # Proses dengan face_recognition
                image = face_recognition.load_image_file(temp_path)
                face_encodings = face_recognition.face_encodings(image)
                
                if len(face_encodings) == 0:
                    StorageService.delete_temp(temp_path)
                    return jsonify({'error': f'No face detected in: {photo.filename}'}), 400
                    
                encodings.append(face_encodings[0])
                StorageService.delete_temp(temp_path)
                
            except Exception as img_error:
                return jsonify({'error': f'Invalid image file: {photo.filename}. Error: {str(img_error)}'}), 400
                
        # Lanjutkan dengan proses registrasi...
        avg_encoding = np.mean(encodings, axis=0)
        encoding_str = json.dumps(avg_encoding.tolist())
        
        student = Student(
            name=name,
            nis=nis,
            class_id=class_id,
            face_encoding=encoding_str
        )
        
        db.session.add(student)
        db.session.commit()
        
        # Simpan foto asli (tanpa konversi)
        for photo in photos:
            photo.seek(0)  # Reset file pointer
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


def get_all_students():
    try:
        students = Student.query.all()
        data = []

        for student in students:
            # Ambil semua gambar yang sesuai student_id
            images = StudentImage.query.filter_by(student_id=student.id).all()
            image_data = [img.to_dict() for img in images]

            student_dict = {
                "id": student.id,
                "name": student.name,
                "nis": student.nis,
                "grade_id": student.grade_id,
                "face_encoding": student.face_encoding,
                "created_at": student.created_at.isoformat(),
                "images": image_data
            }
            data.append(student_dict)

        return jsonify({
            "status": "success",
            "message": "Data siswa berhasil diambil.",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal mengambil data: {str(e)}"
        }), 500

def get_student_by_id(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({
                "status": "error",
                "message": f"Siswa dengan ID {student_id} tidak ditemukan."
            }), 404

        # Ambil semua gambar yang terkait student ini
        images = StudentImage.query.filter_by(student_id=student.id).all()
        image_data = [img.to_dict() for img in images]

        student_data = {
            "id": student.id,
            "name": student.name,
            "nis": student.nis,
            "grade_id": student.grade_id,
            "face_encoding": student.face_encoding,
            "created_at": student.created_at.isoformat(),
            "images": image_data
        }

        return jsonify({
            "status": "success",
            "message": "Data siswa berhasil diambil.",
            "data": student_data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Gagal mengambil data siswa: {str(e)}"
        }), 500