
import json
import logging
import os

from src.services.student_service import StudentService
from src.utils.logger import logger


class StudentInformationSystem:
    def __init__(self):
        try:
            with open(
                "config/config.json", "r", encoding="utf-8"
            ) as file:
                config = json.load(file)

            self.student_service = StudentService(
                config.get("data_file", "data/students.json")
            )

            logger.info("Application started.")

        except (OSError, json.JSONDecodeError, KeyError) as error:
            logger.error("Application setup failed: %s", error)
            raise

    def display_menu(self):
        print("\n===== STUDENT INFORMATION SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

    def add_student(self):
        print("\n--- Add New Student ---")

        student_data = {
            "student_id": input("Student ID (optional): ").strip(),
            "name": input("Name: ").strip(),
            "email": input("Email: ").strip(),
            "course": input("Course: ").strip(),
            "year_level": input("Year Level: ").strip()
        }

        if not all(
            student_data[field]
            for field in ["name", "email", "course", "year_level"]
        ):
            print("Please complete all required fields.")
            return

        try:
            student = self.student_service.add_student(student_data)

            print("Student added successfully!")
            print("Student ID:", student["student_id"])
            logger.info("Added student successfully.")

        except (ValueError, KeyError, OSError) as error:
            logger.error("Error adding student: %s", error)
            print("Error adding student:", error)

    def view_all_students(self):
        print("\n--- All Students ---")

        try:
            students = self.student_service.get_all_students()

            if not students:
                print("No students found.")
                return

            for student in students:
                print("-" * 35)
                print("ID:", student["student_id"])
                print("Name:", student["name"])
                print("Email:", student["email"])
                print("Course:", student["course"])
                print("Year Level:", student["year_level"])
                print("GPA:", student.get("gpa", 0.0))

        except (OSError, ValueError, json.JSONDecodeError) as error:
            logger.error("Error viewing students: %s", error)
            print("Unable to load student records.")

    def view_student_by_id(self):
        student_id = input("Enter Student ID: ").strip()

        try:
            student = self.student_service.get_student(student_id)

            if student:
                print("\n--- Student Details ---")
                for key, value in student.items():
                    print(f"{key}: {value}")
            else:
                print("Student not found.")

        except (OSError, ValueError) as error:
            logger.error("Error searching student: %s", error)
            print("Unable to search student records.")

    def update_student(self):
        student_id = input("Enter Student ID to update: ").strip()

        try:
            student = self.student_service.get_student(student_id)

            if not student:
                print("Student not found.")
                return

            print("Press Enter to keep the current value.")

            update_data = {}

            for field in ["name", "email", "course", "year_level"]:
                current = student[field]
                new_value = input(
                    f"{field.replace('_', ' ').title()} [{current}]: "
                ).strip()

                if new_value:
                    update_data[field] = new_value

            if not update_data:
                print("No changes entered.")
                return

            updated = self.student_service.update_student(
                student_id, update_data
            )

            if updated:
                print("Student updated successfully.")
            else:
                print("Student not found.")

        except (OSError, ValueError) as error:
            logger.error("Error updating student: %s", error)
            print("Unable to update student:", error)

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ").strip()

        try:
            student = self.student_service.get_student(student_id)

            if not student:
                print("Student not found.")
                return

            confirm = input(
                f"Delete {student['name']}? (y/n): "
            ).strip().lower()

            if confirm != "y":
                print("Deletion cancelled.")
                return

            if self.student_service.delete_student(student_id):
                print("Student deleted successfully.")
            else:
                print("Student could not be deleted.")

        except (OSError, ValueError) as error:
            logger.error("Error deleting student: %s", error)
            print("Unable to delete student:", error)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_all_students()
            elif choice == "3":
                self.view_student_by_id()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                logger.info("Application closed.")
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 to 6.")


if __name__ == "__main__":
    try:
        app = StudentInformationSystem()
        app.run()
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print("Unable to start the application:", error)
