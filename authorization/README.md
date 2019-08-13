# 授权服务器

监听端口为 8802
Cookie的格式为 f'{uid}:{token}'（第一个对应uid0，第二个对应uid99999）
Set-Cookie: session="2|1:0|10:1565667400|7:session|32:MDpUSEVTRSBJUyBBIEZBS0UgVE9LRU4=|9219dc4d00f6b49916cbf4ab720414c03a59d154c0d4c02ea6df242a32f9acca"; expires=Thu, 12 Sep 2019 03:36:40 GMT; Path=/

Cookie: session="2|1:0|10:1565667400|7:session|32:MDpUSEVTRSBJUyBBIEZBS0UgVE9LRU4=|9219dc4d00f6b49916cbf4ab720414c03a59d154c0d4c02ea6df242a32f9acca"

使用了对称加密方法来隐藏


即Cookie_Name为session，

## 登录

* /auth/login POST Body内的格式为(注意uid不能为0)
{
    "uid":12332323,
    "password":"FDSkkkkkk", //先md5再sha1
}

返回就是设置一个Cookie


## 登出

* /auth/logout POST

