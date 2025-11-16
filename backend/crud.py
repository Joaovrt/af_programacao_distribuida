from models import Student, Teacher, Subject, Class
from db import SessionLocal
from sqlalchemy.orm import joinedload

# ---------- Students ----------
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
    s = db.query(Student).get(student_id)
    db.close()
    return s

def list_students():
    db = SessionLocal()
    res = db.query(Student).all()
    db.close()
    return res

def update_student(student_id: int, name: str):
    db = SessionLocal()
    s = db.query(Student).get(student_id)
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
    s = db.query(Student).get(student_id)
    if not s:
        db.close()
        return False
    db.delete(s)
    db.commit()
    db.close()
    return True

# ---------- Teachers ----------
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
    t = db.query(Teacher).get(teacher_id)
    db.close()
    return t

def list_teachers():
    db = SessionLocal()
    res = db.query(Teacher).all()
    db.close()
    return res

def update_teacher(teacher_id: int, name: str):
    db = SessionLocal()
    t = db.query(Teacher).get(teacher_id)
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
    t = db.query(Teacher).get(teacher_id)
    if not t:
        db.close()
        return False
    db.delete(t)
    db.commit()
    db.close()
    return True

# ---------- Subjects ----------
def create_subject(name: str, teacher_id: int):
    db = SessionLocal()
    # validar existência do teacher
    teacher = db.query(Teacher).get(teacher_id)
    if not teacher:
        db.close()
        return None
    sub = Subject(name=name, teacher_id=teacher_id)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    db.close()
    return sub

def get_subject(subject_id: int):
    db = SessionLocal()
    sub = db.query(Subject).get(subject_id)
    db.close()
    return sub

def list_subjects():
    db = SessionLocal()
    res = db.query(Subject).options(joinedload(Subject.teacher)).all()
    db.close()
    return res

def update_subject(subject_id: int, name: str = None, teacher_id: int = None):
    db = SessionLocal()
    sub = db.query(Subject).get(subject_id)
    if not sub:
        db.close()
        return None
    if name is not None:
        sub.name = name
    if teacher_id is not None:
        # validar teacher existe
        teacher = db.query(Teacher).get(teacher_id)
        if not teacher:
            db.close()
            return None
        sub.teacher_id = teacher_id
    db.add(sub)
    db.commit()
    db.refresh(sub)
    db.close()
    return sub

def delete_subject(subject_id: int):
    db = SessionLocal()
    sub = db.query(Subject).get(subject_id)
    if not sub:
        db.close()
        return False
    db.delete(sub)
    db.commit()
    db.close()
    return True

# ---------- Classes ----------
def create_class(subject_id: int, schedule: str, teacher_id: int = None):
    """
    teacher_id: usado para autorizar que o professor que está criando a turma é o dono da matéria.
    """
    db = SessionLocal()
    sub = db.query(Subject).get(subject_id)
    if not sub:
        db.close()
        return None  # subject não existe
    if teacher_id is not None and sub.teacher_id != teacher_id:
        db.close()
        return None  # não autorizado
    c = Class(subject_id=subject_id, schedule=schedule)
    db.add(c)
    db.commit()
    db.refresh(c)
    db.close()
    return c

def get_class(class_id: int):
    db = SessionLocal()
    c = db.query(Class).options(joinedload(Class.subject), joinedload(Class.students)).get(class_id)
    db.close()
    return c

def list_classes():
    db = SessionLocal()
    res = db.query(Class).options(joinedload(Class.subject), joinedload(Class.students)).all()
    db.close()
    return res

def update_class(class_id: int, subject_id: int = None, schedule: str = None):
    db = SessionLocal()
    c = db.query(Class).get(class_id)
    if not c:
        db.close()
        return None
    if subject_id is not None:
        sub = db.query(Subject).get(subject_id)
        if not sub:
            db.close()
            return None
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
    c = db.query(Class).get(class_id)
    if not c:
        db.close()
        return False
    db.delete(c)
    db.commit()
    db.close()
    return True

def get_classes_by_teacher(teacher_id: int):
    db = SessionLocal()
    # todas as classes cujas subjects têm teacher_id == teacher_id
    res = db.query(Class).join(Subject).filter(Subject.teacher_id == teacher_id).options(joinedload(Class.subject), joinedload(Class.students)).all()
    db.close()
    return res

def get_classes_by_subject(subject_id: int):
    db = SessionLocal()
    res = db.query(Class).filter(Class.subject_id == subject_id).options(joinedload(Class.subject), joinedload(Class.students)).all()
    db.close()
    return res

# ---------- Enrollment ----------
def enroll_student_in_class(class_id: int, student_id: int):
    db = SessionLocal()
    c = db.query(Class).get(class_id)
    s = db.query(Student).get(student_id)
    if c is None or s is None:
        db.close()
        return None
    if s not in c.students:
        c.students.append(s)
        db.commit()
        db.refresh(c)
    db.close()
    return c