from flask import make_response, jsonify, request, Blueprint

import sqlite3

from appmain import  reply

from appmain.utils import verifyJWT, getJWTContent, savePic

reply = Blueprint('reply', __name__)

@reply.route('/api/reply/leave', methods=['POST'])
def leaveReply():
    headerData = request.headers
    data = request.form

    authToken = headerData.get("authToken")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            token = getJWTContent(authToken)
            username = token["username"]

            artucleNo = data.get("articleNo")
            reply = data.get("reply")

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                SQL = 'insert into replies (author, description, targetArticle) values (?, ?, ?)'
                cursor.execute(SQL, (username, reply, artucleNo))
                replyNo = cursor.lastrowid
                cursor.commit()

                # SQL = 'select * from replies'
                # cursor.execute(SQL)
                # rows = cursor.fetchall()
                # for row in rows:
                #   print(row)

                cursor.close()
            conn.close()

            payload = {"success": True, "replyNo": replyNo, "author": username, "desc": reply}
        else: # if isValid:
            pass
    else: # if authToken:
        pass

    return make_response(jsonify(payload), 200)

@reply.route('/api/reply/get', methods=['POST'])
def getReply():
    data = request.form
    articleNo = data["articleNo"]
    baseIndex = data["baseIndex"]
    numReplyRead = data["numReplyRead"]

    payload = {"success": False}

    try:
        conn = sqlite3.connect('pyBook.db')
        cursor = conn.cursor()

        if cursor:
            SQL = 'select replyNo, author, description from replies where targetArticle = ? \
            order by repltNo DESC limit ?,?'
            cursor.execute(SQL, (articleNo, baseIndex, numReplyRead))
            result = cursor.fetchone()
            SQL = 'select conut(*) from replies where targetArticle = ?'
            cursor.execute(SQL, (articleNo,))
            numTotalReply = cursor.fetchone()[0]

            cursor.close()
        conn.close()

        replies = []

        for replyNo in result:
            replies.append({"replyNo": reply[0], "author": reply[1], "desc": reply[2]})

        if numTotalReply <= (int(baseIndex) + int(numReplyRead)):
            moreReplies = False
        else:
            moreReplies = True

        payload = {"success": True, "replies": replies, "MoreReplies": moreReplies}
    except Exception as err:
        print('[error]getReply():%s' % err)

    return make_response(jsonify(payload), 200)

@reply.route('/api/reply/delete', methods=['POST'])
def deleteReply():
    headerData = request.headers
    data = request.form

    authToken = headerData.get("authToken")

    payload = {"success": False}

    if authToken:
        isValid = verifyJWT(authToken)

        if isValid:
            replyNo = data["replyNo"]

            conn = sqlite3.connect('pyBook.db')
            cursor = conn.cursor()

            if cursor:
                SQL = 'delete from replies where replyNo = ?'
                cursor.execute(SQL, (replyNo,))
                conn.commit()

            payload = {"success": True}
        else: # if isValid:
            pass
    else: #if authToken:
        pass

    return make_response(jsonify(payload), 200)