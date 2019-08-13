# 服务器分类

## 匹配服务器
端口 8803
匹配服务器的作用是客户端请求后，去读取其游戏信息，计算出排名值，然后参与到list中的排序，如果排序成功则，去游戏房间服务器创建一个房间，返回给匹配的人。这里的问题是，是
单线程：
    1，排序list不用加锁，但是有两个同步操作（判断登录信息/拉取战绩信息），

多线程：
    可以支持多处理，但是list要加锁，当然锁的操作还是小于访问数据库的操作。所以最好是这样实现。

玩家然后去加入游戏。

/doudizhu/createroom POST 私有接口，创建一个房间。通过这个接口也可以实现核心服务器的并发架构，简单的就是通过随机数，均衡的分布到不同的实例上去。

## 核心游戏服务器

端口 8804
只有判断登录的redis操作，所以可以使用tornador单线程，避免对内存游戏数据的加锁。

游戏结束时，将结果通过HTTP异步接口分发置结果服务器。由结果服务器存储至数据库。
只是POST该局游戏的统计信息登。
* /doudizhu/rooms/ROOMID/players  如果有变化，会有推送通知 event_players
    - GET获取房间内uid列表 
    - POST 加入房间 ，返回longpoll地址
    - DELETE 离开房间
* /doudizhu/rooms/ROOMID/ready   如果有变化，会有推送通知 event_ready
    - GET获取准备状态列表，
    - POST准备 
    - DELETE 取消准备
* /doudizhu/rooms/ROOMID/afk    如果有变化，会有推送通知 event_afk
    - GET 获取afk状态列表， 
    - POST 托管  
    - DELETE 取消托管
* /doudizhu/rooms/ROOMID/act?action=*** POST 玩牌动作
    - status 获取我的手牌
    - bid_landlord 叫地主
    - pass_landlord 不要地主
    - play 出牌
    - pass 不出
    - tracks 出牌历史记录


层级关系是
doudizhu_server  提供pool和给http的接口
doudizhu  提供完整的数据结构体
core_doudizhu 提供游戏最简结构体
doudizhu_match 只提供牌的大小判断
card 提供牌的通用表示

## 游戏历史、结果服务器（flask)

8805
提供内部和client的直接服务
如果这里提供游戏排名计算服务呢，那么匹配服务器就不需要任何具体的业务逻辑了，可以很方便的横向扩展。



