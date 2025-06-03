import mysql.connector
import pymysql

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="loki",
    database="pyconnect"
)

mycursor = mydb.cursor()
# mycursor.execute("select * from student")
# for i in mycursor:
#     print(i)
    
# Insert a record into student table
sql = "INSERT INTO student (name,college ) VALUES (%s, %s)"
val = ("John Doe","KKIT")

mycursor.execute(sql, val)

# Commit the transaction
mydb.commit()
print(mycursor.rowcount, "record inserted.")

# students = [
#     ("Alice", 20, "B"),
#     ("Bob", 19, "A"),
#     ("Charlie", 21, "C")
# ]

# mycursor.executemany(sql, students)
# mydb.commit()

print(mycursor.rowcount, "records inserted.")

# # Close connection
# mycursor.close()
# mydb.close()

mycursor.execute("select * from student")
for i in mycursor:
    print(i)

delete_sql = "DELETE FROM student WHERE name = %s"
delete_val = ("John Doe",)
mycursor.execute(delete_sql, delete_val)

mydb.commit()
print(mycursor.rowcount, "record(s) deleted.")
