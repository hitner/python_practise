# 服务器分类

* 候机室服务器 doudizhu_waiting_room 

## 匹配服务器
doudizhu_match 端口 8811

* */doudizhu/match POST 由候机室服务器调用*
    - JSON BODY: players:[111,0,2222,0]

匹配服务器的作用是客户端请求后，去读取其游戏信息，计算出排名值，然后参与到list中的排序，如果排序成功则，去游戏房间服务器创建一个房间，返回给匹配的人。这里的问题是，是
单线程：
    1，排序list不用加锁，但是有两个同步操作（判断登录信息/拉取战绩信息），

多线程：
    可以支持多处理，但是list要加锁，当然锁的操作还是小于访问数据库的操作。所以最好是这样实现。

玩家然后去加入游戏。

/doudizhu/createroom POST 私有接口，创建一个房间。通过这个接口也可以实现核心服务器的并发架构，简单的就是通过随机数，均衡的分布到不同的实例上去。

## 游戏历史、结果服务器（flask)
doudizhu_record 端口 8812
提供内部和client的直接服务 ，提供匹配值计算等服务
如果这里提供游戏排名计算服务呢，那么匹配服务器就不需要任何具体的业务逻辑了，可以很方便的横向扩展。

## 核心游戏服务器
doudizhu 端口 8813
只有判断登录的redis操作，所以可以使用tornador单线程，避免对内存游戏数据的加锁。

游戏结束时，将结果通过HTTP异步接口分发置结果服务器。由结果服务器存储至数据库。


层级关系是
doudizhu_server  提供pool和给http的接口
doudizhu  提供完整的数据结构体
core_doudizhu 提供游戏最简结构体
doudizhu_match 只提供牌的大小判断
card 提供牌的通用表示


只是POST该局游戏的统计信息登。
* /doudizhu/rooms/ROOMID/players  如果有变化，会有推送通知 event_players （离开房间有托管动作）
    - GET获取房间内uid列表 
    - DELETE 离开房间
* /doudizhu/rooms/ROOMID/ready   如果有变化，会有推送通知 event_ready
    - GET获取准备状态列表，
    - POST准备 
    - DELETE 取消准备
* /doudizhu/rooms/ROOMID/afk    如果有变化，会有推送通知 event_afk
    - GET 获取afk状态列表， 
    - POST 托管
    - DELETE 取消托管
* /doudizhu/rooms/ROOMID/act?action=*** POST 玩牌动作 （有对应托管动作）
    - fapai  服务器根据时间点，返回列表中的三段["kkk","AAA","222"],客户端在每段快结束的时候去请求新的发牌列表，以保证动画的连续。（服务器根据第一次牌生成的时间节点来返回对应段数，防止提前知道所有的牌）
    - status 获取我的手牌 （发牌阶段，不会返回手牌）
    - bid_landlord 叫地主
    - pass_landlord 不要地主
    - play 出牌
    - pass 不出
    - tracks 出牌历史记录

* */doudizhu/rooms/create POST 由匹配服务器调用*
    - JSON BODY: players:[111,0,2222,0]。所以就没有加入游戏这个过程，如果一局游戏结束后，有人没有准备，就开始倒计时，倒计时到就剔出房间
    - return: 返回房间id，玩家列表，房间属性（longpoll地址），同时调起托管ai。客户端收到之后，请求手牌
    所有人准备之后，如果人齐直接在本房间开始，如果人不齐，则重现加入匹配服务器去匹配

* */doudizhu/rooms/ROOMID/ai/UID?action=___ POST 由托管服务器调用*

    action除了act里面的定义外，还有leave

## 托管服务器

doudizhu_ai 端口8814

* */doudizhu/ai/rooms POST 由核心服务器调用*
    - 告知ai服务器开始监听ROOMID里面的所有事件
通过long_poll 和get_status 储存每个玩家视角的手牌，设置定时器，定时器到了之后就


