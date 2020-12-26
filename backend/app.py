import datetime
import json

import requests
from flask import Flask, request, render_template
import pymysql
from flask_cors import CORS

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
CORS(app, supports_credentials=True)
db = pymysql.connect(host='121.196.111.9',
                     port=3306,
                     user='test',
                     passwd='123456',
                     db='blogs'
                     )
db.autocommit(True)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
version = cursor.fetchone()

labels = {'1': "科技", '2': "新闻", '3': "美食", '4': "校园", '5': "更多"}
user_info = {
    'user_id':'',
    'name':'',
    'password':'',
    'email':'',
    'credit':0,
    'role':0,
    'state':0,
    'reputation':5
}

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     if app.debug:
#         return requests.get('http://localhost:8603/{}'.format(path)).text
#     return render_template("index.html")

def updateUserInfo():
    sql='SELECT name,password,email,credit,role,state,reputation FROM Blog_user WHERE user_id="%s"'%user_info['user_id']
    cursor.execute(sql)
    row=cursor.fetchone()
    if row!=None:
        user_info['name']=row[0]
        user_info['password']=row[1]
        user_info['email']=row[2]
        user_info['credit']=row[3]
        user_info['role']=row[4]
        user_info['reputation']=row[6]
        user_info['state']=row[5]
        file_object = open("user_info.txt", "w")
        json.dump(user_info, file_object)
        file_object.close()

# 1.index
@app.route('/index/getNewBlog', methods=['GET'])  # 指定接口访问的路径，支持什么请求方式get，post
def getNewBlog():
    currentPage = int(request.values.get("currentPage"))
    pageSize = int(request.values.get("pageSize"))
    data = {}
    sql = "SELECT COUNT(*) FROM Blog WHERE state=0"
    cursor.execute(sql)
    total = cursor.fetchone()
    data['total'] = total
    data['currentPage'] = currentPage + 1
    records = []
    sql = "SELECT blog_id,Blog.user_id,publish_time,title,summary,content,approval_number,browse_number,need_credit,label,Blog.state,activity,name FROM Blog,Blog_user WHERE Blog_user.user_id=Blog.user_id AND Blog.state=0 ORDER BY publish_time DESC"
    cursor.execute(sql)
    row = cursor.fetchone()
    start = (currentPage - 1) * pageSize
    end = currentPage * pageSize
    i = 0
    size = 0
    while row:
        if i >= start:
            size += 1
            record = {}
            record['user_id'] = row[1]
            record['blog_id'] = row[0]
            record['name']=row[12]
            blog_labels = row[9].split(",")
            blog_label_name = []
            for blog_label in blog_labels:
                blog_label_name.append(labels[blog_label])

            record['labels'] = blog_label_name
            record['summary'] = row[4][0:100]
            record['clickCount'] = row[7]
            record['likeCount'] = row[6]
            record['time'] = row[2].strftime("%Y-%m-%d %H:%M:%S")
            record['title'] = row[3]
            records.append(record)
            i += 1
            if i >= end:
                break
        row = cursor.fetchone()

    data['size'] = size
    data['code'] = 'success'
    data['records'] = records
    return data


# 2.TagCloud;
@app.route('/index/getHotTag', methods=['GET'])
def getHotTag():
    data = {}
    data['records'] = [{'uid': '1', 'name': '科技'},
                       {'uid': '2', 'name': '新闻'},
                       {'uid': '3', 'name': '美食'},
                       {'uid': '4', 'name': '校园'},
                       {'uid': '5', 'name': '更多'}]
    data['code'] = 'success'
    return data


# 3.info

