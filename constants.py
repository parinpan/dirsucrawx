import datetime
import sqlite3 as lite

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class Constants:
    DB_NAME = 'database/dirsucrawx.db'
    DB_CONN = lite.connect(DB_NAME)

    MIN_GEN_TO_CRAWL = 1990
    MAX_GEN_TO_CRAWL = int(datetime.datetime.now().year)

    GENERATION_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/prodi/'
    DEPARTMENT_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/getprodi/'
    STUDENT_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/daftarmhs/'
    PROFILE_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/datamhs/'

    # ATTENTION
    # higher value produces deeper crawling and slower speed

    MAX_FAIL_PER_GENERATION = 15  # maximum only 999
    MAX_STUDENT_PER_GENERATION = 999  # maximum only 999
    CRAWLING_TIMEOUT_EACH_REQUEST = 15  # in seconds

    MAX_TRY_PER_TIMEOUT = 15
    DELAY_ON_TIMEOUT_TRY = 2  # in seconds

    FACULTIES_DATA = {
        1: "Fakultas Kedokteran",
        2: "Fakultas Hukum",
        3: "Fakultas Pertanian",
        4: "Fakultas Teknik",
        5: "Fakultas Ekonomi",
        6: "Fakultas Kedokteran Gigi",
        7: "Fakultas Ilmu Budaya",
        8: "Fakultas Matematika dan IPA",
        9: "Fakultas Ilmu-ilmu Sosial dan Politik",
        10: "Fakultas Kesehatan Masyarakat",
        11: "Fakultas Keperawatan",
        13: "Fakultas Psikologi",
        14: "Fakultas Ilmu Komputer dan Teknologi Informasi",
        15: "Fakultas Farmasi",
        21: "Sekolah Pascasarjana",
        22: "PPDS",
        23: "PPDGS",
        24: "Profesi Ners",
        25: "Apoteker"
    }

    DEFAULT_REQUEST_HEADERS = {
        'Connection': 'keep-alive',
        'Host': 'dirmahasiswa.usu.ac.id',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://dirmahasiswa.usu.ac.id/'
    }

    @staticmethod
    def get_generation_full_url(faculty, department):
        return Constants.GENERATION_BASE_URL + str(faculty) + '/' + str(department)

    @staticmethod
    def get_department_full_url(faculty):
        return Constants.DEPARTMENT_BASE_URL + str(faculty)

    @staticmethod
    def get_student_full_url(department, generation):
        return Constants.STUDENT_BASE_URL + str(department) + '/' + str(generation)

    @staticmethod
    def get_profile_full_url(identity):
        return Constants.PROFILE_BASE_URL + str(identity)

    @staticmethod
    def get_db_new_instance():
        return lite.connect(Constants.DB_NAME)
