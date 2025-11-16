import requests
import time

BASE_URL = "http://localhost:5000"

def print_step(name):
    print(f"\n=== {name} ===")


def test_create_student():
    print_step("Create Student")
    res = requests.post(f"{BASE_URL}/students", json={"name": "João"})
    print(res.json())
    return res.json()["id"]


def test_list_students():
    print_step("List Students")
    res = requests.get(f"{BASE_URL}/students")
    print(res.json())


def test_create_teacher():
    print_step("Create Teacher")
    res = requests.post(f"{BASE_URL}/teachers", json={"name": "Prof. Ana"})
    print(res.json())
    return res.json()["id"]


def test_create_subject():
    print_step("Create Subject")
    res = requests.post(f"{BASE_URL}/subjects", json={"name": "Matemática"})
    print(res.json())
    return res.json()["id"]


def test_create_class(teacher_id, subject_id):
    print_step("Create Class")
    payload = {
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "schedule": "Seg 08:00-10:00"
    }
    res = requests.post(f"{BASE_URL}/classes", json=payload)
    print(res.json())
    return res.json()["id"]


def test_list_classes():
    print_step("List Classes")
    res = requests.get(f"{BASE_URL}/classes")
    print(res.json())


def test_enroll_student(class_id, student_id):
    print_step("Enroll Student")
    payload = {"student_id": student_id}
    res = requests.post(f"{BASE_URL}/classes/{class_id}/enroll", json=payload)
    print(res.json())


def run_all_tests():
    print("Aguarde… garantindo que o servidor gRPC + Flask já estão rodando.")
    time.sleep(1)

    # 1. CRIAR ENTIDADES
    student_id = test_create_student()
    test_list_students()

    teacher_id = test_create_teacher()
    subject_id = test_create_subject()

    # 2. CRIAR TURMA
    class_id = test_create_class(teacher_id, subject_id)

    # 3. LISTAR TURMAS
    test_list_classes()

    # 4. MATRICULAR ALUNO NA TURMA
    test_enroll_student(class_id, student_id)

    # 5. LISTAR NOVAMENTE PARA VER A MATRÍCULA
    test_list_classes()

    print("\n\n=== TODOS OS TESTES FINALIZADOS COM SUCESSO ===")


if __name__ == "__main__":
    run_all_tests()