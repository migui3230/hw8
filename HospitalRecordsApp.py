"""
Name:Miguel Sarenas
Date:10/22/2023
Assignment:Module8:Send authenticated Message
Due Date:10/22/2023
About this project: this program shows how to send an authenticated message
Assumptions: sample data
All work below was performed by Miguel Sarenas
"""






from flask import Flask, render_template, request, session, flash
import sqlite3 as sql
import math
import re
from markupsafe import escape
import os
import socket
import Encryption
import pandas as pd
import hmac
import hashlib

key = b'\x89\xcc\x01y\xfd\xbd\xcd=Gv\x99m\xa5\x9f?f\x02\x86\xc9#\xea\xf7\xc3e\xd6\xa0\t\x06D\xad<\x84'
iv = b'w\xdb^K%\\\xf5,`\xc7\xbb\xabs\x1f\x06\x16'
cipher = Encryption.AESCipher(key, iv)


def create_app() -> Flask:
    app = Flask(__name__)
    ...
    return app


app = create_app()

# home
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', name=session['name'])

# add new user
@app.route('/enternew')
def new_hospitalAppUser():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('Level') == 3:
        return render_template('newHospitalAppUser.html')
    else:
        return render_template('login.html')

# enter new test result
@app.route('/enterTestResult')
def new_TestResult():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('Level') >= 3:
        return render_template('newTestResult.html')
    else:
        return render_template('login.html')

# send encrypted message
@app.route('/sendEncryptedMessage')
def send_encrypted_message():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('Level') >= 3:
        return render_template('sendEncryptedMessage.html')
    else:
        return render_template('login.html')

# add new test result
@app.route('/addTestResults', methods=['POST', 'GET'])
def addTestResult():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('Level') >= 2:
        if request.method == 'POST':
            try:
                error = False
                testNm = request.form['TestName']
                testResult = request.form['TestResult']
                UserId = request.form['UserId']
                testNm = str(testNm).lstrip()
                testResult = str(testResult).lstrip()

                msg = "\n"
                if (len(testNm) == 0):
                    error = True
                    msg += "You can not enter in an empty test name \n"

                if (len(testResult) == 0):
                    error = True
                    msg += "You can not enter in an empty test Result \n"

                try:
                    if (int(UserId) <= 0):
                        error = True
                        msg += "The User Id must be a whole number greater than 0. \n"
                except ValueError:
                    error = True
                    msg += "The User Id must be a whole number greater than 0. \n"

                if (not (error)):
                    sep = "^%$"
                    msg = UserId+sep+testNm+sep+testResult
                    msg = cipher.encrypt(msg)

                    HOST, PORT = "localhost", 9999
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Connect to server and send data
                    sock.connect((HOST, PORT))

                    sock.sendall(msg)
                    sock.close()

                    msg = "Help message sent!"

            finally:
                return render_template("result.html", msg=escape(msg))
    else:
        return render_template('login.html')

# process encrypted message
@app.route('/processEncryptedMessage', methods=['POST'])
def process_encrypted_message():
    TestResultId = request.form.get('TestResultId')
    TestResult = request.form.get('TestResult')

    if not TestResultId or not TestResultId.isdigit() or int(TestResultId) <= 0:
        return render_template("result.html", msg="Invalid TestResultId")
    if not TestResult or TestResult.strip() == "":
        return render_template("result.html", msg="Invalid TestResult")

    try:
        HOST, PORT = "localhost", 8888
        msg = TestResultId + "|SEP|" + TestResult
        encrypted_message = cipher.encrypt(msg)
        hmac_signature = hmac.new(
            key, encrypted_message, hashlib.sha512).digest()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(encrypted_message + hmac_signature)
            sock.close()

        return render_template("result.html", msg="Test Result Update successfully sent")
    except Exception as e:
        return render_template("result.html", msg="Error - Test Result Update NOT sent")

