import socketserver
import hmac
import hashlib
import sqlite3 as sql
import Encryption



key = b'\x89\xcc\x01y\xfd\xbd\xcd=Gv\x99m\xa5\x9f?f\x02\x86\xc9#\xea\xf7\xc3e\xd6\xa0\t\x06D\xad<\x84'
iv = b'w\xdb^K%\\\xf5,`\xc7\xbb\xabs\x1f\x06\x16'
cipher = Encryption.AESCipher(key, iv)


# encryption server class 
HOST, PORT = "localhost", 8888

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive the data from the client
        self.data = self.request.recv(1024).strip()

        # Split the received data into encrypted message and HMAC signature
        encrypted_message = self.data[:-64]  # Assuming SHA-512 HMAC is used, which is 64 bytes long
        received_hmac = self.data[-64:]

        # Compute the HMAC of the received encrypted message
        computed_hmac = hmac.new(key, encrypted_message, hashlib.sha512).digest()

        # Authenticate the message
        if computed_hmac == received_hmac:
            decrypted_message = cipher.decrypt(encrypted_message)


            TestResultId, TestResult = decrypted_message.split("|SEP|")

            # Validate the data
            if not TestResultId or not TestResultId.isdigit() or int(TestResultId) <= 0:
                print("Invalid TestResultId received.")
                return

            if not TestResult or TestResult.strip() == "":
                print("Invalid TestResult received.")
                return

            # Update the UserTestResults database table
            try:
                with sql.connect("HospitalUsers.db") as con:
                    cur = con.cursor()
                    cur.execute("UPDATE UserTestResults SET TestResult=? WHERE TestResultId=?", (TestResult, TestResultId))
                    con.commit()
            except:
                print("Error updating the UserTestResults table.")
        else:
            print("Unauthenticated Test Result Update received! Be on alert! Watch out for bad guys!!!")

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
