# 牌类通用设计

game.xiaoc100.com/shengji/rooms/110/players/1

出牌：/shengji/rooms/110/players/1/tracks    POST

对局中玩家状态: /shengji/rooms/110/players/1     GET

获得自己的牌和获得别人的牌又是不一样的。那么Restfull规范是通用的吗？

uid要怎样去做？ 就是每个game host都要维护一个 list 0-n 对应的uid

出牌：    shengji/rooms/110/do?action=ready/playcard/bid/overbid/pass/raise POST
托管:     shengji/rooms/110/sleep POST 托管 DELETE 取消托管
当前状态： shengji/rooms/110/status GET 就是针对我，应该知道的所有信息
离开房间： shengji/rooms/110/players DELETE 离开房间 POST 加入房间 GET获得玩家信息
历史信息： shengji/rooms/110/tracks GET 历史动作信息
长轮询：  shengji/rooms/110/actions GET long-poll操作

shengji/enlist GET 加入房间6秒超时时间，返回房间号，
shengji/myinfo GET 我的游戏数据
shengji/player/79348 GET 其它人的游戏数据
其它行为如何处理：

比方说聊天，送礼物，旁观等等，这应该是当独的房间信息，弄个websocket就可以了。这些跟聊天没有关系。


shengji/rooms/110/

获得对家的状态

游戏局通用
/shengji/rooms/110/poker 公开的牌类属性


几个玩家的状态列表

： tracks 出牌历史
： 当前状态（自己和公开）

游戏局应该也有唯一id，

托管的实现
* 超时托管？ 
* 杀进程托管
* 主动托管？ 

托管服务也是拉取到这些数据，发起这样的调用。

主动托管就让一个服务主动启动，如何判断超时？ 一个单独的服务去做这样一件事情。

相当于一个上帝视角，相当于有超时控制，和自动AI





# 高手升级

棋逢对手