@app.route('/api/getBlogByUid', methods=['GET'])
def getBlogByUid():
    blog_id = int(request.values.get("blog_id"))
    sql = "SELECT blog_id,Blog.user_id,publish_time,title,summary,content,approval_number,browse_number,need_credit,label,Blog.state,activity,name FROM Blog,Blog_user WHERE Blog_user.user_id=Blog.user_id AND blog_id=" + str(blog_id)
    cursor.execute(sql)
    blog = cursor.fetchone()
    print(blog_id)
    result = {}
    result['blogSort'] = blog[11]
    result['title'] = blog[3]
    result['author'] = blog[1]
    result['name']=blog[12]
    sql = "SELECT name FROM Activity WHERE activity_id=%d" % (blog[11])
    cursor.execute(sql)
    sortname = cursor.fetchone()
    result['blogSortName'] = sortname[0]

    blog_labels = blog[9].split(",")
    blog_label_name = []
    for blog_label in blog_labels:
        blog_label_name.append(labels[blog_label])
    result['labels'] = blog_label_name
    result['summary'] = blog[4]
    result['clickCount'] = blog[7]
    result['likeCount'] = blog[6]
    result['time'] = blog[2].strftime("%Y-%m-%d %H:%M:%S")
    result['content'] = blog[5]

    sql = 'SELECT * FROM History WHERE user_id="%s" AND blog_id=%d' % (user_info['user_id'], blog_id)
    cursor.execute(sql)
    row = cursor.fetchall()
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if len(row) == 0:
        if user_info['reputation'] == 5:
            result['need_credit'] = blog[8]
        elif user_info['reputation'] == 4:
            result['need_credit'] = blog[8] * 1.05
        elif user_info['reputation'] == 3:
            result['need_credit'] = blog[8] * 1.1
        elif user_info['reputation'] == 2:
            result['need_credit'] = blog[8] * 1.2
        elif user_info['reputation'] == 1:
            result['code'] = 'error'
            result['message'] = '您信誉积分过低，无法查看'
            return result

        if result['need_credit'] == 0 and user_info['user_id'] is not '':
            sql = 'INSERT INTO History VALUES("%s",%d,"%s")' % (user_info['user_id'], blog_id,time)
            cursor.execute(sql)
            sql = 'UPDATE Blog SET browse_number=browse_number+1 WHERE blog_id=%d' % blog_id
            cursor.execute(sql)
            result['clickCount']+=1

    else:
        result['need_credit'] = 0
        sql = "UPDATE History SET time='%s' WHERE user_id='%s' AND blog_id='%d'" % (time,user_info['user_id'], blog_id)
        cursor.execute(sql)
        sql = 'UPDATE Blog SET browse_number=browse_number+1 WHERE blog_id=%d' % blog_id
        cursor.execute(sql)
        result['clickCount']+=1
    updateUserInfo()
    result['code'] = 'success'
    return result


