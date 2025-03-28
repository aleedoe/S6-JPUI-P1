import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

class StorageService:
    UPLOAD_FOLDER = 'uploads'
    STUDENT_FOLDER = 'student_images'
    ATTENDANCE_FOLDER = 'attendance_images'
    
    @staticmethod
    def ensure_folder_exists(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    @staticmethod
    def save_temp(file):
        StorageService.ensure_folder_exists('temp')
        filename = f"temp_{uuid.uuid4().hex}.jpg"
        temp_path = os.path.join('temp', filename)
        file.save(temp_path)
        return temp_path
        
    @staticmethod
    def delete_temp(temp_path):
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    @staticmethod
    def save_student_photo(file, student_id):
        StorageService.ensure_folder_exists(StorageService.STUDENT_FOLDER)
        student_folder = os.path.join(StorageService.STUDENT_FOLDER, str(student_id))
        StorageService.ensure_folder_exists(student_folder)
        
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(student_folder, filename)
        file.save(filepath)
        
        return filepath
        
    @staticmethod
    def save_attendance_photo(file, student_id):
        StorageService.ensure_folder_exists(StorageService.ATTENDANCE_FOLDER)
        today = datetime.now().strftime('%Y-%m-%d')
        daily_folder = os.path.join(StorageService.ATTENDANCE_FOLDER, today)
        StorageService.ensure_folder_exists(daily_folder)
        
        filename = f"{student_id}_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(daily_folder, filename)
        file.save(filepath)
        
        return filepath