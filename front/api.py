from flask import Flask, jsonify, request, abort
import grpc
import sys
import os

# garante que backend/protos esteja no path (ajuste se necessário)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from protos import school_pb2, school_pb2_grpc

app = Flask(__name__)

def grpc_channel():
    channel = grpc.insecure_channel("localhost:50051")
    return school_pb2_grpc.SchoolServiceStub(channel)

# ---------- STUDENTS ----------
@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    if not data or "name" not in data:
        abort(400)
    stub = grpc_channel()
    req = school_pb2.Student(name=data["name"])
    res = stub.CreateStudent(req)
    return jsonify({"id": res.id, "name": res.name}), 201

@app.route("/students", methods=["GET"])
def list_students():
    stub = grpc_channel()
    res = stub.ListStudents(school_pb2.Empty())
    return jsonify([{"id": s.id, "name": s.name} for s in res.students])

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    stub = grpc_channel()
    res = stub.GetStudent(school_pb2.Id(id=student_id))
    return jsonify({"id": res.id, "name": res.name})

# ---------- TEACHERS ----------
@app.route("/teachers", methods=["POST"])
def create_teacher():
    data = request.get_json()
    if not data or "name" not in data:
        abort(400)
    stub = grpc_channel()
    req = school_pb2.Teacher(name=data["name"])
    res = stub.CreateTeacher(req)
    return jsonify({"id": res.id, "name": res.name}), 201

@app.route("/teachers", methods=["GET"])
def list_teachers():
    stub = grpc_channel()
    res = stub.ListTeachers(school_pb2.Empty())
    return jsonify([{"id": t.id, "name": t.name} for t in res.teachers])

# ---------- SUBJECTS ----------
@app.route("/subjects", methods=["POST"])
def create_subject():
    data = request.get_json()
    if not data or "name" not in data or "teacher_id" not in data:
        abort(400, "name and teacher_id required")
    stub = grpc_channel()
    req = school_pb2.Subject(name=data["name"], teacher_id=data["teacher_id"])
    try:
        res = stub.CreateSubject(req)
    except grpc.RpcError as e:
        abort(400, e.details())
    return jsonify({"id": res.id, "name": res.name, "teacher_id": res.teacher_id}), 201

@app.route("/subjects", methods=["GET"])
def list_subjects():
    stub = grpc_channel()
    res = stub.ListSubjects(school_pb2.Empty())
    return jsonify([{"id": s.id, "name": s.name, "teacher_id": s.teacher_id} for s in res.subjects])

# ---------- CLASSES ----------
@app.route("/classes", methods=["POST"])
def create_class():
    """
    Para criar uma turma, o professor que está criando deve enviar teacher_id para autorização.
    Body: { "subject_id": int, "schedule": str, "teacher_id": int }
    """
    data = request.get_json()
    if not data or "subject_id" not in data or "teacher_id" not in data:
        abort(400, "subject_id and teacher_id required")
    stub = grpc_channel()
    req = school_pb2.CreateClassRequest(subject_id=data["subject_id"], schedule=data.get("schedule", ""), teacher_id=data["teacher_id"])
    try:
        res = stub.CreateClass(req)
    except grpc.RpcError as e:
        abort(400, e.details())
    return jsonify({
        "id": res.id,
        "subject_id": res.subject_id,
        "schedule": res.schedule,
        "student_ids": list(res.student_ids)
    }), 201

@app.route("/classes", methods=["GET"])
def list_classes():
    stub = grpc_channel()
    res = stub.ListClasses(school_pb2.Empty())
    classes = []
    for c in res.classes:
        classes.append({
            "id": c.id,
            "subject_id": c.subject_id,
            "student_ids": list(c.student_ids),
            "schedule": c.schedule,
        })
    return jsonify(classes)

@app.route("/classes/<int:class_id>", methods=["GET"])
def get_class(class_id):
    stub = grpc_channel()
    res = stub.GetClass(school_pb2.Id(id=class_id))
    return jsonify({
        "id": res.id,
        "subject_id": res.subject_id,
        "student_ids": list(res.student_ids),
        "schedule": res.schedule,
    })

# professor vê turmas das suas matérias
@app.route("/teachers/<int:teacher_id>/classes", methods=["GET"])
def get_classes_by_teacher_route(teacher_id):
    stub = grpc_channel()
    res = stub.GetClassesByTeacher(school_pb2.Teacher(id=teacher_id))
    classes = []
    for c in res.classes:
        classes.append({
            "id": c.id,
            "subject_id": c.subject_id,
            "student_ids": list(c.student_ids),
            "schedule": c.schedule,
        })
    return jsonify(classes)

# listar turmas por matéria
@app.route("/subjects/<int:subject_id>/classes", methods=["GET"])
def get_classes_by_subject_route(subject_id):
    stub = grpc_channel()
    res = stub.GetClassesBySubject(school_pb2.Subject(id=subject_id))
    classes = []
    for c in res.classes:
        classes.append({
            "id": c.id,
            "subject_id": c.subject_id,
            "student_ids": list(c.student_ids),
            "schedule": c.schedule,
        })
    return jsonify(classes)

# aluno se inscreve em turma
@app.route("/classes/<int:class_id>/enroll", methods=["POST"])
def enroll(class_id):
    data = request.get_json()
    if not data or "student_id" not in data:
        abort(400, "student_id required")
    stub = grpc_channel()
    req = school_pb2.EnrollRequest(class_id=class_id, student_id=data["student_id"])
    try:
        res = stub.EnrollStudentInClass(req)
    except grpc.RpcError as e:
        abort(400, e.details())
    return jsonify({
        "id": res.id,
        "student_ids": list(res.student_ids)
    }), 200

@app.route("/teachers/<int:teacher_id>/subjects", methods=["GET"])
def get_subjects_by_teacher(teacher_id):
    stub = grpc_channel()
    req = school_pb2.Id(id=teacher_id)
    res = stub.GetSubjectsByTeacher(req)

    subjects = [{"id": s.id, "name": s.name, "teacher_id": s.teacher_id} for s in res.subjects]
    return jsonify(subjects), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)