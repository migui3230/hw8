import	socketserver
import sqlite3 as sql
import Encryption

key = b'\x89\xcc\x01y\xfd\xbd\xcd=Gv\x99m\xa5\x9f?f\x02\x86\xc9#\xea\xf7\xc3e\xd6\xa0\t\x06D\xad<\x84'
iv = b'w\xdb^K%\\\xf5,`\xc7\xbb\xabs\x1f\x06\x16'
cipher = Encryption.AESCipher(key,iv)

class	MyTCPHandler(socketserver.BaseRequestHandler):
    def	handle(self):
        #	self.request	is	the	TCP	socket	connected	to	the	client
        self.data	=	self.request.recv(1024).strip()
        #print(self.data)
        print("{}	sent message:	".format(self.client_address[0]))
        self.data = cipher.decrypt(self.data)
        print(self.data)
        sep = "^%$"
        userId = self.data.partition(sep)[0]
        print(userId)
        rest = self.data.partition(sep)[2]

        testName = rest.partition(sep)[0]
        testResult = rest.partition(sep)[2]

        try:
            error = False
            testName = str(testName).lstrip()
            testResult = str(testResult).lstrip()
            msg = "\n"
            if (len(testName) == 0):
                error = True
                msg += "You can not enter in an empty test name \n"
            if (len(testResult) == 0):
                error = True
                msg += "You can not enter in an empty test Result \n"
            try:
                if (int(userId) <= 0):
                    error = True
                    msg += "The User Id must be a whole number greater than 0. \n"
            except ValueError:
                error = True
                msg += "The User Id must be a whole number greater than 0. \n"
            if (not (error)):
                try:
                    ## need validation of User ID
                    with sql.connect("HospitalUsers.db") as con:
                        con.row_factory = sql.Row
                        cur = con.cursor()
                        sql_select_query = """select * from HospitalUser where UserId = ? """
                        cur.execute(sql_select_query, (userId))

                        row = cur.fetchone();
                        if (row != None):
                            testName = cipher.encrypt(testName)
                            testResult = cipher.encrypt(testResult)

                            cur.execute(
                            "INSERT INTO UserTestResults ('UserId','TestName','TestResult') VALUES (?,?,?)",
                            (userId, testName, testResult))

                            con.commit()
                            msg = "Record successfully added"
                        else:
                            msg = "Error: Unknown User ID"

                except:
                    con.rollback()
                    msg = "error in insert operation"
        except:
            msg = "error in insert operation"
        print(msg)
if __name__  ==	"__main__":
    try:
        HOST,	PORT	=	"localhost",	9999
        #	Create	the	server,	binding	to	localhost	on	port	9999
        server	=	socketserver.TCPServer((HOST,	PORT),	MyTCPHandler)
        # Activate	the	server;	this	will	keep	running	until	you
        #	interrupt	the	program	with	Ctrl-C
        server.serve_forever()
    except server.error as e:
        print("Error:",e)
        exit(1)
    finally:
        server.close()
