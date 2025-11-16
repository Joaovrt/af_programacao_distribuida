from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

# associações many-to-many entre classes (turmas) e students
class_student = Table(
    'class_student',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id'), primary_key=True),
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True)
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # relacionamento opcional: subjects
    subjects = relationship("Subject", back_populates="teacher", lazy="joined")


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)

    teacher = relationship("Teacher", back_populates="subjects")
    # uma matéria terá várias turmas
    classes = relationship("Class", back_populates="subject", lazy="joined")


class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    schedule = Column(String, nullable=True)

    subject = relationship("Subject", back_populates="classes")
    students = relationship('Student', secondary=class_student, backref='classes', lazy='joined')

engine = create_engine("sqlite:///school.db", echo=True)
Base.metadata.create_all(engine)