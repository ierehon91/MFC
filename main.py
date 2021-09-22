import psycopg2

conn = psycopg2.connect(dbname='MFC', user='postgres',
                        password='qwe123!@', host='localhost')

cursor = conn.cursor()
cursor.execute("SELECT version()")
version = cursor.fetchall()
print(version)
