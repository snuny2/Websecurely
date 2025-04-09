from flask import Blueprint, send_from_directory, make_response, request, jsonify
import sqlite3
import bcrypt
import secrets
import jwt

from appmain import app, mail
from appmain.utils import verifyJWT, getJWTContent
from flask_mail import Message

user = Blueprint('user', __name__)


@user.route('/signup')
def signUp():
    return send_from_directory(app.root_path, 'templates/signup.html')


@user.route('/signin')
def signIn():
    return send_from_directory(app.root_path, 'templates/signin.html')


@user.route('/myinfo')
def myPage():
    return send_from_directory(app.root_path, 'templates/mypage.html')


@user.route('/resetpw')
def resetpw():
    return send_from_directory(app.root_path, 'templates/reset_passwd.html')


@user.route('/api/user/signup', methods=['POST'])
def register():
    data = request.form

    username = data.get("username")
    email = data.get("email")
    passwd = data.get("passwd")

    hashedPW = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    if cursor:
        SQL = 'insert into users (username, email, passwd) values (?, ?, ?)'
        cursor.execute(SQL, (username, email, hashedPW))
        conn.commit()

        SQL = 'select * from users'
        cursor.execute(SQL)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()
    conn.close()

    payload = {"success": True}
    return make_response(jsonify(payload), 200)


@user.route('/api/user/signin', methods=['POST'])
def getAuth():
    data = request.form

    # 이메일과 패스워드를 얻음
    email = data.get("email")
    passwd = data.get("passwd")

    # DB에 저장된 패스워드와 비교
    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    payload = {"authenticated": False, "email": '', "username": '', "authtoken": ''}

    if cursor:
        SQL = 'select id, username, passwd from users where email = ?'
        cursor.execute(SQL, (email,))
        result = cursor.fetchone()

        if result:
            pwMatch = bcrypt.checkpw(passwd.encode('utf-8'), result[2])
            id = result[0]
            username = result[1]
        else:
            pwMatch = None

        # 패스워드가 같으면 로그인 토큰생성
        if pwMatch:
            authkey = secrets.token_hex(16)

            SQL = 'update users set authkey = ? where id = ?'
            cursor.execute(SQL, (authkey, id))
            conn.commit()

            token = jwt.encode({"id": id, "email": email, "username": username, "authkey": authkey},
                               app.config["SECRET_KEY"], algorithm='HS256')
            payload = {"authenticated": True, "email": email, "username": username, "authtoken": token}

            # print('user.signin: %s' %email)
        else:
            pass

            cursor.close()
        conn.close()

        return make_response(jsonify(payload), 200)


@user.route('/api/user/myinfo', methods=['POST'])
def getMyInfo():
    headerData = request.headers

    authToken = headerData.get("authtoken")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            email = token['email']

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                SQL = 'select username from users where email = ?'
                cursor.execute(SQL, (email,))
                username = cursor.fetchone()[0]
                cursor.close()
            conn.close()

            payload = {"success": True, "username": username}

        return make_response(jsonify(payload), 200)


@user.route('/api/user/update', methods=['POST'])
def updatreMyinfo():
    headerDate = request.headers
    data = request.form

    authToken = headerDate.get('authtoken')
    username = data.get("username")
    passwd = data.get("passwd")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            email = token['email']

            hashedPW = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                if passwd:
                    SQL = 'update users set username = ?, passwd = ? where email = ?'
                    cursor.execute(SQL, (username, hashedPW, email))
                else:
                    SQL = 'update users set username = ? where email = ?'
                    cursor.execute(SQL, (username, email))
                conn.commit()

                # SQL = 'select * from users'
                # cursor.execute(SQL)
                # rows = cursor.fetchall()
                # for row in rows:
                # print(row)

                cursor.close()
            conn.close()
    else:
        pass

    return make_response(jsonify(payload), 200)


@user.route('/api/user/resetpw', methods=['POST'])
def checkAndSendNewPW():

    data = request.form
    email = data.get("email")

    payload = {"success": False}

    conn = sqlite3.connect('pyBook.db')
    cursor = conn.cursor()

    if cursor:
        SQL = 'select id from users where email = ?'
        cursor.execute(SQL, (email,))
        result = cursor.fetchone()

        if result:
            id = result[0]
            randPW = secrets.token_hex(8)
            hashedPW = bcrypt.hashpw(randPW.encode('utf-8'), bcrypt.gensalt())

            SQL = 'update users set passwd = ? where id = ?'
            cursor.execute(SQL, (hashedPW, id))
            conn.commit()

            cursor.close()
            conn.close()

            msg = Message(subject='임시 비밀번호', sender='efzxcsh20@gmail.com', recipients=[email])
            msg.body = '임시 비밀번호입니다.: ' + randPW

            print('checkAndSendNewPW.mag:', msg)
            mail.send(msg)

            payload = {"success": True}
        else:
            payload = {"success": False, "message": '등록되어 있지 않은 이메일 입니다.'}
    else:
        pass

    return make_response(jsonify(payload), 200)
