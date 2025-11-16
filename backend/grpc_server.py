import grpc
from concurrent import futures
import time

from protos import school_pb2, school_pb2_grpc
from crud import (
    create_student, list_students, create_teacher, create_subject,
    create_class, list_classes, get_classes_by_teacher, enroll_student_in_class
)

class SchoolServicer(school_pb2_grpc.SchoolServiceServicer):

    # Students
    def CreateStudent(self, request, context):
        s = create_student(request.name)
        return school_pb2.Student(id=s.id, name=s.name)

    def GetStudent(self, request, context):
        # optional: implement if needed (using crud + DB)
        # here we'll try to list and find - but better implement in crud
        return school_pb2.Student(id=0, name="")  # placeholder

    def ListStudents(self, request, context):
        rows = list_students()
        return school_pb2.StudentList(
            students=[school_pb2.Student(id=r.id, name=r.name) for r in rows]
        )

    def DeleteStudent(self, request, context):
        # optional: implement delete in crud and call here
        return school_pb2.Empty()

    # Teachers
    def CreateTeacher(self, request, context):
        t = create_teacher(request.name)
        return school_pb2.Teacher(id=t.id, name=t.name)

    def ListTeachers(self, request, context):
        # optional: if you implemented list_teachers in crud
        return school_pb2.TeacherList()

    # Subjects
    def CreateSubject(self, request, context):
        sub = create_subject(request.name)
        return school_pb2.Subject(id=sub.id, name=sub.name)

    def ListSubjects(self, request, context):
        # optional: implement if you made list_subjects
        return school_pb2.SubjectList()

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

    def GetClassesByTeacher(self, request, context):
        # request is a Teacher message (has id)
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

    def EnrollStudentInClass(self, request, context):
        # request is EnrollRequest (class_id, student_id)
        c = enroll_student_in_class(request.class_id, request.student_id)
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