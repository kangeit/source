import psycopg
from psycopg.rows import dict_row
from .config import settings

# try:
#     conn = psycopg.connect(host=settings.database_hostname, dbname=settings.database_name,
#                            user=settings.database_username, password=settings.database_password)
#     # conn = psycopg.connect(host="localhost", dbname="pgdb", user="postg_dev", password="postgres")
#     cur = conn.cursor(row_factory=dict_row)
# except Exception as e:
#     print("Database error", e)


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

def execute_sql_query(query, *params):
    try:
        connection = psycopg.connect(
            host=settings.database_hostname, 
            dbname=settings.database_name,
            user=settings.database_username, 
            password=settings.database_password
        )

        cursor = connection.cursor(row_factory=dict_row)
        cursor.execute(query, params)
        result = cursor.fetchall()        
        if not query.lower().startswith("select"):
            connection.commit()
        return result

    except (Exception, psycopg.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()