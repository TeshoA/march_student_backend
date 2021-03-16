import pymysql

host='127.0.0.1'
port=3306
user='root'
password='Pa55w.rd'
database='blog_flask'
conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database)

cursor = conn.cursor()

sql = "SELECT * FROM post"
cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    post_id = row[0]
    author_id = row[1]
    created = row[2]
    title = row[3]
    content = row[4]
    print(post_id, " ", title, " ", content)


cursor.close()
conn.close()
