import time
from .accessor import Accessor
from constants import Constants
from database.memorizer import Memorizer

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class Collector:
    def __init__(self):
        self.__shy_student = {}
        self.__traveled_student = {}

        self._accessor = Accessor()
        self.__crawx_threads = []

    def __convince_students_list(self, conf):
        if not conf["students"]:
            return

        new_accessor = Accessor(
            self._accessor.cookies,
            self._accessor.key_to_open
        )

        convinced = False
        success = True

        faculty_code = "%02d" % int(conf["faculty_code"])
        department_code = conf["department"]["prodikode"]

        for student in conf["students"]:
            min_gen = Constants.MIN_GEN_TO_CRAWL
            max_gen = Constants.MAX_GEN_TO_CRAWL

            max_fail = Constants.MAX_FAIL_PER_GENERATION
            max_student = Constants.MAX_STUDENT_PER_GENERATION

            department_id = str(student["NIM"])[4:6]
            conf.update({'department_id': department_id})

            for gen in range(max_gen, min_gen - 1, -1):
                fail_counter = 0
                gen_id = str(gen)[2:4]

                for order in range(1, max_student + 1):
                    student_id = (gen_id + faculty_code + department_id + "%03d") % order

                    if student_id not in self.__traveled_student:
                        self.__traveled_student[student_id] = True
                        print("Trying to guess: " + student_id + " and... ", end='')

                        json_profile = Accessor.get_parsed_json(
                            new_accessor.show_profile_of(student_id)
                        )

                        if json_profile:
                            if department_code not in self.__shy_student:
                                self.__shy_student[department_code] = {}

                            if gen not in self.__shy_student[department_code]:
                                self.__shy_student[department_code][gen] = []

                            self.__shy_student[department_code][gen].append(
                                json_profile
                            )

                            convinced = True
                            fail_counter = 0
                            print("success!")

                        else:
                            fail_counter += 1
                            print("doesn't exist!")

                    if fail_counter == max_fail:
                        break

            break  # i just need one data from the list

        if convinced:
            conf.update({'students': self.__shy_student[department_code]})
            del self.__shy_student[department_code]
            saved = Memorizer.save(conf)

            # to give flag that saving process has ever been failed
            if not saved and success:
                success = False

        return success

    def run(self):
        saving_info = {}

        # collect all departments by simulating 'the scenario'
        for faculty_code, faculty_name in Constants.FACULTIES_DATA.items():
            saving_info[faculty_code] = {}

            departments = Accessor.get_parsed_json(
                self._accessor.show_departments_of(
                    faculty_code
                )
            )

            if departments:
                print("All departments in: " + faculty_name + " are successfully found.")

                # collect all identity configuration
                for department in departments:
                    saving_info[faculty_code][department["prodikode"]] = True

                    # ups, brute force detected, apologize me
                    max_gen = Constants.MAX_GEN_TO_CRAWL
                    min_gen = Constants.MIN_GEN_TO_CRAWL - 1

                    for generation in range(max_gen, min_gen, -1):
                        gen_res = Accessor.get_parsed_json(
                            self._accessor.show_generations_of(
                                faculty_code,
                                department["prodikode"]
                            )
                        )

                        if gen_res:
                            saved = self.__convince_students_list({
                                'students': Accessor.get_parsed_json(
                                    self._accessor.show_students_of(
                                        department["prodikode"],
                                        generation
                                    )
                                ) if not False else [],
                                'department': department,
                                'faculty_code': faculty_code
                            })

                            saving_info[faculty_code][department["prodikode"]] = saved
                            break

                self._accessor.open_session(True)
                time.sleep(2)  # to prevent of considering me as a bot

        return saving_info

    def __del__(self):
        # thank you for your hard work
        Constants.DB_CONN.close()
