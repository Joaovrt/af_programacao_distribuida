from flask import Flask, jsonify, request
import grpc
import sys
import os

# garante que backend/protos esteja no path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from protos import school_pb2, school_pb2_grpc

app = Flask(__name__)

def grpc_channel():
    channel = grpc.insecure_channel("localhost:50051")
    return school_pb2_grpc.SchoolServiceStub(channel)

# STUDENTS
@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    stub = grpc_channel()
    req = school_pb2.Student(name=data["name"])
    res = stub.CreateStudent(req)
    return jsonify({"id": res.id, "name": res.name}), 201

@app.route("/students", methods=["GET"])
def list_students():
    stub = grpc_channel()
    res = stub.ListStudents(school_pb2.Empty())
    return jsonify([{"id": s.id, "name": s.name} for s in res.students])

# TEACHERS
@app.route("/teachers", methods=["POST"])
def create_teacher():
    data = request.get_json()
    stub = grpc_channel()
    req = school_pb2.Teacher(name=data["name"])
    res = stub.CreateTeacher(req)
    return jsonify({"id": res.id, "name": res.name}), 201

# SUBJECTS
@app.route("/subjects", methods=["POST"])
def create_subject():
    data = request.get_json()
    stub = grpc_channel()
    req = school_pb2.Subject(name=data["name"])
    res = stub.CreateSubject(req)
    return jsonify({"id": res.id, "name": res.name}), 201

# CLASSES
@app.route("/classes", methods=["POST"])
def create_class():
    data = request.get_json()
    stub = grpc_channel()
    req = school_pb2.Class(
        teacher_id=data["teacher_id"],
        subject_id=data["subject_id"],
        schedule=data.get("schedule", "")
    )
    res = stub.CreateClass(req)
    return jsonify({
        "id": res.id,
        "teacher_id": res.teacher_id,
        "subject_id": res.subject_id,
        "schedule": res.schedule
    }), 201

@app.route("/classes", methods=["GET"])
def list_classes():
    stub = grpc_channel()
    res = stub.ListClasses(school_pb2.Empty())
    classes = []
    for c in res.classes:
        classes.append({
            "id": c.id,
            "teacher_id": c.teacher_id,
            "subject_id": c.subject_id,
            "student_ids": list(c.student_ids),
            "schedule": c.schedule,
        })
    return jsonify(classes)

# ENROLL
@app.route("/classes/<int:class_id>/enroll", methods=["POST"])
def enroll(class_id):
    data = request.get_json()
    stub = grpc_channel()
    req = school_pb2.EnrollRequest(class_id=class_id, student_id=data["student_id"])
    res = stub.EnrollStudentInClass(req)
    return jsonify({
        "id": res.id,
        "student_ids": list(res.student_ids)
    }), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)