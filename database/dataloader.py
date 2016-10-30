import sqlite3 as lite
from constants import Constants

"""

Written by  : M. Fachrin Aulia Nasution
Web Page    : http://samper.in || http://fachr.in
Email       : fachrinfan@gmail.com

"""


class DataLoader:
    @staticmethod
    def __fetch(query, my_type):
        data = None

        try:
            Constants.DB_CONN.row_factory = lite.Row
            cur = Constants.DB_CONN.cursor()
            cur.execute(query)
            data = cur.fetchone() if my_type == "one" else cur.fetchall()

        except lite.Error as e:
            print(str(e))

        return data

    @staticmethod
    def preload(my_type):
        col = "number"
        indexed_data = {}

        if my_type == "faculty" or my_type == "department":
            col = "code"

        query = "SELECT " + col + " FROM " + my_type
        all_data = DataLoader.__fetch(query, "all")

        # rearrange to indexing the data
        for data in all_data:
            indexed_data[data[col]] = 1

        return indexed_data if indexed_data else None
