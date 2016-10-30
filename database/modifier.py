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

        if int(dicts["code"]) in Modifier.LOADED_FACULTIES:
            query = "UPDATE faculty SET name = '{}' "
            query += "WHERE code = " + str(dicts["code"])
            Memorizer._query(query.format(dicts["name"]))

        else:
            data_to_insert = [(dicts["code"], dicts["name"])]

        return data_to_insert

    @staticmethod
    def department(dicts):
        data_to_insert = []

        if int(dicts["code"]) in Modifier.LOADED_DEPARTMENTS:
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

        for number, student in dicts.items():
            existed_number = int(number) in Modifier.LOADED_STUDENTS

            if existed_number:
                query = "UPDATE student SET name = '{}', generation = '{}', photo = '{}', "
                query += "registered_semester = '{}', active_status = '{}', gpa = '{}',  "
                query += "email = '{}', department_code = '{}' WHERE number = " + str(number)

                Modifier._query(
                    query.format(
                        student["NAMA"], student["ANGKATAN"],
                        student["FOTO"], student["SEMTERDAFTAR"],
                        student["STATUSAKTIF"], student["IPK"],
                        student["EMAIL"], department_code
                    )
                )

            if not existed_number:
                data_to_insert.append((
                    student["NIM"], student["NAMA"],
                    student["ANGKATAN"], student["FOTO"],
                    student["SEMTERDAFTAR"], student["STATUSAKTIF"],
                    student["IPK"], student["EMAIL"], department_code
                ))

        return data_to_insert
