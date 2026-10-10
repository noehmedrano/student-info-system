
import tempfile
import unittest
import os

from src.services.student_service import StudentService


class TestStudentService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(
            self.temp_dir.name, "students.json"
        )
        self.service = StudentService(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_student(self):
        student = self.service.add_student({
            "student_id": "TEST001",
            "name": "Juan Dela Cruz",
            "email": "juan@example.com",
            "course": "BSIT",
            "year_level": "3"
        })

        self.assertEqual(student["student_id"], "TEST001")
        self.assertEqual(len(self.service.get_all_students()), 1)

    def test_find_student(self):
        self.service.add_student({
            "student_id": "TEST002",
            "name": "Maria Santos",
            "email": "maria@example.com",
            "course": "BSIT",
            "year_level": "2"
        })

        student = self.service.get_student("TEST002")
        self.assertEqual(student["name"], "Maria Santos")

    def test_update_student(self):
        self.service.add_student({
            "student_id": "TEST003",
            "name": "Pedro Cruz",
            "email": "pedro@example.com",
            "course": "BSIT",
            "year_level": "1"
        })

        updated = self.service.update_student(
            "TEST003", {"course": "BSCS"}
        )

        self.assertEqual(updated["course"], "BSCS")

    def test_delete_student(self):
        self.service.add_student({
            "student_id": "TEST004",
            "name": "Ana Reyes",
            "email": "ana@example.com",
            "course": "BSIT",
            "year_level": "4"
        })

        result = self.service.delete_student("TEST004")

        self.assertTrue(result)
        self.assertEqual(self.service.get_all_students(), [])

    def test_duplicate_id(self):
        student_data = {
            "student_id": "TEST005",
            "name": "Test Student",
            "email": "test@example.com",
            "course": "BSIT",
            "year_level": "1"
        }

        self.service.add_student(student_data)

        with self.assertRaises(ValueError):
            self.service.add_student(student_data)


if __name__ == "__main__":
    unittest.main()
