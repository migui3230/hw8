import sqlite3
import Encryption
import base64

key = b'\x89\xcc\x01y\xfd\xbd\xcd=Gv\x99m\xa5\x9f?f\x02\x86\xc9#\xea\xf7\xc3e\xd6\xa0\t\x06D\xad<\x84'
iv = b'w\xdb^K%\\\xf5,`\xc7\xbb\xabs\x1f\x06\x16'
cipher = Encryption.AESCipher(key, iv)

# Connect to db
conn = sqlite3.connect('HospitalUsers.db')

# create Cursor to execute queries
cur = conn.cursor()

# fetch records from the UserTestResults table
cur.execute('SELECT * FROM UserTestResults;')
rows = cur.fetchall()

print("TestResultId | UserId | TestName    | TestResult")
print("-----------------------------------------------")

# decrypt and display the records
for row in rows:
    encrypted_test_name_bytes = base64.b64decode(row[2])
    encrypted_test_result_bytes = base64.b64decode(row[3])

    decrypted_test_name = cipher.decrypt(encrypted_test_name_bytes).decode('utf-8').strip()
    decrypted_test_result = cipher.decrypt(encrypted_test_result_bytes).decode('utf-8').strip()

    print(f"{row[0]}          | {row[1]}    | {decrypted_test_name} | {decrypted_test_result}")

# close database connection
conn.close()