# add new user
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('Level') == 3:
        if request.method == 'POST':
            try:
                error = False
                nm = request.form['Name']
                phNum = request.form['PhoneNumber']
                Age = request.form['Age']
                if (request.form.get('HasCOVID')):
                    hasCOVID = 1
                else:
                    hasCOVID = 0
                SecurityRoleLevel = request.form['SecurityRoleLevel']
                pwd = request.form['Password']

                nm = str(nm).lstrip()
                phNum = str(phNum).lstrip()
                pwd = str(pwd).lstrip()

                msg = "\n"
                if (len(nm) == 0):
                    error = True
                    msg += "You can not enter in an empty name \n"

                if (len(phNum) == 0):
                    error = True
                    msg += "You can not enter in an empty phone number \n"

                try:
                    if ((int(Age) <= 0) or (int(Age) > 120)):
                        error = True
                        msg += "The Age must be a whole number greater than 0 and less than 121. \n"
                except ValueError:
                    error = True
                    msg += "The Age must be a whole number greater than 0 and less than 121. \n"

                try:
                    if ((int(SecurityRoleLevel) <= 0) or (int(SecurityRoleLevel) > 3)):
                        error = True
                        msg += "The SecurityRoleLevel must be a numeric between 1 and 3. \n"
                except ValueError:
                    error = True
                    msg += "The SecurityRoleLevel must be a numeric between 1 and 3. \n"

                if (len(pwd) == 0):
                    error = True
                    msg += "You can not enter in an empty pwd \n"

                if (not (error)):
                    with sql.connect("HospitalUsers.db") as con:
                        cur = con.cursor()

                        nm = cipher.encrypt(nm)
                        phNum = cipher.encrypt(phNum)
                        pwd = cipher.encrypt(pwd)

                        cur.execute("INSERT INTO HospitalUser (UserName,UserAge,UserPhNum,UserHasCOVID,UserSecurityLevel,LoginPassword) VALUES (?,?,?,?,?,?)", (
                            nm, Age, phNum, hasCOVID, SecurityRoleLevel, pwd))

                        con.commit()
                        msg = "Record successfully added"
            except:
                con.rollback()
                msg = "error in insert operation"

            finally:
                return render_template("result.html", msg=escape(msg))
                con.close()
    else:
        return render_template('login.html')

# add data 
@app.route('/list')
def list():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('Level') >= 2:
        con = sql.connect("HospitalUsers.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute(
            "select UserName,UserAge,UserPhNum,UserHasCOVID,UserSecurityLevel,LoginPassword from HospitalUser")
        df = pd.DataFrame(cur.fetchall(), columns=[
                          'UserName', 'UserAge', 'UserPhNum', 'UserHasCOVID', 'UserSecurityLevel', 'LoginPassword'])
        df['UserName'] = df['UserName'].apply(lambda x: cipher.decrypt(x))
        df['UserPhNum'] = df['UserPhNum'].apply(lambda x: cipher.decrypt(x))
        df['LoginPassword'] = df['LoginPassword'].apply(
            lambda x: cipher.decrypt(x))

        return render_template("list.html", rows=df)
    else:
        return render_template('login.html')

# add test results
@app.route('/testResults')
def testResults():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        con = sql.connect("HospitalUsers.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select TestName, TestResult from UserTestResults where UserId = ?", [
                    session['UserId']])
        df = pd.DataFrame(cur.fetchall(),
                          columns=['TestName', 'TestResult'])
        df['TestName'] = df['TestName'].apply(lambda x: cipher.decrypt(x))
        df['TestResult'] = df['TestResult'].apply(lambda x: cipher.decrypt(x))
        print(df)
        return render_template("TestResults.html", rows=df)

# show user data
@app.route('/showUser')
def showUser():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        con = sql.connect("HospitalUsers.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        sql_select_query = """select UserName,UserAge,UserPhNum,UserHasCOVID,UserSecurityLevel,LoginPassword from HospitalUser where UserName = ? """
        cur.execute(sql_select_query, [cipher.encrypt(session['name'])])
        df = pd.DataFrame(cur.fetchall(), columns=[
                          'UserName', 'UserAge', 'UserPhNum', 'UserHasCOVID', 'UserSecurityLevel', 'LoginPassword'])

        # UserName
        df.iat[0, 0] = cipher.decrypt(df.iat[0, 0])
        # UserPhNum
        df.iat[0, 2] = cipher.decrypt(df.iat[0, 2])
        # LoginPassword
        df.iat[0, 5] = cipher.decrypt(df.iat[0, 5])

        return render_template("ShowHospitalAppUser.html", row=df)

# do admin login
@app.route('/login', methods=['POST'])
def do_admin_login():

    try:
        nm = request.form['username']
        pwd = request.form['password']

        with sql.connect("HospitalUsers.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            name = nm
            nm = cipher.encrypt(nm)
            pwd = cipher.encrypt(pwd)
            sql_select_query = """select * from HospitalUser where UserName = ? and LoginPassword = ?"""
            cur.execute(sql_select_query, (nm, pwd))

            row = cur.fetchone()
            if (row != None):
                session['logged_in'] = True
                session['UserId'] = int(row['UserId'])
                session['name'] = name
                session['Level'] = int(row['UserSecurityLevel'])
            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')
    except:
        con.rollback()
        flash("error in insert operation")
    finally:
        con.close()
    return home()

# logout
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['level'] = -99
    session['name'] = ""
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
