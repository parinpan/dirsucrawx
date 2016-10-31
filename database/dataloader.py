import MySQLdb
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
            cur = Constants.DB_CONN.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            data = cur.fetchone() if my_type == "one" else cur.fetchall()

        except MySQLdb.Error as e:
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

        return indexed_data
