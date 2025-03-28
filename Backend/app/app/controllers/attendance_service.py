from flask import request, jsonify
from models import db, Attendance, Student
from .storage_service import StorageService
from .face_service import FaceService
import datetime


def take_attendance():
    if 'photo' not in request.files or 'class_id' not in request.form:
        return jsonify({'error': 'Photo and class_id are required'}), 400
        
    photo = request.files['photo']
    class_id = request.form['class_id']
    
    # Simpan foto sementara
    temp_path = StorageService.save_temp(photo)
    
    try:
        # Kenali wajah
        student_id = FaceService.recognize_face(temp_path, class_id)
        
        if not student_id:
            return jsonify({'error': 'Student not recognized'}), 404
            
        # Simpan foto ke storage permanen
        photo_url = StorageService.save_attendance_photo(photo, student_id)
        
        # Buat record presensi
        attendance = Attendance(
            student_id=student_id,
            status='H',  # Default: Hadir
            photo_url=photo_url,
            created_at=datetime.datetime.utcnow()
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        student = Student.query.get(student_id)
        
        return jsonify({
            'message': 'Attendance recorded',
            'student': {
                'id': student.id,
                'name': student.name,
                'nis': student.nis
            },
            'photo_url': photo_url
        }), 200
        
    finally:
        # Hapus file temp
        StorageService.delete_temp(temp_path)