# 候机厅服务
端口号 8810

应该是这样的概念吧，房间是公共的，然后会分配一个管理员，当管理员离开后，下一个人就自动成为管理员。
管理员的唯一的权限是可以踢人，加入房间和切换座位都是任意的；
跟踪和邀请：其实就是发房间号

因为没有数据库操作，以及需要数据加锁，所以用tornado是合适的


### doudizhu/waiting_rooms/ROOM_ID
- GET 获取所有房间内所有玩家,和基本信息
    * 返回值
    players:[0, 1000, 00, 0]
    websocket_address:""

### doudizhu/waiting_rooms/ROOM_ID/players
- POST 加入房间（自己加入自己的房间、接受邀请、跟踪好友房间都是此接口）?location=0-3 可以指定位置

### doudizhu/waiting_rooms/ROOM_ID/players/UID
- DELETE 离开房间 管理员离开后，下一个位置的人成为管理员，如果没有人了，该房间自动销毁
    
### doudizhu/waiting_rooms
 - POST 创建一个rooms ,并加入，自己就是管理员




