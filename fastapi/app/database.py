import psycopg
from psycopg.rows import dict_row
from .config import settings

try:
    conn = psycopg.connect(host=settings.database_hostname, dbname=settings.database_name,
                           user=settings.database_username, password=settings.database_password)
    # conn = psycopg.connect(host="localhost", dbname="pgdb", user="postg_dev", password="postgres")
    cur = conn.cursor(row_factory=dict_row)
except Exception as e:
    print("Database new serror", e)


# class DatabaseUtil:
#     # def database_execute()
#     #     with psycopg.connect(host="132.145.102.212", dbname="postgres", user="postgres", password="db") as conn:
#     #         with conn.cursor(row_factory=dict_row) as cursor:
#     def __int__(self):
#         self.conn = psycopg.connect(host="132.145.102.212", dbname="postgres", user="postgres", password="db")
#
#     def execute_query(self, sql, **kwargs):
#         with self.conn.cursor(row_factory=dict_row) as cur:
#             cur.execute(sql, **kwargs)
#             rows = cur.fetchall()
#             return rows
