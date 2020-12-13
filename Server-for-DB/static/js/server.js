var http = require('http')   //获取对应的module
var fs = require('fs')
var url = require('url')
// var express=require('express')
// var port = process.argv[2]

// if(!port){
//   console.log('请指定端口号!例如: node server.js 8888')
//   process.exit(1)
// }
//
// var app=express()
// app.use(express.static('public'));
// //参数里为'/'则是默认打开页面
// app.get('/', function (req, res) {
//   res.sendFile( __dirname + "/" + "index.html" );
// })
//
// var server = app.listen(8080, function () {
//
//   var host = server.address().address
//   var port = server.address().port
//
//   console.log("应用实例，访问地址为 http://%s:%s", host, port)
//
// })

var server = http.createServer(function(request, response){
  var parsedUrl = url.parse(request.url, true)
  var pathWithQuery = request.url 
  var queryString = ''
  if(pathWithQuery.indexOf('?') >= 0){ queryString = pathWithQuery.substring(pathWithQuery.indexOf('?')) }
  var path = parsedUrl.pathname
  console.log(path);
  var query = parsedUrl.query
  var method = request.method

  console.log('含查询字符串的路径: ' + pathWithQuery + '\n请求方法为: ' + method)

  if(path === '/fresh'){
    if (request.headers.cookie) {
      let string = fs.readFileSync('./homepage.html', 'utf8')
      response.statusCode = 200
      response.writeHeader(200, {
        'Content-Type': 'text/plain;charset=utf-8',//不加这个会返回乱码，因为下面返回的数据是中文
        'Access-Control-Allow-Origin': 'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;1,400&family=Raleway:ital,wght@0,500;0,700;1,400;1,600&display=swap'
      })
      // let cookies = request.headers.cookie.split('; ')
      // let hash = {}
      // for (let i = 0; i < cookies.length; i++) {
      //   let parts = cookies[i].split('=')
      //   let key = parts[0]
      //   let value = parts[1]
      //   hash[key] = value
      // }
      // console.log(hash[0])
      response.write("seccessed");
      response.end()
      console.log("cookie exist")
    }
    else{
      let string = fs.readFileSync('./index.html', 'utf8')
      response.writeHeader(200, {
        'Content-Type': 'text/plain;charset=utf-8',//不加这个会返回乱码，因为下面返回的数据是中文
        'Access-Control-Allow-Origin': 'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;1,400&family=Raleway:ital,wght@0,500;0,700;1,400;1,600&display=swap'
      })
      response.write("Not Found")
      response.end()
    }
      //存在cookie
      // let cookies = request.headers.cookie.split('; ')
      // let hash = {}
      // for (let i = 0; i < cookies.length; i++) {
      //   let parts = cookies[i].split('=')
      //   let key = parts[0]
      //   let value = parts[1]
      //   hash[key] = value
      // }
      // let email = hash.sign_in_email
      // let users = fs.readFileSync('./db/users', 'utf8')
      // //JSON.parse()必须解析有效的JSON对象, 否则报错.
      // try {
      //   users = JSON.parse(users)
      // } catch(exception) {
      //   users = []
      // }
      // let foundUser
      // for (let i = 0; i < users.length; i++) {
      //   if (users[i].email === email) {
      //     foundUser = users[i]
      //     break
      //   }
      // }
      // if (foundUser) {
    //     string = string.replace('__user__', foundUser.email)
    //   }
    // } else {
    //  string = string.replace('__user__', '同学')
    // }
  } else if(path === '/sign_up' && method === 'GET'){ 
    let string = fs.readFileSync('./sign_up.html', 'utf8')
    response.statusCode = 200
    response.setHeader('Content-Type', 'text/html;charset=utf-8')
    response.write(string)
    response.end()
  } else if (path === '/sign_up' && method === 'POST') {
    readBody(request).then((body)=>{
      console.log('请求体body为: '+decodeURIComponent(body))
      let strings = body.split('&')
      let hash={} //hash存储key-value值
      strings.forEach((string)=>{
        let parts = string.split('=')
        let key = parts[0]
        let value = parts[1]
        hash[key] = decodeURIComponent(value)
      })
      let {name,email, password, password_confirmation} = hash
      
      if (email.indexOf('@') === -1) {
        response.writeHeader(200, {
          'Content-Type': 'text/plain;charset=utf-8',//不加这个会返回乱码，因为下面返回的数据是中文
          'Access-Control-Allow-Origin': 'http://localhost:62732'
        })
        response.write("invalid")
      } else if (password !== password_confirmation) {
        //密码一致性
        response.writeHeader(200, {
          'Content-Type': 'text/plain;charset=utf-8',//不加这个会返回乱码，因为下面返回的数据是中文
          'Access-Control-Allow-Origin': 'http://localhost:62732'
        })
        response.write("not match")
      } else {
        var users = fs.readFileSync('./db/users', 'utf8')
        
        try {
          users = JSON.parse(users)
        } catch(exception) {
          users = []
        }
        let inUse = false
        for (let i = 0; i < users.length; i++) {
          let user = users[i]
          if (user.email === email) {
            inUse =  true
            break;
          }
        }
        if (inUse) {
          console.log('此用户已注册, 请重新输入\n')
          response.writeHeader(200, {
            'Content-Type': 'text/plain;charset=utf-8',//不加这个会返回乱码，因为下面返回的数据是中文
            'Access-Control-Allow-Origin': 'http://localhost:62732'
          })
          response.write("used")
        } else {
          users.push({email: email, password: password})
          var usersString = JSON.stringify(users)
          fs.writeFileSync('./db/users', usersString)
          console.log('写入数据库, 用户注册成功\n')
          response.statusCode = 200
          response.writeHeader(200, {
            'Content-Type': 'text/plain;charset=utf-8',//不加这个会返回乱码，因为下面返回的数据是中文
            'Access-Control-Allow-Origin': 'http://localhost:62732'
          })
          response.write("successed")
        }
      }
      response.end()
    })
  } else if (path === '/sign_in' && method === 'GET') {
    let string = fs.readFileSync('./index.html', 'utf8')
    response.statusCode = 200
    response.setHeader('Content-Type', 'text/html;charset=utf-8')
    response.write(string)
    response.end()
  } else if (path === '/sign_in' && method === "POST") {
    readBody(request).then((body)=>{
      console.log('请求体body为: '+decodeURIComponent(body))
      let strings = body.split('&')
      let hash={} //hash存储key-value值
      strings.forEach((string)=>{
        let parts = string.split('=')
        let key = parts[0]
        let value = parts[1]
        hash[key] = decodeURIComponent(value)
      })
      let {email, password} = hash
      var users = fs.readFileSync('./db/users', 'utf8')
      try {
        users = JSON.parse(users)
      } catch(exception) {
        users = []
      }
      let found = false
      for (let i = 0; i < users.length; i++) {
        if (users[i].email === email && users[i].password === password) {
          found = true
          break
        }
      }
      if (found) {
        
        response.writeHeader(200, {
          // 'Set-Cookie': 'sign_in_email=${email}',//不加这个会返回乱码，因为下面返回的数据是中文
          'Content-Type': 'text/plain;charset=utf-8',
          'Access-Control-Allow-Origin': 'http://localhost:62732'
        })
        response.write("successed,"+email)
        // response.setHeader('Set-Cookie', `sign_in_email=${email}`)
        console.log('设置cookie')
        // response.statusCode = 200
      } else {
        response.writeHeader(200, {
          'Content-Type': 'text/plain;charset=utf-8',//不加这个会返回乱码，因为下面返回的数据是中文
          'Access-Control-Allow-Origin': 'http://localhost:62732'
        })
        response.write("Fail")
      }
      response.end()
    })
  }
  else {
    fs.readFile('.'+request.url,function (err,data){
      if(!err){
        response.end(data)
      }
    })
  }

})

function readBody(request) {
  return new Promise((resolve, reject)=>{
    let body = [] //请求体
    request.on('data', (chunk)=>{
      console.log('服务器正在接收请求体')
      // 监听data事件
      body.push(chunk);
    }).on('end', ()=>{
      // 监听end事件, 当服务器接收POST请求中的全部数据触发
      console.log('服务器接收完毕请求体')
      body = Buffer.concat(body).toString();
      resolve(body)
    })
  })
}

server.listen(8080)
console.log('监听 ' + 8080 + ' 成功\n请在浏览器打开 http://localhost:' + 8080 + '\n')

