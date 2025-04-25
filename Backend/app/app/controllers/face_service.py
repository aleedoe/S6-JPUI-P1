import face_recognition
import numpy as np
from app.models.student import Student
import os
import json
from flask import current_app


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

ALLOWED_EXTENSIONS = current_app.config['ALLOWED_EXTENSIONS']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load dataset dan buat encoding wajah
def load_dataset():
    known_face_encodings = []
    known_face_names = []
    known_face_nis = []
    known_face_grades = []
    
    # Loop melalui setiap kelas (kelas-1 sampai kelas-6)
    DATASET_FOLDER = current_app.config['DATASET_FOLDER']
    for grade_folder in os.listdir(DATASET_FOLDER):
        grade_path = os.path.join(DATASET_FOLDER, grade_folder)
        if os.path.isdir(grade_path) and grade_folder.startswith('kelas-'):
            grade_name = grade_folder.replace('kelas-', 'Kelas ')
            
            # Loop melalui setiap siswa dalam kelas
            for student_folder in os.listdir(grade_path):
                student_path = os.path.join(grade_path, student_folder)
                if os.path.isdir(student_path):
                    # Asumsi nama folder adalah nama siswa
                    student_name = student_folder
                    
                    # Cari data siswa di database
                    student = Student.query.filter_by(name=student_name, grade_id=int(grade_folder.split('-')[1])).first()
                    if not student:
                        continue
                    
                    # Loop melalui setiap gambar siswa
                    for image_file in os.listdir(student_path):
                        image_path = os.path.join(student_path, image_file)
                        
                        # Load gambar dan dapatkan encoding wajah
                        image = face_recognition.load_image_file(image_path)
                        face_encodings = face_recognition.face_encodings(image)
                        
                        if len(face_encodings) > 0:
                            known_face_encodings.append(face_encodings[0])
                            known_face_names.append(student.name)
                            known_face_nis.append(student.nis)
                            known_face_grades.append(grade_name)
    
    return known_face_encodings, known_face_names, known_face_nis, known_face_grades
