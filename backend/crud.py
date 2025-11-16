from models import Student, Teacher, Subject, Class
from db import SessionLocal


def create_student(name: str):
    db = SessionLocal()
    s = Student(name=name)
    db.add(s)
    db.commit()
    db.refresh(s)
    db.close()
    return s


def list_students():
    db = SessionLocal()
    res = db.query(Student).all()
    db.close()
    return res


def create_teacher(name: str):
    db = SessionLocal()
    t = Teacher(name=name)
    db.add(t)
    db.commit()
    db.refresh(t)
    db.close()
    return t


def create_subject(name: str):
    db = SessionLocal()
    sub = Subject(name=name)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    db.close()
    return sub


def create_class(teacher_id: int, subject_id: int, schedule: str):
    db = SessionLocal()
    c = Class(teacher_id=teacher_id, subject_id=subject_id, schedule=schedule)
    db.add(c)
    db.commit()
    db.refresh(c)
    db.close()
    return c


def list_classes():
    db = SessionLocal()
    res = db.query(Class).all()
    db.close()
    return res


def get_classes_by_teacher(teacher_id: int):
    db = SessionLocal()
    res = db.query(Class).filter(Class.teacher_id == teacher_id).all()
    db.close()
    return res


def enroll_student_in_class(class_id: int, student_id: int):
    db = SessionLocal()

    c = db.get(Class, class_id)
    s = db.get(Student, student_id)

    if s not in c.students:
        c.students.append(s)
        db.commit()
        db.refresh(c)

    db.close()
    return c