from models import Student, Teacher, Subject, Class
from db import SessionLocal

# --- Students ---
def create_student(name: str):
    db = SessionLocal()
    s = Student(name=name)
    db.add(s)
    db.commit()
    db.refresh(s)
    db.close()
    return s

def get_student(student_id: int):
    db = SessionLocal()
    s = db.get(Student, student_id)
    db.close()
    return s

def list_students():
    db = SessionLocal()
    res = db.query(Student).all()
    db.close()
    return res

def update_student(student_id: int, name: str):
    db = SessionLocal()
    s = db.get(Student, student_id)
    if not s:
        db.close()
        return None
    s.name = name
    db.add(s)
    db.commit()
    db.refresh(s)
    db.close()
    return s

def delete_student(student_id: int):
    db = SessionLocal()
    s = db.get(Student, student_id)
    if not s:
        db.close()
        return False
    db.delete(s)
    db.commit()
    db.close()
    return True

# --- Teachers ---
def create_teacher(name: str):
    db = SessionLocal()
    t = Teacher(name=name)
    db.add(t)
    db.commit()
    db.refresh(t)
    db.close()
    return t

def get_teacher(teacher_id: int):
    db = SessionLocal()
    t = db.get(Teacher, teacher_id)
    db.close()
    return t

def list_teachers():
    db = SessionLocal()
    res = db.query(Teacher).all()
    db.close()
    return res

def update_teacher(teacher_id: int, name: str):
    db = SessionLocal()
    t = db.get(Teacher, teacher_id)
    if not t:
        db.close()
        return None
    t.name = name
    db.add(t)
    db.commit()
    db.refresh(t)
    db.close()
    return t

def delete_teacher(teacher_id: int):
    db = SessionLocal()
    t = db.get(Teacher, teacher_id)
    if not t:
        db.close()
        return False
    db.delete(t)
    db.commit()
    db.close()
    return True

# --- Subjects ---
def create_subject(name: str):
    db = SessionLocal()
    sub = Subject(name=name)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    db.close()
    return sub

def get_subject(subject_id: int):
    db = SessionLocal()
    sub = db.get(Subject, subject_id)
    db.close()
    return sub

def list_subjects():
    db = SessionLocal()
    res = db.query(Subject).all()
    db.close()
    return res

def update_subject(subject_id: int, name: str):
    db = SessionLocal()
    sub = db.get(Subject, subject_id)
    if not sub:
        db.close()
        return None
    sub.name = name
    db.add(sub)
    db.commit()
    db.refresh(sub)
    db.close()
    return sub

def delete_subject(subject_id: int):
    db = SessionLocal()
    sub = db.get(Subject, subject_id)
    if not sub:
        db.close()
        return False
    db.delete(sub)
    db.commit()
    db.close()
    return True

# --- Classes ---
def create_class(teacher_id: int, subject_id: int, schedule: str):
    db = SessionLocal()
    c = Class(teacher_id=teacher_id, subject_id=subject_id, schedule=schedule)
    db.add(c)
    db.commit()
    db.refresh(c)
    db.close()
    return c

def get_class(class_id: int):
    db = SessionLocal()
    c = db.get(Class, class_id)
    db.close()
    return c

def list_classes():
    db = SessionLocal()
    res = db.query(Class).all()
    db.close()
    return res

def update_class(class_id: int, teacher_id: int = None, subject_id: int = None, schedule: str = None):
    db = SessionLocal()
    c = db.get(Class, class_id)
    if not c:
        db.close()
        return None
    if teacher_id is not None:
        c.teacher_id = teacher_id
    if subject_id is not None:
        c.subject_id = subject_id
    if schedule is not None:
        c.schedule = schedule
    db.add(c)
    db.commit()
    db.refresh(c)
    db.close()
    return c

def delete_class(class_id: int):
    db = SessionLocal()
    c = db.get(Class, class_id)
    if not c:
        db.close()
        return False
    db.delete(c)
    db.commit()
    db.close()
    return True

def get_classes_by_teacher(teacher_id: int):
    db = SessionLocal()
    res = db.query(Class).filter(Class.teacher_id == teacher_id).all()
    db.close()
    return res

def get_classes_by_subject(subject_id: int):
    db = SessionLocal()
    res = db.query(Class).filter(Class.subject_id == subject_id).all()
    db.close()
    return res

# --- Enrollment ---
def enroll_student_in_class(class_id: int, student_id: int):
    db = SessionLocal()
    c = db.get(Class, class_id)
    s = db.get(Student, student_id)
    if c is None or s is None:
        db.close()
        return None
    # evita duplicata
    if s not in c.students:
        c.students.append(s)
        db.commit()
        db.refresh(c)
    db.close()
    return c