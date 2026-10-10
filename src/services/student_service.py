import json
import os
from datetime import datetime

from src.models.student import Student
from src.utils.logger import logger


class StudentService:
    def __init__(self, data_file="data/students.json"):
        self.data_file = data_file
        folder = os.path.dirname(data_file)

        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(data_file):
            self._save_students([])

    def _load_students(self):
        with open(self.data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_students(self, students):
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)

    def add_student(self, student_data):
        students = self._load_students()

        student_id = student_data.get("student_id", "").strip()
        if not student_id:
            import uuid
            student_id = str(uuid.uuid4())[:8]

        if any(s["student_id"] == student_id for s in students):
            raise ValueError("Student ID already exists.")

        student = Student(
            name=student_data["name"],
            email=student_data["email"],
            course=student_data["course"],
            year_level=student_data["year_level"],
            student_id=student_id,
            gpa=student_data.get("gpa", 0.0)
        )

        students.append(student.to_dict())
        self._save_students(students)
        logger.info("Added student ID: %s", student_id)
        return student.to_dict()

    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        for student in self._load_students():
            if student["student_id"] == student_id:
                return student
        return None

    def update_student(self, student_id, update_data):
        students = self._load_students()

        for student in students:
            if student["student_id"] == student_id:
                for field in ["name", "email", "course", "year_level", "gpa"]:
                    if field in update_data:
                        student[field] = update_data[field]

                student["updated_at"] = datetime.now().isoformat()
                self._save_students(students)
                return student

        return None

    def delete_student(self, student_id):
        students = self._load_students()
        remaining = [
            student for student in students
            if student["student_id"] != student_id
        ]

        if len(remaining) == len(students):
            return False

        self._save_students(remaining)
        return True