# 候机厅服务
端口号 8810

每个人都有自己的候机厅，在多人匹配中，如果房主离开了，就把房间解散？
这样好像比较简单一点？

唯一的权限控制是房主可以踢人，加入房间和切换座位都是任意的；
房主退出后，房间解散

跟踪和邀请：其实就是发房间号

所以根本上就是
离开：

## doudizhu/waiting_rooms/ROOM_ID/players
    
- GET 获取所有房间内所有玩家,和基本信息
    * 返回值
    players:[0, 1000, 00, 0]
    websocket_address:""
    
- POST 加入房间（自己加入自己的房间、接受邀请、跟踪好友房间都是此接口）?location=0-3 可以指定位置

* doudizhu/waiting_rooms/ROOM_ID/players/UID
    - DELETE 离开房间 主人离开后，房间自动销毁 (如果uid是别人就是房主踢人！)
    
* doudizhu/waiting_rooms/myroom
    - POST 创建我的房间
    - DELETE 离开我的房间




