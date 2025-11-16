import requests
import time

BASE_URL = "http://localhost:5000"

def print_step(name):
    print(f"\n=== {name} ===")

# -----------------------------
# CREATE
# -----------------------------

def test_create_student(name="João"):
    print_step("Create Student")
    res = requests.post(f"{BASE_URL}/students", json={"name": name})
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

def test_create_teacher(name="Prof. Ana"):
    print_step("Create Teacher")
    res = requests.post(f"{BASE_URL}/teachers", json={"name": name})
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

def test_create_subject(name, teacher_id):
    print_step("Create Subject")
    payload = {"name": name, "teacher_id": teacher_id}
    res = requests.post(f"{BASE_URL}/subjects", json=payload)
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

def test_create_class(subject_id, teacher_id, schedule="Seg 08:00-10:00"):
    print_step("Create Class (teacher must own subject)")
    payload = {"subject_id": subject_id, "teacher_id": teacher_id, "schedule": schedule}
    res = requests.post(f"{BASE_URL}/classes", json=payload)
    res.raise_for_status()
    print(res.json())
    return res.json()["id"]

# -----------------------------
# LIST SUBJECTS
# -----------------------------

def test_list_subjects():
    print_step("List All Subjects")
    res = requests.get(f"{BASE_URL}/subjects")
    res.raise_for_status()
    print(res.json())
    return res.json()

def test_get_subjects_by_teacher(teacher_id, expected_subject_ids):
    print_step("Get Subjects By Teacher")

    res = requests.get(f"{BASE_URL}/teachers/{teacher_id}/subjects")
    res.raise_for_status()

    data = res.json()
    print(data)

    returned_ids = [s["id"] for s in data]

    # validação
    assert set(expected_subject_ids) == set(returned_ids), (
        f"ERRO: matérias retornadas ({returned_ids}) "
        f"≠ esperadas ({expected_subject_ids})"
    )

    print("✔ Subjects do professor retornadas corretamente.")
    return data

# -----------------------------
# CLASSES
# -----------------------------

def test_list_classes():
    print_step("List Classes")
    res = requests.get(f"{BASE_URL}/classes")
    res.raise_for_status()
    print(res.json())
    return res.json()

def test_get_classes_by_teacher(teacher_id):
    print_step("Get Classes By Teacher")
    res = requests.get(f"{BASE_URL}/teachers/{teacher_id}/classes")
    res.raise_for_status()
    print(res.json())
    return res.json()

def test_get_classes_by_subject(subject_id):
    print_step("Get Classes By Subject")
    res = requests.get(f"{BASE_URL}/subjects/{subject_id}/classes")
    res.raise_for_status()
    print(res.json())
    return res.json()

# -----------------------------
# ENROLL
# -----------------------------

def test_enroll_student(class_id, student_id):
    print_step("Enroll Student")
    res = requests.post(
        f"{BASE_URL}/classes/{class_id}/enroll",
        json={"student_id": student_id}
    )
    res.raise_for_status()
    print(res.json())

# -----------------------------
# MASTER TEST RUNNER
# -----------------------------

def run_all_tests():
    print("Aguarde… garantindo que o servidor gRPC + Flask já estão rodando.")
    time.sleep(1)

    # 1) criar teacher
    teacher_id = test_create_teacher("Prof. Ana")

    # 2) criar duas matérias
    subject_id1 = test_create_subject("Matemática", teacher_id)
    subject_id2 = test_create_subject("Geometria", teacher_id)

    # testar listagem geral
    test_list_subjects()

    # testar listagem por professor
    test_get_subjects_by_teacher(teacher_id, [subject_id1, subject_id2])

    # 3) criar aluno
    student_id = test_create_student("João")

    # 4) criar turma (da 1ª matéria)
    class_id = test_create_class(subject_id1, teacher_id)

    # 5) listagens
    test_list_classes()
    test_get_classes_by_teacher(teacher_id)
    test_get_classes_by_subject(subject_id1)

    # 6) aluno se inscreve
    test_enroll_student(class_id, student_id)

    # 7) confirmar inscrição
    test_get_classes_by_subject(subject_id1)
    test_list_classes()

    print("\n\n=== TODOS OS TESTES FINALIZADOS COM SUCESSO ===")

if __name__ == "__main__":
    run_all_tests()