@app.route('/index/getWebConfig', methods=['GET'])
def getWebConfig():
    data = {}
    data['createTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['openAdmiration'] = '1'
    data['openComment'] = '1'
    data['code'] = 'success'
    return data


@app.route('/web/comment/payCreditByUid', methods=['GET'])
def payCreditByUid():
    blog_id = int(request.values.get("blog_id"))
    data = {}
    credit=0;
    sql = 'CALL readBlog(%d,"%s",%s)' % (blog_id, user_info['user_id'],'@credit')
    cursor.execute(sql)
    sql1=" select @credit"
    cursor.execute(sql1)
    recredit=cursor.fetchone()[0]
    if user_info['reputation']==1:
        data['code']='error'
        data['message']='你个烂人信誉积分只有1，你不配'
        return data
    if recredit > 0:
        data['code'] = 'success'
    elif recredit < 0:
        data['code'] = 'error'
        data['message'] = '您积分不足，差%d' % recredit


    updateUserInfo()
    return data


@app.route('/web/comment/add', methods=['POST'])
def addComment():
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    blogUid = int(data_json.get("blogUid"))
    userUid = data_json.get("userUid")
    content = data_json.get("content")
    sql = 'SELECT MAX(comment_id) FROM Comment'
    cursor.execute(sql)
    row = cursor.fetchone()
    comment_id = 0
    if row[0] == None:
        comment_id = 1
    else:
        comment_id = int(row[0]) + 1
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = 'INSERT INTO Comment(comment_id,user_id,blog_id,time,content) VALUES (%d,"%s",%d,"%s","%s")' % (
    comment_id, user_info['user_id'], blogUid,time, content)
    cursor.execute(sql)

    data = {}
    data['code'] = 'success'
    return data


# 6.home
@app.route('/oauth/getFeedbackList',methods=['GET'])
def getFeedbackList():
    data={}
    sql='SELECT content FROM Blog_message WHERE user_id="%s"'%user_info['user_id']
    cursor.execute(sql)
    row=cursor.fetchone()
    records=[]
    while row!=None:
        records.append(row[0])
        row=cursor.fetchone()
    print(records)
    data['records']=records
    data['code']='success'
    return data


@app.route('/getUserinfo',methods=['GET'])
def getUserInfo():
    data={}
    data['user_info']=user_info
    data['code']='success'
    return data

@app.route('/logout/logout', methods=['GET'])
def logout():
    global user_info
    data = {}
    # user_info['user_id'] = ''
    #     # user_info['name'] = ''
    #     # user_info['password'] = ''
    #     # user_info['email'] = ''
    #     # user_info['credit'] = ''
    #     # user_info['role'] = 0
    #     # user_info['reputation'] = 5
    #     # user_info['state'] = 1
    user_info = {
        'user_id': '',
        'name': '',
        'password': '',
        'email': '',
        'credit': 0,
        'role': 0,
        'state': 0,
        'reputation': 5
    }
    f = open('user_info.txt', 'w')
    f.write(str(user_info))
    print(user_info)
    f.close()
    data['code'] = 'success'
    data['message'] = '退出成功'
    return data

@app.route('/web/comment/getFollowListByUser')
def getFollowListByUser():
    data = {}
    records = []
    sql = 'SELECT follower_id,time,name FROM Follow,Blog_user WHERE Follow.user_id=Blog_user.user_id AND Follow.user_id="%s" ORDER BY time DESC' % \
          user_info['user_id']
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        record = {}
        record['follower_id'] = row[0]
        idd = row[0]
        sql1 = " SELECT name from Blog_user WHERE user_id = %s" %idd
        cursor.execute(sql1)
        nname = cursor.fetchone()[0]
        record['createTime'] = row[1]
        record['nickName'] = nname
        records.append(record)
        row = cursor.fetchone()

    data['records'] = records
    data['code'] = 'success'
    return data


@app.route('/web/comment/getCollectListByUser')
def getCollectListByUser():
    data = {}
    records = []
    sql = 'SELECT blog_id,time,name FROM Favorites WHERE user_id="%s" ORDER BY time DESC' % user_info['user_id']
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        record = {}
        record['blog_id'] = row[0]
        record['createTime'] = row[1]
        record['name'] = row[2]
        records.append(record)
        row = cursor.fetchone()

    data['records'] = records
    data['code'] = 'success'
    return data


@app.route('/web/comment/getHistoryListByUser', methods=['POST'])
def getHistoryListByUser():
    data = {}
    records = []
    sql = 'SELECT History.blog_id,time,title ' \
          'FROM History,Blog ' \
          'WHERE History.blog_id=Blog.blog_id AND History.user_id="%s" AND state=0 ' \
          'ORDER BY time DESC' % user_info['user_id']
    cursor.execute(sql)
    row = cursor.fetchone()
    i = 0
    while row:
        i += 1
        record = {}
        record['blog_id'] = row[0]
        record['createTime'] = row[1]
        record['title'] = row[2]
        records.append(record)
        row = cursor.fetchone()

    data['records'] = records
    if i == 0:
        data['code'] = 'error'
        data['message'] = '暂无历史浏览记录'
    else:
        data['code'] = 'success'
    return data

@app.route('/search/sqlSearchBlog',methods=['GET'])
def search():
    # currentPage = int(request.values.get("currentPage"))
    # pageSize = int(request.values.get("pageSize"))
    str = request.values.get("keywords")
    data = {}
    sql = 'SELECT COUNT(*) FROM Blog WHERE state=0 AND title LIKE %s '
    params=['%'+str+'%']
    print(sql)
    cursor.execute(sql,params)
    total = cursor.fetchone()[0]
    print(total)
    data['total'] = total
    # data['currentPage'] = currentPage + 1
    # print(data['currentPage'])
    records = []
    sql = 'SELECT * FROM Blog WHERE state=0 AND title LIKE %s  ORDER BY publish_time DESC'
    cursor.execute(sql,params)
    row = cursor.fetchone()
    # start = (currentPage - 1) * pageSize
    # end = currentPage * pageSize
    size = 0
    while row:
        size += 1
        record = {}
        record['user_id'] = row[1]
        record['blogUid']=row[0]
        blog_labels = row[9].split(",")
        blog_label_name = []
        for blog_label in blog_labels:
            blog_label_name.append(labels[blog_label])

        record['labels'] = blog_label_name
        record['summary'] = row[4][0:100]
        record['clickCount'] = row[7]
        record['likeCount'] = row[6]
        record['time'] = row[2].strftime("%Y-%m-%d %H:%M:%S")
        record['title'] = row[3]
        print(record)
        records.append(record)

        row = cursor.fetchone()

    data['size'] = size
    data['code'] = 'success'
    data['records'] = records
    return data


@app.route('/web/comment/getListByUser', methods=['POST'])
def getCommentListByUser():
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    data = {}
    commentList = []
    replyList = []
    user_id = user_info['user_id']
    sql = "select name from Blog_user where user_id=" + user_id
    cursor.execute(sql)
    name = cursor.fetchone()[0]
    # 前面的name是我评论的文章的作者的姓名，后面的name是评论我的文章的用户姓名
    sql = "SELECT Comment.comment_id,Comment.user_id,Comment.blog_id,Comment.time,Comment.content,Blog.user_id,Blog_user.name from Comment,Blog,Blog_user where Comment.blog_id=Blog.blog_id and Blog_user.user_id=Blog.user_id and Comment.user_id=" + user_id;
    cursor.execute(sql)
    row = cursor.fetchone()
    end = 10
    comment = 0
    reply = 0
    size = 0
    while row:
        if comment <= 10:
            comment += 1
            record = {}
            record['uid'] = row[0]
            record['createTime'] = row[3]
            record['blogUid'] = row[2]
            user = {}
            user['nickName'] = row[6]
            user['source'] = 'BLOG_INFO'
            user['sourceName'] = '博客详情'
            user['content'] = row[4]
            record['user'] = user
            commentList.append(record)
        else:
            break;
        row = cursor.fetchone()

    sql = "SELECT Comment.comment_id,Comment.user_id,Comment.blog_id,Comment.time,Comment.content,Blog.user_id,Blog_user.name from Comment,Blog,Blog_user where Comment.blog_id=Blog.blog_id and Blog_user.user_id=Comment.user_id and Blog.user_id=" + user_id;
    cursor.execute(sql)
    row = cursor.fetchone()
    end = 10
    comment = 0
    reply = 0
    size = 0
    while row:
        if reply <= 10:
            reply += 1
            record = {}
            record['uid'] = row[0]
            record['createTime'] = row[3]
            record['blogUid']=row[2]
            user = {}
            # 评论我的博客的用户名称
            user['nickName'] = row[6]
            user['source'] = 'BLOG_INFO'
            user['sourceName'] = '博客详情'
            user['content'] = row[4]
            record['user'] = user
            replyList.append(record)
        else:
            break;
        row = cursor.fetchone()

    data['code'] = 'success'
    data['commentList'] = commentList
    data['replyList'] = replyList
    return data


@app.route('/api/praiseBlogByUid', methods=['GET'])
def praiseBlogByUid():
    print("I am in praiseBlogByUid")
    id = int(request.values.get('uid'))
    # SQL语句点赞数+1
    sql1 = "UPDATE Blog SET approval_number = approval_number+1 WHERE blog_id='%d'" % id
    # SQL语句查询点赞数
    sql2 = "SELECT approval_number FROM Blog WHERE blog_id='%d'" % id
    sql3 = "INSERT INTO `blogs`.`Approval` (`user_id`, `blog_id`, `time`) VALUES ('%s', '%d', current_time);" % (
        user_info["user_id"], id)

    # 执行SQL语句
    flag=False
    try:
        cursor.execute(sql2)
        number = cursor.fetchall()
        cursor.execute(sql3)
        cursor.execute(sql1)
        flag=True
    except:
        flag=False
    if flag==True:
        return {"code": 'success', "number": number[0][0]+1}

    return {"code": 'error', "number": number[0][0], "message": "您已经点过赞了！"}


def getPraise(id):
    sql = "SELECT approval_number FROM Blog WHERE blog_id='%d'" % id
    try:
        # 执行SQL语句
        cursor.execute(sql)
        number = cursor.fetchall()
    except:
        print('error')
        db.rollback()
    return number


@app.route('/api/getBlogPraiseCountByUid', methods=['GET'])
def getBlogPraiseCountByUid():
    print("I am in getBlogPraiseCountByUid")
    id = int(request.values.get('uid'))
    return getPraise(id)


#  这里没写！
@app.route('/api/addCollectBlog', methods=['GET'])
def addCollectBlog():
    print("I am in addCollectBlog")
    id = int(request.values.get('uid'))
    collectName = str(request.values.get('collectName'))
    data = {}
    print(user_info)
    if user_info['user_id']=='':
        data["code"] = 'error'
        data['message']='您尚未登录！'
        return data
    sql = "INSERT INTO `blogs`.`Favorites` (`user_id`, `blog_id`, `time`, `name`) VALUES ('%s', '%d', current_time, '%s');" % (
        user_info['user_id'], id, collectName)
    try:
        cursor.execute(sql)
        data['code'] = 'success'
    except:
        db.rollback()
        data['code']='error'
        data['message']='您已经收藏过了'
        print('error啦！！！！')
    return data


#  这里没写！

@app.route('/web/comment/getPraiseListByUser', methods=['POST'])
def getPraiseList():
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    currentPage = data_json.get("currentPage")
    pageSize = data_json.get("pageSize")
    data = {}
    records = []
    data["records"] = records
    user_id = user_info['user_id']
    sql = "select Approval.user_id,Approval.blog_id,Approval.time,Blog.title from Approval,Blog where Approval.blog_id=Blog.blog_id and Approval.user_id='" + user_id + "'";
    cursor.execute(sql)
    row = cursor.fetchone()
    start = (currentPage - 1) * pageSize
    end = currentPage * pageSize
    i = 0
    size = 0
    while row:
        if i >= start:
            size += 1
            record = {}
            record['uid'] = row[0]
            record['createTime'] = row[2]
            user = {}
            user['uid'] = row[1]
            user['title'] = row[3]
            record['blog'] = user
            records.append(record)
            i += 1
            if i >= end:
                break
        row = cursor.fetchone()

    data['code'] = 'success'
    data['records'] = records
    return data


@app.route('/oauth/verify/<params>')
def authVerify(params):
    data = {}
    # sql = "SELECT * FROM Blog_user WHERE user_id = '%s'" % params
    # cursor.execute(sql)
    # results = cursor.fetchall()
    # for row in results:
    #     user_info['user_id'] = row[0]
    #     user_info['name'] = row[1]
    #     user_info['password'] = row[2]
    #     user_info['email'] = row[3]
    #     user_info['credit'] = row[4]
    #     user_info['role'] = row[5]
    #     user_info['state'] = row[6]
    #     user_info['reputation'] = row[7]
    # data['id'] = user_info.get('user_id')
    # if int(user_info['reputation']) == 0:
    #     data['message'] = '你个烂人！'
    #     data['code'] = 'error'
    #     return data
    # if (params == user_info["user_id"]):
    global user_info
    file=open("user_info.txt", 'r')
    user_info=json.load(file)
    print(user_info)
    file.close()
    print("用户登录正常")
    data['uid'] = user_info['user_id']
    data['nickName'] = user_info['name']
    data['email'] = user_info['email']
    data['credit'] = user_info['credit']
    data['role'] = user_info['role']
    data['reputation'] = user_info['reputation']
    data['code'] = 'success'
    data['message'] = '恭喜登录成功!'
    # else:
    #     print("用户登录异常！")
    #     data['code'] = 'error'
    #     data['message']='上一个账号未退出'
    return data


# 7.blog
# @app.route('/tag/getTagList', methods=['GET'])
# def getBlogTagList():
#     data = {}
#     records = [{"uid": 1, "content": "科技"}, {"uid": 2, "content": "新闻"}, {"uid": 3, "content": "美食"},
#                {"uid": 4, "content": "校园"}, {"uid": 5, "content": "更多"}]
#     data['records'] = records
#     data['code'] = 'success'
#     return data


@app.route('/blogSort/getList', methods=['GET'])
def getBlogSortList():
    data = {}
    records = []
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "SELECT activity_id,name,description FROM Activity WHERE start_time<='%s' AND end_time>='%s'"%(time,time)
    cursor.execute(sql)
    row = cursor.fetchone()
    i = 0
    while row:
        i += 1
        activity = {}
        activity['uid'] = int(row[0])
        activity['name'] = row[1]
        records.append(activity)
        row = cursor.fetchone()

    data['records'] = records
    if i == 0:
        data['code'] = 'error'
        data['message'] = '暂无活动'
    else:
        data['code'] = 'success'
    return data


@app.route('/blog/add', methods=['POST'])
def addBlog():
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    form = data_json
    sql = "SELECT MAX(blog_id) FROM Blog"
    cursor.execute(sql)
    max_id = cursor.fetchone()
    if max_id == None:
        blog_id = 1
    else:
        blog_id = max_id[0] + 1
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    label_num = form.get("tagUid")
    activityid = str(form.get("blogSortUid"))
    sql = "INSERT INTO Blog VALUES (" + str(blog_id) + ",\"" + user_info['user_id'] + \
          "\",\""+time+"\",\"" + form.get("title") + "\",\"" + form.get("summary") + "\",\"" + \
          form.get("content") + "\",0,0," + form.get("need_credit") + ",\"" + label_num + "\",0," + activityid + ")"
    cursor.execute(sql)
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = 'INSERT INTO History VALUES ("%s",%d,"%s")' % (user_info['user_id'], blog_id,time)
    cursor.execute(sql)
    sql='SELECT credit FROM Activity WHERE activity_id=%s'%activityid
    cursor.execute(sql)
    credit=int(cursor.fetchone()[0])
    sql='UPDATE Blog_user SET credit=credit+%d WHERE user_id="%s"'%(credit,user_info['user_id'])
    cursor.execute(sql)
    updateUserInfo()
    data = {}
    data['code'] = 'success'
    data['message'] = '发布博客成功'
    return data


# 8.FollowBtn
@app.route('/api/getFollowedByUid', methods=['GET'])
def getFollowedByUid():
    uid = request.values.get("uid")
    print("getfollowedbyuid")
    print(user_info)
    print(uid)
    sql = "SELECT * FROM Follow WHERE user_id=\"" + user_info['user_id'] + "\" AND follower_id='" + uid + "'"
    cursor.execute(sql)
    row = cursor.fetchone()
    data = {}
    if row == None:
        data['liked'] = 0
    else:
        data['liked'] = 1
    data['code'] = 'success'
    print(data.get('liked'))
    return data


@app.route('/api/FollowByUid', methods=['GET'])
def followByUid():
    uid = request.values.get("uid")
    if uid == user_info['user_id']:
        data = {}
        data['code'] = 'error'
        data['message'] = '自己不能关注自己'
        return data

    sql = "SELECT * FROM Follow WHERE user_id= '" + user_info['user_id'] + "' AND follower_id= '" + uid + "'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row == None:
        print(user_info['user_id'] )
        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO Follow VALUES ('" + user_info['user_id'] + "','" + uid + "','"+time+"')"
        cursor.execute(sql)
    else:
        sql = "DELETE FROM Follow WHERE user_id= '" + user_info['user_id'] + "' AND follower_id='" + uid + "'"
        cursor.execute(sql)
    data = {}
    data['code'] = 'success'
    return data


# 9.sort
@app.route('/sort/getSortList', methods=['GET'])
def getSortList():
    data = {}
    records = []
    sql = "SELECT activity_id,name,description FROM Activity"
    cursor.execute(sql)
    row = cursor.fetchone()
    i = 0
    while row:
        print(row)
        i += 1
        activity = {}
        activity['id'] = int(row[0])
        activity['content'] = row[1]
        activity['description'] = row[2]
        records.append(activity)
        row = cursor.fetchone()

    data['records'] = records
    if i == 0:
        data['code'] = 'error'
        data['message'] = '暂无活动'
    else:
        data['code'] = 'success'
    return data


@app.route('/sort/getArticleBySort', methods=['GET'])
def getArticleBySort():
    id = int(request.values.get("id"))
    data = {}
    records = []
    sql = "SELECT Blog.user_id,publish_time,title,label,activity,name ,blog_id" \
          " FROM Blog,Activity " \
          " WHERE Blog.activity=Activity.activity_id AND activity=" + str(id) + " ORDER BY publish_time DESC"
    cursor.execute(sql)
    row = cursor.fetchone()
    i = 0
    while row:
        i += 1
        blog = {}
        blog['title'] = row[2]
        blog['author'] = row[0]
        blog['uid']=row[6]
        label_nums = row[3].split(",")
        blog_labels = []
        for label_num in label_nums:
            label = {}
            label['uid'] = label_num
            label['content'] = labels[label_num]
            blog_labels.append(label)
        blog['labels'] = blog_labels
        blogSort = {}
        blogSort['uid'] = row[4]
        blogSort['sortName'] = row[5]
        blog['blogSort'] = blogSort
        blog['time'] = row[1].strftime('%Y-%m-%d %H:%M:%S')
        records.append(blog)
        row = cursor.fetchone()

    data['records'] = records
    if i == 0:
        data['code'] = 'error'
        data['message'] = '此活动下暂无博客'
    else:
        data['code'] = 'success'

    return data


# 10.tag
@app.route('/tag/getTagList', methods=['GET'])
def getTagList():
    data = {'records': [
        {'id': '1', 'name': '科技'},
        {'id': '2', 'name': '新闻'},
        {'id': '3', 'name': '美食'},
        {'id': '4', 'name': '校园'},
        {'id': '5', 'name': '更多'},
    ], 'code': 'success'}
    return data


@app.route('/tag/getArticleByTagUid', methods=['GET'])
def getArticleByTagUid():
    tagUid = request.values.get("tagUid")
    sql = "SELECT title,Blog.user_id,label,activity,publish_time,name " \
          "FROM Blog,Activity " \
          "WHERE Blog.activity=Activity.activity_id " \
          "AND label LIKE \"%" + tagUid + "%\" " + \
          "ORDER BY publish_time DESC"
    cursor.execute(sql)
    row = cursor.fetchone()
    records = []
    i = 0
    while row:
        i += 1
        blog = {}
        blog['title'] = row[0]
        blog['author'] = row[1]
        blog_labels = []
        label_nums = row[2].split(",")
        for label_num in label_nums:
            label = {}
            label['uid'] = label_num
            label['content'] = labels[label_num]
            blog_labels.append(label)
        blog['labels'] = blog_labels
        blogSort = {}
        blogSort['uid'] = row[3]
        blogSort['sortName'] = row[5]
        blog['blogSort'] = blogSort
        blog['time'] = row[4].strftime('%Y-%m-%d %H:%M:%S')
        records.append(blog)
        row = cursor.fetchone()
    data = {}
    data['records'] = records
    if i == 0:
        data['code'] = 'error'
        data['message'] = '此标签下暂无博客'
    else:
        data['code'] = 'success'
    return data


# 11.admin
@app.route('/admin/workReport', methods=['POST'])
def workReport():
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    uid = data_json.get("uid")
    blog_id = data_json.get("blog_id")
    status = data_json.get("status")
    if status == 1:
        sql = 'UPDATE Report SET state=1 WHERE user_id="%s" AND blog_id=%d' % (uid, blog_id)
        cursor.execute(sql)
        sql = 'UPDATE Report SET state=1 WHERE blog_id=%d' % blog_id
        cursor.execute(sql)
    else:
        sql = 'UPDATE Report SET state=2 WHERE user_id="%s" AND blog_id=%d' % (uid, blog_id)
        cursor.execute(sql)
    data = {}
    data['code'] = 'success'
    updateUserInfo()
    return data


@app.route('/admin/getReportList')
def getReportList():
    data = {}
    records = []
    data["records"] = records
    user_id = user_info['user_id']
    sql = "select Report.user_id,Report.blog_id,Report.time,Report.reason,Report.state,Blog.title from Report,Blog where Report.state=0 AND Report.blog_id=Blog.blog_id";
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        record = {}
        record['uid'] = row[0]
        record['blog_id'] = row[1]
        record['time'] = row[2]
        record['reason'] = row[3]
        record['status'] = row[4]
        record['title'] = row[5]
        records.append(record)
        row = cursor.fetchone()

    data['code'] = 'success'
    data['message'] = '操作成功'
    return data


@app.route('/admin/getSortList')
def getActivityList():
    data = {}
    records = []
    data["records"] = records
    sql = "select * from Activity";
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        record = {}
        record['uid'] = row[0]
        record['sortName'] = row[2]
        record['startTime'] = row[3]
        record['endTime'] = row[4]
        record['credit'] = row[5]
        records.append(record)
        row = cursor.fetchone()

    data['code'] = 'success'
    return data


@app.route('/admin/blogSort/add',methods=['POST'])
def addBlogSort():
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    activityName = data_json.get("sortName")
    description = data_json.get("description")
    startTime = data_json.get("startTime")
    endTime = data_json.get("endTime")
    credit = int(data_json.get("credit"))
    data = {}
    records = []
    data["records"] = records
    user_id = user_info['user_id']
    sql = "select count(*) from Activity"
    cursor.execute(sql)
    num = cursor.fetchone()[0]+1
    sql='INSERT INTO Activity (activity_id,user_id,name,start_time,end_time,credit,description) VALUES (%d,"%s","%s","%s","%s",%d,"%s")'%(num,user_info['user_id'],activityName,startTime,endTime,credit,description)
    print(sql)
    cursor.execute(sql)
    row = cursor.fetchone()
    data['message'] = '添加活动成功'
    data['code'] = 'success'
    return data


@app.route('/login/login', methods=['POST'])
def LocalLogin():
    global user_info
    print("I am in loginAndLogin")
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    username = data_json.get("userName")
    password = data_json.get("passWord")
    print(username)
    print(password)
    sql = "SELECT * FROM Blog_user WHERE user_id = '%s' AND password = '%s' " % (username, password)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        results = cursor.fetchall()

    except:
        # 发生错误时回滚
        print('error')
        db.rollback()
    data = {}
    if len(results) == 0:
        data['code'] = 'error'
        data['message'] = '密码不正确'
    else:
        data['code'] = 'success'
        data['message'] = '登录成功'
        sql = "SELECT * FROM Blog_user WHERE user_id = '%s'" % username
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            user_info['user_id'] = row[0]
            user_info['name'] = row[1]
            user_info['password'] = row[2]
            user_info['email'] = row[3]
            user_info['credit'] = row[4]
            user_info['role'] = row[5]
            user_info['state'] = row[6]
            user_info['reputation'] = row[7]
        data['id'] = user_info.get('user_id')
        if int(user_info['reputation']) == 0:
            data['message'] = '你个烂人！'
            data['code'] = 'error'
    print("loginnn")
    print(user_info)
    data['records'] = user_info
    file_object = open("user_info.txt","w")
    json.dump(user_info,file_object)
    file_object.close()


    return data


@app.route('/login/register', methods=['POST'])
def localRegister():
    global user_info
    print("I am in registerAndregister")
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    username = data_json.get("userName")
    password = data_json.get("passWord")
    email = data_json.get("email")
    nickname = data_json.get("nickName")

    sql = "SELECT * FROM Blog_user WHERE user_id = '%s'" % username
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        results = cursor.fetchall()

    except:
        # 发生错误时回滚
        print('error')
        db.rollback()
    data = {}
    if len(results) == 0:
        data['code'] = 'success'
        data['message'] = '注册成功'
        sql = "INSERT INTO `blogs`.`Blog_user` (`user_id`, `name`, `password`, `email`, `credit`, `role`, `state`, `reputation`) VALUES ('%s', '%s', '%s', '%s', '100', '0', '1', '5');" % (
            username, nickname, password, email)
        cursor.execute(sql)
        sql = "SELECT * FROM Blog_user WHERE user_id = '%s'" % username
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            user_info['user_id'] = row[0]
            user_info['name'] = row[1]
            user_info['password'] = row[2]
            user_info['email'] = row[3]
            user_info['credit'] = row[4]
            user_info['role'] = row[5]
            user_info['state'] = row[6]
            user_info['reputation'] = row[7]
    else:
        data['code'] = 'error'
        data['message'] = '注册失败,该账号已被注册'

    sql = "SELECT * FROM Blog_user "
    cursor.execute(sql)
    return data


# 4.举报
@app.route('/api/reportBlog', methods=['GET'])
def ReportBlog():
    print("I AM IN ReportBlog!")
    id = int(request.values.get('uid'))
    content = str(request.values.get("reason"))
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO `blogs`.`Report` (`user_id`, `blog_id`, `time`, `reason`, `state`) VALUES ('%s', '%d', '%s', '%s', 0);" % (
        user_info['user_id'], id, time, content)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        comment = cursor.fetchall()
    except:
        print('error')
        db.rollback()
    data = {}
    data['code'] = 'success'
    data['message'] = '举报成功'
    return data


# 12 读取评论
@app.route('/web/comment/getList', methods=['POST'])
def GetCommentList():
    print("I AM IN GetCommentList!")
    datastr = str(request.data, 'utf-8')
    data_json = json.loads(datastr)
    id = int(data_json.get('blogUid'))
    records = []
    sql = "SELECT * FROM Comment WHERE blog_id='%d'" % id
    #   try:
    # 执行SQL语句
    cursor.execute(sql)
    comment = cursor.fetchall()
    for i in range(0, min(9, len(comment))):
        record = {}
        record['uid'] = int(i)
        record['createTime'] = comment[i][3].strftime("%Y-%m-%d %H:%M:%S")
        sql = "SELECT name FROM Blog_user WHERE user_id = '%s'" % comment[i][1]
        cursor.execute(sql)
        nname = cursor.fetchall()
        name = nname[0][0]
        user = {}
        user['id'] = comment[i][1]
        user['nickName'] = name
        record['user'] = user
        record['content'] = comment[i][4]
        records.append(record)
    data = {}
    data['code'] = 'success'
    data['records'] = records
    return data

@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/')
def welcome():
    return render_template("index.html")
# @app.route('/')
# def welcome():
#     return render_template("Welcome.html")

if __name__ == '__main__':
    app.run()
