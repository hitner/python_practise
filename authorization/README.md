# 授权服务器

监听端口为 8802
Cookie的格式为（第一个对应uid0，第二个对应uid99999）
Set-Cookie: session="2|1:0|10:1565665993|7:session|32:MDpUSEVTRSBJUyBBIEZBS0UgVE9LRU4=|792658af486451ebb51082a06a453aa580f0e653c073bd2d376aa6ebdc29ec3d"; expires=Thu, 12 Sep 2019 03:13:13 GMT; Path=/

Set-Cookie: session=2|1:0|10:1565666279|7:session|40:OTk5OTk5OTk6VEhFU0UgSVMgQSBGQUtFIFRPS0VO|f54b94ccd6947c9ff746bba422964b3755c1450e7d1453f90c47b0b52c3c9ae7; expires=Thu, 12 Sep 2019 03:17:59 GMT; Path=/

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

