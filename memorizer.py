from constants import Constants
from accessor import Accessor
import sqlite3 as lite

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class Memorizer:
    @staticmethod
    def _query(query, data=None):
        success = True

        try:
            cur = Constants.DB_CONN.cursor()

            if data:
                success = cur.executemany(query, data).rowcount > 0

            else:
                success = cur.execute(query).rowcount > 0

        except lite.Error as e:
            success = False
            print(str(e))

        return success

    @staticmethod
    def save(conf):
        success = Memorizer.__save_faculty(conf["faculty_code"])
        success = success and Memorizer.__save_department(conf)

        message = "All students in {}/{} were{}added to the database."
        faculty_name = Constants.FACULTIES_DATA[int(conf["faculty_code"])]
        department_name = conf["department"]["prodinamaresmi"]

        if success:
            student_dicts = {}

            for gen, students_json in conf["students"].items():
                for student_json in students_json:
                    student = Accessor.get_parsed_json(student_json)

                    if student:
                        student_dicts[student["NIM"]] = student

            if not Memorizer.__save_student(
                student_dicts,
                conf["department"]["prodikode"]
            ):
                success = False

        if success:
            message = message.format(faculty_name, department_name, " ")
            Constants.DB_CONN.commit()

        else:
            message = message.format(faculty_name, department_name, " not ")
            Constants.DB_CONN.rollback()

        # tell them what I've got
        print(message)

        return success

    @staticmethod
    def __save_faculty(faculty_code):
        saved = True
        from modifier import Modifier

        data = Modifier.faculty({
            'code': int(faculty_code),
            'name': Constants.FACULTIES_DATA[faculty_code],
        })

        if data:
            query = "INSERT INTO faculty VALUES(?, ?)"
            saved = Memorizer._query(query, data)

        return saved

    @staticmethod
    def __save_department(conf):
        saved = True
        from modifier import Modifier

        data = Modifier.department({
            'code': conf["department"]["prodikode"],
            'id': conf["department_id"],
            'name': conf["department"]["prodinamaresmi"],
            'faculty_code': conf["faculty_code"]
        })

        if data:
            query = "INSERT INTO department VALUES(?, ?, ?, ?)"
            saved = Memorizer._query(query, data)

        return saved

    @staticmethod
    def __save_student(students, department_code):
        data = None
        saved = True
        from modifier import Modifier

        if students:
            data = Modifier.student(
                students,
                department_code
            )

        if data:
            query = "INSERT INTO student VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
            saved = Memorizer._query(query, data)

        return saved
