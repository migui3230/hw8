import sqlite3
import Encryption

key = b'\x89\xcc\x01y\xfd\xbd\xcd=Gv\x99m\xa5\x9f?f\x02\x86\xc9#\xea\xf7\xc3e\xd6\xa0\t\x06D\xad<\x84'
iv = b'w\xdb^K%\\\xf5,`\xc7\xbb\xabs\x1f\x06\x16'
cipher = Encryption.AESCipher(key,iv)

#create new db
conn = sqlite3.connect('HospitalUsers.db')

# create Cursor to execute queries
cur = conn.cursor()


# drop table from database
try:
    conn.execute('''Drop table UserTestResults ''')
    # save changes
    conn.commit()
    print('UserTestResults  table dropped.')
except:
    print('UserTestResults  table did not exist')


# create table in database
cur.execute('''CREATE TABLE UserTestResults (
TestResultId INTEGER PRIMARY KEY NOT NULL,
UserId INTEGER NOT NULL,
TestName TEXT NOT NULL,
TestResult REAL NOT NULL
);
''')

# save changes
conn.commit()
print('UserTestResults Table created.')

nm = cipher.encrypt('Chicken Pox')
testResult = cipher.encrypt('negative')
cur.execute('''Insert Into UserTestResults ('UserId','TestName','TestResult')
 Values (1, ?,?);''',[nm,testResult])

conn.commit()

nm = cipher.encrypt('Chicken Pox')
testResult = cipher.encrypt('positive')
cur.execute('''Insert Into UserTestResults ('UserId','TestName','TestResult')
 Values (2, ?,?);''',[nm,testResult])

conn.commit()

nm = cipher.encrypt('Flu')
testResult = cipher.encrypt('undetermined')
cur.execute('''Insert Into UserTestResults ('UserId','TestName','TestResult')
 Values (3, ?,?);''',[nm,testResult])

conn.commit()

nm = cipher.encrypt('Flu')
testResult = cipher.encrypt('positive')
cur.execute('''Insert Into UserTestResults ('UserId','TestName','TestResult')
 Values (4, ?,?);''',[nm,testResult])

conn.commit()

nm = cipher.encrypt('Flu')
testResult = cipher.encrypt('negative')
cur.execute('''Insert Into UserTestResults ('UserId','TestName','TestResult')
 Values (1, ?,?);''',[nm,testResult])

conn.commit()

# iterate over the rows
for row in cur.execute('SELECT * FROM UserTestResults;'):
    print(row[0],row[1],row[2])



# close database connection
conn.close()
print('Connection closed.')
