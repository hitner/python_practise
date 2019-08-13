# 授权服务器

监听端口为
Cookie的格式为

即Cookie_Name为session，

## 登录

* /auth/login POST Body内的格式为
{
    "uid":12332323,
    "token":"FDSkkkkkk", //先md5再sha1
}

返回就是设置一个Cookie


## 登出

* /auth/logout POST

