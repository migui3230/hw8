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
    conn.execute('''Drop table HospitalUser''')
    # save changes
    conn.commit()
    print('HospitalUser table dropped.')
except:
    print('HospitalUser table did not exist')


# create table in database
cur.execute('''CREATE TABLE HospitalUser(
UserId INTEGER PRIMARY KEY NOT NULL,
UserName TEXT NOT NULL,
UserAge TEXT NOT NULL,
UserPhNum TEXT NOT NULL,
UserHasCOVID BOOL NOT NULL,
UserSecurityLevel INTEGER NOT NULL,
LoginPassword TEXT NOT NULL);
''')

# save changes
conn.commit()
print('HospitalUser Table created.')

nm = cipher.encrypt('PDiana')
PhNum = cipher.encrypt('123-675-7645')
Password = cipher.encrypt('test123')

cur.execute('''Insert Into HospitalUser ('UserName','UserAge','UserPhNum','UserHasCOVID','UserSecurityLevel','LoginPassword') 
Values (?, 34,?,0, 1,?);''',[nm,PhNum,Password])

conn.commit()

nm = cipher.encrypt('TJones')
PhNum = cipher.encrypt('895-345-6523')
Password = cipher.encrypt('test123')

cur.execute('''Insert Into HospitalUser ('UserName','UserAge','UserPhNum','UserHasCOVID','UserSecurityLevel','LoginPassword') 
Values (?, 68,?,1, 2,?);''',[nm,PhNum,Password])

conn.commit()

nm = cipher.encrypt('AMath')
PhNum = cipher.encrypt('428-197-3967')
Password = cipher.encrypt('test123')

cur.execute('''Insert Into HospitalUser ('UserName','UserAge','UserPhNum','UserHasCOVID','UserSecurityLevel','LoginPassword') 
Values (?, 29,?,0, 3,?);''',[nm,PhNum,Password])

conn.commit()

nm = cipher.encrypt('BSmith')
PhNum = cipher.encrypt('239-567-3498')
Password = cipher.encrypt('test123')

cur.execute('''Insert Into HospitalUser ('UserName','UserAge','UserPhNum','UserHasCOVID','UserSecurityLevel','LoginPassword') 
Values (?, 37,?,1, 2,?);''',[nm,PhNum,Password])

conn.commit()

# iterate over the rows
for row in cur.execute('SELECT * FROM HospitalUser;'):
    #print(row[0],cipher.decrypt(row[1]),row[2],cipher.decrypt(row[3]),row[4],row[5],cipher.decrypt(row[6]))
    print(row[0],row[1],row[2],row[3],row[4],row[5],row[6])



# close database connection
conn.close()
print('Connection closed.')
