import threading

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class CrawxThread(threading.Thread):
    def __init__(self, func, params):
        threading.Thread.__init__(self)
        self.__func = func
        self.__params = params

    def run(self):
        return self.__func(self.__params)