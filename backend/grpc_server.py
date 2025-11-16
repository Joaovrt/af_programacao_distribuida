import grpc
from concurrent import futures
import time

from protos import school_pb2, school_pb2_grpc
from crud import (
    create_student, get_student, list_students, update_student, delete_student,
    create_teacher, get_teacher, list_teachers, update_teacher, delete_teacher,
    create_subject, get_subject, list_subjects, update_subject, delete_subject,
    create_class, get_class, list_classes, update_class, delete_class,
    get_classes_by_teacher, get_classes_by_subject,
    enroll_student_in_class
)

class SchoolServicer(school_pb2_grpc.SchoolServiceServicer):

    # Students
    def CreateStudent(self, request, context):
        s = create_student(request.name)
        return school_pb2.Student(id=s.id, name=s.name)

    def GetStudent(self, request, context):
        s = get_student(request.id)
        if not s:
            return school_pb2.Student()  # vazio
        return school_pb2.Student(id=s.id, name=s.name)

    def ListStudents(self, request, context):
        rows = list_students()
        return school_pb2.StudentList(
            students=[school_pb2.Student(id=r.id, name=r.name) for r in rows]
        )

    def UpdateStudent(self, request, context):
        s = update_student(request.id, request.name)
        if not s:
            return school_pb2.Student()
        return school_pb2.Student(id=s.id, name=s.name)

    def DeleteStudent(self, request, context):
        delete_student(request.id)
        return school_pb2.Empty()

    # Teachers
    def CreateTeacher(self, request, context):
        t = create_teacher(request.name)
        return school_pb2.Teacher(id=t.id, name=t.name)

    def GetTeacher(self, request, context):
        t = get_teacher(request.id)
        if not t:
            return school_pb2.Teacher()
        return school_pb2.Teacher(id=t.id, name=t.name)

    def ListTeachers(self, request, context):
        rows = list_teachers()
        return school_pb2.TeacherList(
            teachers=[school_pb2.Teacher(id=r.id, name=r.name) for r in rows]
        )

    def UpdateTeacher(self, request, context):
        t = update_teacher(request.id, request.name)
        if not t:
            return school_pb2.Teacher()
        return school_pb2.Teacher(id=t.id, name=t.name)

    def DeleteTeacher(self, request, context):
        delete_teacher(request.id)
        return school_pb2.Empty()

    # Subjects
    def CreateSubject(self, request, context):
        sub = create_subject(request.name)
        return school_pb2.Subject(id=sub.id, name=sub.name)

    def GetSubject(self, request, context):
        sub = get_subject(request.id)
        if not sub:
            return school_pb2.Subject()
        return school_pb2.Subject(id=sub.id, name=sub.name)

    def ListSubjects(self, request, context):
        rows = list_subjects()
        return school_pb2.SubjectList(
            subjects=[school_pb2.Subject(id=r.id, name=r.name) for r in rows]
        )

    def UpdateSubject(self, request, context):
        sub = update_subject(request.id, request.name)
        if not sub:
            return school_pb2.Subject()
        return school_pb2.Subject(id=sub.id, name=sub.name)

    def DeleteSubject(self, request, context):
        delete_subject(request.id)
        return school_pb2.Empty()

    # Classes
    def CreateClass(self, request, context):
        c = create_class(request.teacher_id, request.subject_id, request.schedule)
        return school_pb2.Class(
            id=c.id,
            teacher_id=c.teacher_id,
            subject_id=c.subject_id,
            schedule=c.schedule,
            student_ids=[s.id for s in c.students]
        )

    def GetClass(self, request, context):
        c = get_class(request.id)
        if not c:
            return school_pb2.Class()
        return school_pb2.Class(
            id=c.id,
            teacher_id=c.teacher_id,
            subject_id=c.subject_id,
            schedule=c.schedule,
            student_ids=[s.id for s in c.students]
        )

    def ListClasses(self, request, context):
        rows = list_classes()
        pb_classes = []
        for r in rows:
            pb_classes.append(
                school_pb2.Class(
                    id=r.id,
                    teacher_id=r.teacher_id,
                    subject_id=r.subject_id,
                    schedule=r.schedule,
                    student_ids=[s.id for s in r.students]
                )
            )
        return school_pb2.ClassList(classes=pb_classes)

    def UpdateClass(self, request, context):
        c = update_class(request.id, request.teacher_id, request.subject_id, request.schedule)
        if not c:
            return school_pb2.Class()
        return school_pb2.Class(
            id=c.id,
            teacher_id=c.teacher_id,
            subject_id=c.subject_id,
            schedule=c.schedule,
            student_ids=[s.id for s in c.students]
        )

    def DeleteClass(self, request, context):
        delete_class(request.id)
        return school_pb2.Empty()

    def GetClassesByTeacher(self, request, context):
        rows = get_classes_by_teacher(request.id)
        pb_classes = []
        for r in rows:
            pb_classes.append(
                school_pb2.Class(
                    id=r.id,
                    teacher_id=r.teacher_id,
                    subject_id=r.subject_id,
                    schedule=r.schedule,
                    student_ids=[s.id for s in r.students]
                )
            )
        return school_pb2.ClassList(classes=pb_classes)

    def GetClassesBySubject(self, request, context):
        rows = get_classes_by_subject(request.id)
        pb_classes = []
        for r in rows:
            pb_classes.append(
                school_pb2.Class(
                    id=r.id,
                    teacher_id=r.teacher_id,
                    subject_id=r.subject_id,
                    schedule=r.schedule,
                    student_ids=[s.id for s in r.students]
                )
            )
        return school_pb2.ClassList(classes=pb_classes)

    # Enrollment
    def EnrollStudentInClass(self, request, context):
        c = enroll_student_in_class(request.class_id, request.student_id)
        if not c:
            return school_pb2.Class()
        return school_pb2.Class(
            id=c.id,
            teacher_id=c.teacher_id,
            subject_id=c.subject_id,
            schedule=c.schedule,
            student_ids=[s.id for s in c.students]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    school_pb2_grpc.add_SchoolServiceServicer_to_server(SchoolServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('gRPC server started on 50051')
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Shutting down gRPC server...")
        server.stop(0)


if __name__ == '__main__':
    serve()