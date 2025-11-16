from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class_class_student = Table(
    'class_student',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id')),
    Column('student_id', Integer, ForeignKey('students.id'))
)


class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    schedule = Column(String, nullable=True)

    teacher = relationship('Teacher')
    subject = relationship('Subject')

    # AQUI É A CORREÇÃO
    students = relationship(
        'Student',
        secondary=class_class_student,
        backref='classes',
        lazy='joined'
    )


engine = create_engine("sqlite:///school.db", echo=True)
Base.metadata.create_all(engine)