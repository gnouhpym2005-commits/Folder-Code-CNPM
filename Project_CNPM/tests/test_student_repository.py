from database.student_repository import StudentRepository
repo = StudentRepository()
students = repo.get_all()
for student in students:
    print(student)