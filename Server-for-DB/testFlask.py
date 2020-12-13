from flask import Flask, request
import pymysql

app = Flask(__name__)  # 创建一个服务，赋值给APP
db = pymysql.connect(host='121.196.111.9',
                     port=3306,
                     user='test',
                     passwd='123456',
                     db='blogs'
                     )
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("%s" % data)


@app.route('/index/getNewBlog', methods=['get'])  # 指定接口访问的路径，支持什么请求方式get，post
def getNewBlog():
    print("---------------")
    currentPage = request.values.get("currentPage")
    pageSize = request.values.get("pageSize")
    data = {}
    sql = "SELECT COUNT(*) FROM Blog"
    cursor.execute(sql)
    total = cursor.fetchall()
    print(total)
    data['total'] = total
    data['currentPage'] = currentPage+1
    records = []
    sql = "SELECT COUNT(*) FROM Blog ORDER BY publish_time"
    cursor.execute(sql)
    row = cursor.fetchone()
    start = (currentPage - 1) * pageSize
    end = currentPage * pageSize
    i = 0
    size=0
    while row:
        if i >= start:
            size+=1
            record = {}
            record['user_id'] = row[1]
            record['label'] = row[9]
            record['summary'] = row[4][0:100]
            record['clickCount'] = row[7]
            record['likeCount'] = row[6]
            record['time'] = row[2]
            print(record)
            records.append(record)
            i += 1
            if i >= end:
                break
        row = cursor.fetchone()

    data['size']=size
    data['records']=records

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
