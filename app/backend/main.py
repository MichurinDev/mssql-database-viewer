import pymssql

conn = pymssql.connect(
    server='localhost:1434',
    user='sa',
    password='420506Mf',
    database='test'
)

cursor = conn.cursor()
cursor.execute('SELECT * FROM test_table')

for row in cursor:
    print(row)

conn.close()
