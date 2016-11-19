from .memorizer import Memorizer
from database.dataloader import DataLoader

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class Modifier(Memorizer):
    LOADED_STUDENTS = DataLoader.preload("student")
    LOADED_FACULTIES = DataLoader.preload("faculty")
    LOADED_DEPARTMENTS = DataLoader.preload("department")

    @staticmethod
    def faculty(dicts):
        data_to_insert = []

        if str(dicts["code"]) in Modifier.LOADED_FACULTIES:
            query = "UPDATE faculty SET name = '{}' "
            query += "WHERE code = " + str(dicts["code"])
            Memorizer._query(query.format(dicts["name"]))

        else:
            data_to_insert = [(dicts["code"], dicts["name"])]

        return data_to_insert

    @staticmethod
    def department(dicts):
        data_to_insert = []

        if str(dicts["code"]) in Modifier.LOADED_DEPARTMENTS:
            query = "UPDATE department SET name = '{}', "
            query += "faculty_code = '{}' WHERE code = " + str(dicts["code"])

            Memorizer._query(
                query.format(
                    dicts["name"],
                    dicts["faculty_code"],
                )
            )

        else:
            data_to_insert = [(
                dicts["code"], dicts["id"],
                dicts["name"], dicts["faculty_code"]
            )]

        return data_to_insert

    @staticmethod
    def student(dicts, department_code):
        data_to_insert = []
        from constants import Constants

        for number, student in dicts.items():
            temp_query = ""
            future_insert = []
            existed_number = number in Modifier.LOADED_STUDENTS

            for key, db_key in sorted(Constants.STUDENT_FIELD_MAPPING.items(), key=lambda x: x[1]):
                key = key.upper()

                if key not in student:
                    student[key] = ""

                if key in ["IPK", "SEMESTERSKRG", "SISASKS", "JUMLAHSAUDARASEKOLAH"] \
                        and (student[key] is None or key not in student):
                    student[key] = 0

                if key == "DEPKODE":
                    student[key] = department_code

                future_insert.append(student[key])
                temp_query += db_key + " = '{}',"

            if existed_number:
                query = "UPDATE student SET [statement] WHERE number = " + str(number)
                query = query.replace('[statement]', temp_query.rstrip(','))
                Modifier._query(query.format(*future_insert))

            if not existed_number:
                data_to_insert.append(tuple(future_insert))

        return data_to_insert
