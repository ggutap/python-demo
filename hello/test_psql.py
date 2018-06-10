import psycopg2

conn = psycopg2.connect(database='jdasta',user='postgres',password='twtimes2018',host='106.15.202.31',port='5432')
cur = conn.cursor()
cur.execute("select * from sys_users")
rows = cur.fetchall()
print(rows)
for item in rows :
    print(item)

conn.commit()
cur.close()
conn.close()

