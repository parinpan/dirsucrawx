import time
import requests
import simplejson as json
from constants import Constants

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class Accessor:
    def __init__(self, cookies=None, key_to_open=None):
        self.cookies = cookies
        self.key_to_open = key_to_open
        self.requester = requests.Session()

        if cookies is None and key_to_open is None:
            self.open_session()

    # additional but really important (hmm not really additional)
    def __add_additional_query(self, url):
        url = url + "?_=" + str(self.key_to_open)
        self.key_to_open += 1
        return url

    def open_session(self, renew_session=False):
        if renew_session:
            self.cookies = {}

        self.key_to_open = Accessor.__get_micro_time_key()
        self.requester = requests.Session()

    # this is the magic that I figured out
    @staticmethod
    def __get_micro_time_key():
        key = '{:.10f}'.format(float(time.time() * 1000))
        return int(key[0:13])

    @staticmethod
    def get_parsed_json(output):
        parsed = True

        if hasattr(output, "text"):
            try:
                output = json.loads(output.text)

            except json.JSONDecodeError:
                parsed = False

        return output if output and parsed and "error" not in output else False

    def __get_response_of(self, url):
        output = False
        max_try_on_fail = Constants.MAX_TRY_PER_TIMEOUT

        while max_try_on_fail:
            try:
                output = self.requester.get(
                    self.__add_additional_query(url),
                    headers=Constants.DEFAULT_REQUEST_HEADERS,
                    cookies=self.cookies,
                    timeout=Constants.CRAWLING_TIMEOUT_EACH_REQUEST
                )

                self.cookies = output.cookies.get_dict()
                break

            except requests.exceptions.Timeout as e:
                print(str(e))
                max_try_on_fail -= 1
                time.sleep(Constants.DELAY_ON_TIMEOUT_TRY)

            except requests.exceptions.TooManyRedirects as e:
                print(str(e))

            except requests.exceptions.RequestException as e:
                print(str(e))

        return output

    def show_departments_of(self, faculty):
        return self.__get_response_of(
            Constants.get_department_full_url(faculty)
        )

    def show_generations_of(self, faculty, department):
        return self.__get_response_of(
            Constants.get_generation_full_url(faculty, department)
        )

    def show_students_of(self, department, generation):
        return self.__get_response_of(
            Constants.get_student_full_url(department, generation)
        )

    def show_profile_of(self, identity):
        return self.__get_response_of(
            Constants.get_profile_full_url(identity)
        )
