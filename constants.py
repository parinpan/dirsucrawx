import datetime
import MySQLdb

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class Constants:
    @staticmethod
    def get_db_new_instance():
        return MySQLdb.connect(
            "localhost",  # host
            "root",       # user
            "",           # password
            "dirsucrawx"  # db name
        )

    MIN_GEN_TO_CRAWL = 2016
    MAX_GEN_TO_CRAWL = int(datetime.datetime.now().year)
    DB_CONN = get_db_new_instance.__func__()

    GENERATION_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/prodi/'
    DEPARTMENT_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/getprodi/'
    STUDENT_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/daftarmhs/'
    PROFILE_BASE_URL = 'http://dirmahasiswa.usu.ac.id/index.php/mahasiswa/datamhs/'

    # ATTENTION
    # higher value produces deeper crawling and slower speed

    MAX_FAIL_PER_GENERATION = 15  # maximum only 999
    MAX_STUDENT_PER_GENERATION = 4  # maximum only 999
    CRAWLING_TIMEOUT_EACH_REQUEST = 15  # in seconds

    MAX_TRY_PER_TIMEOUT = 15
    DELAY_ON_TIMEOUT_TRY = 5  # in seconds

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

    STUDENT_FIELD_MAPPING = {
        'NIM': 'number',
        'NAMA': 'name',
        'FOTO': 'photo',
        'ANGKATAN': 'generation',
        'SEMTERDAFTAR': 'registered_semester',
        'STATUSAKTIF': 'active_status',
        'IPK': 'gpa',
        'EMAIL': 'email',
        'DEPKODE': 'department_code',
        'AGAMA': 'religion',
        'ALAMATMEDAN': 'medan_address',
        'ALAMATMHS': 'address',
        'ALAMATORTU': 'parent_address',
        'ALAMATTERAKHIR': 'last_address',
        'IBU': 'mom',
        'AYAH': 'dad',
        'GOLDARAH': 'blood_type',
        'IS_REGULER': 'is_regular',
        'JENJANG': 'education_level',
        'SEMESTERSKRG': 'current_semester',
        'SISASKS': 'left_sks',
        'SUMBERDANAKULIAH': 'funding_source',
        'TMPATTGLLAHIR': 'birth_info',
        'JENISKELAMIN': 'gender',
        'JUMLAHSAUDARASEKOLAH': 'siblings_total_sc',
        'NOTELPHP': 'phone'
    }

    STUDENT_FIELD_STR = ",".join(sorted(STUDENT_FIELD_MAPPING.values()))

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
