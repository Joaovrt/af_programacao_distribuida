import requests
import time

BASE_URL = "http://localhost:5000"

def print_step(name):
    print(f"\n=== {name} ===")

def test_create_student(name="João"):
    print_step("Create Student")
    res = requests.post(f"{BASE_URL}/students", json={"name": name})
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

def test_get_student(student_id):
    print_step("Get Student")
    res = requests.get(f"{BASE_URL}/students/{student_id}")
    print(res.json())

def test_list_students():
    print_step("List Students")
    res = requests.get(f"{BASE_URL}/students")
    print(res.json())

def test_update_student(student_id, name):
    print_step("Update Student")
    res = requests.put(f"{BASE_URL}/students/{student_id}", json={"name": name})
    print(res.json())

def test_delete_student(student_id):
    print_step("Delete Student")
    res = requests.delete(f"{BASE_URL}/students/{student_id}")
    print("deleted", res.status_code)

# Teachers
def test_create_teacher(name="Prof. Ana"):
    print_step("Create Teacher")
    res = requests.post(f"{BASE_URL}/teachers", json={"name": name})
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

def test_list_teachers():
    print_step("List Teachers")
    res = requests.get(f"{BASE_URL}/teachers")
    print(res.json())

def test_create_subject(name="Matemática"):
    print_step("Create Subject")
    res = requests.post(f"{BASE_URL}/subjects", json={"name": name})
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

def test_list_subjects():
    print_step("List Subjects")
    res = requests.get(f"{BASE_URL}/subjects")
    print(res.json())

# Classes
def test_create_class(teacher_id, subject_id, schedule="Seg 08:00-10:00"):
    print_step("Create Class")
    payload = {"teacher_id": teacher_id, "subject_id": subject_id, "schedule": schedule}
    res = requests.post(f"{BASE_URL}/classes", json=payload)
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

def test_get_class(class_id):
    print_step("Get Class")
    res = requests.get(f"{BASE_URL}/classes/{class_id}")
    print(res.json())

def test_list_classes():
    print_step("List Classes")
    res = requests.get(f"{BASE_URL}/classes")
    print(res.json())

def test_get_classes_by_teacher(teacher_id):
    print_step("Get Classes By Teacher")
    res = requests.get(f"{BASE_URL}/teachers/{teacher_id}/classes")
    print(res.json())

def test_get_classes_by_subject(subject_id):
    print_step("Get Classes By Subject")
    res = requests.get(f"{BASE_URL}/subjects/{subject_id}/classes")
    print(res.json())

def test_enroll_student(class_id, student_id):
    print_step("Enroll Student")
    payload = {"student_id": student_id}
    res = requests.post(f"{BASE_URL}/classes/{class_id}/enroll", json=payload)
    res.raise_for_status()
    print(res.json())

def run_all_tests():
    print("Aguarde… garantindo que o servidor gRPC + Flask já estão rodando.")
    time.sleep(1)

    # Students
    student_id = test_create_student("João")
    test_get_student(student_id)
    test_list_students()
    test_update_student(student_id, "João Atualizado")
    test_get_student(student_id)

    # Teachers & Subjects
    teacher_id = test_create_teacher("Prof. Ana")
    test_list_teachers()
    subject_id = test_create_subject("Matemática")
    test_list_subjects()

    # Classes
    class_id = test_create_class(teacher_id, subject_id)
    test_get_class(class_id)
    test_list_classes()

    # Teacher sees his classes
    test_get_classes_by_teacher(teacher_id)

    # Subject classes
    test_get_classes_by_subject(subject_id)

    # Enroll
    test_enroll_student(class_id, student_id)
    test_get_class(class_id)
    test_list_classes()

    # Optional: cleanup (delete)
    # test_delete_student(student_id)

    print("\n\n=== TODOS OS TESTES FINALIZADOS COM SUCESSO ===")

if __name__ == "__main__":
    run_all_tests()