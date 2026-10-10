
from datetime import datetime
import uuid


class Student:
    def __init__(
        self,
        name,
        email,
        course,
        year_level,
        student_id=None,
        gpa=0.0
    ):
        # Generate an ID if one was not provided.
        self.student_id = student_id or str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.course = course
        self.year_level = year_level
        self.gpa = gpa

        # Record creation and update times.
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self):
        # Convert the student object into a dictionary.
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "course": self.course,
            "year_level": self.year_level,
            "gpa": self.gpa,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
