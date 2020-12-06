from urllib import response

from flask import Flask, render_template, request, redirect, make_response
import pymysql
from datetime import timedelta
from flask_cors import *

from testFlask import cursor

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
CORS(app, supports_credentials=True)


# 打开数据库连接
# db = pymysql.connect(host='121.196.111.9',
#                      port=3306,
#                      user='test',
#                      passwd='123456',
#                      db='blogs'
#                      )
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
#
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")
#
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
#
# print("Database version : %s " % data)
#
# # 关闭数据库连接
# db.close()


@app.route('/homepage')
def homepage():
    return render_template("homepage.html")


# @app.route('/index')
# def index():

# @app.route('/index/<kind>', methods=['GET', 'POST'])
# def signup(kind):
#     if request.method == 'GET':
#         print(request.values.get('name'))
#         return "200"
#     return redirect("index");


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/index/getNewBlog')
def gethottag():
    currentPage = int(request.values.get("currentPage"))
    pageSize = int(request.values.get("pageSize"))
    data = {}
    sql = "SELECT COUNT(*) FROM Blog"
    cursor.execute(sql)
    total = cursor.fetchone()[0]
    print(total)
    data['total'] = total
    data['currentPage'] = currentPage + 1
    print(data['currentPage'])
    records = []
    sql = "SELECT * FROM Blog ORDER BY publish_time"
    cursor.execute(sql)
    row = cursor.fetchone()
    print(row)

    start = (currentPage - 1) * pageSize
    end = currentPage * pageSize
    i = 0
    size = 0
    while row:
        if i >= start:
            size += 1
            record = {}
            record['user_id'] = row[1]
            record['label'] = row[9]
            record['summary'] = row[4][0:100]
            record['clickCount'] = row[7]
            record['likeCount'] = row[6]
            record['time'] = row[2].strftime("%Y-%m-%d %H:%M:%S")
            record['title'] = row[3]
            print(record)
            records.append(record)
            i += 1
            if i >= end:
                break
        row = cursor.fetchone()

    data['size'] = size
    data['code']='success'
    data['records'] = records
    return data


@app.route('/')
def welcome():
    return render_template("Welcome.html")


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000, debug=True)
