import jwt
import sqlite3
import secrets
from PIL import Image
import os

from appmain import app

def verifyJWT(token):
    if token is None:
        return None
    else:
        try:
            decodedToken = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if decodedToken:
                conn = sqlite3.connect('pyBook.db')
                cursor = conn.cursor()

                if cursor:
                    SQL = 'select authkey from user where email = ?'
                    cursor.execute(SQL, (decodedToken['email'],))
                    authkey = cursor.fetchone()[0]
                    cursor.close()
                    conn.close()

                if authkey == decodedToken['authkey']:
                    return True
                else:
                    return None
            else:
                return None
        except:
            return None

def getJWTContent(token):
    isVerified = verifyJWT(token)

    if isVerified:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    else:
        return None

def savePic(pic, username):
    randHex = secrets.token_hex(8) # 파일이름을 대신할 문자열 생성
    _, fExt = os.path.splitext(pic.filename) # 파일이름과 확장자(ext)로 분리
    picFileName = randHex + fExt # 생성한 문자열과 분리한 확장자를 합친다
    picDir = os.path.join(app.static_folder, 'pics', username) # /appmain/static/pices/ 라는 디렉터리 생성
    picPath = os.path.join(picDir, picFileName) # 완성된 파일과 생성된 디렉터리를 합쳐 경로구성
    os.makedirs(picDir, exist_ok=True) # 디렉터리가 없으면 생성, 있으면 아무것도 안한다

    with Image.open(pic) as image: # 이미지파일을 읽음
        image.save(picPath) # 파일을 저장

    return picFileName # 나중에 파일을 찾을 수 있도록 파일이름을 반환