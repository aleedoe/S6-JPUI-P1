import face_recognition
import numpy as np
from app.models.student import Student
import os
import json

class FaceService:
    @staticmethod
    def load_student_encodings(class_id):
        """Muat encoding wajah siswa dari database berdasarkan kelas"""
        students = Student.query.filter_by(class_id=class_id).all()
        encodings = []
        student_ids = []
        
        for student in students:
            encoding = json.loads(student.face_encoding)
            encodings.append(np.array(encoding))
            student_ids.append(student.id)
            
        return encodings, student_ids

    @staticmethod
    def recognize_face(image_path, class_id):
        """Mengenali wajah dari gambar yang diupload"""
        try:
            # Muat encoding yang sudah ada
            known_encodings, known_ids = FaceService.load_student_encodings(class_id)
            
            # Muat gambar yang diupload
            unknown_image = face_recognition.load_image_file(image_path)
            unknown_encoding = face_recognition.face_encodings(unknown_image)
            
            if len(unknown_encoding) == 0:
                return None
                
            # Bandingkan dengan encoding yang ada
            matches = face_recognition.compare_faces(known_encodings, unknown_encoding[0], tolerance=0.6)
            
            if True in matches:
                matched_idx = matches.index(True)
                return known_ids[matched_idx]
                
            return None
        except Exception as e:
            print(f"Error in face recognition: {e}")
            return None