
# 牌的通用表示法
包括三个部分 程序内部表示 手写输入表示法 、 命令行展示方法

## 内部表示法

一个字节（8bit）表示一张牌
最高两位表示花色，后六位表示牌型
* 花色
    - 00 方块 （如果要去掉花色，可以全部变为00）
    - 01 梅花
    - 10 红桃
    - 11 黑桃
    
* 牌型
小王 01 0000 （高两位为00）
大王 10 0000

2  2    0010
3  3    0011
...
10 10   1010
J  11
Q  12
K  13
A  14   1110

* 0 1 15 禁用
## 手写输入表示法

2个ASCII字符来表示

s 黑桃 splade
h 红桃 heart
c 梅花 club
d 方块 diamond

s2  ... s0 sJ sQ sK sA

!V 小王   !W 大王

## 命令行展示法

与手写输入法类似，只是花色用字符'♦', '♣', '♥', '♠'来表示

## python中展示

若不加特定说明，全部为bytearray

## 传输编码
有两种，base16 或者 base64，为了简单起见，还是之间base16 节约多少?
base64可以节省3分之一的字节？平时出牌都很简单，所以还是用base16吧


# 牌类通用接口设计
GAME  ROOM_ID

## 房间外操作
GAME/enlist GET 加入房间6秒超时时间，返回房间号，
GAME/myinfo GET 我的游戏战绩数据
GAME/player/79348 GET 其它人的游戏数据

## 房间内操作
自己的uid从自己的cookie中拿
### 属于玩牌的操作
-  GAME/rooms/ROOM_ID/act?action=ACTION POST
    * ACTION 的值有
    status 从我的视角出发的牌全局描述
    tracks 前面的出牌记录
    play 出牌
    bid  叫牌
    overbid 反牌
    pass 不出
    raise

### 其它房间内操作
- 房间玩家： GAME/rooms/ROOM_ID/players DELETE 离开房间 POST 加入房间 GET获得玩家信息
- 托管:     GAME/rooms/ROOM_ID/afk POST 托管 DELETE 取消托管 GET 获取托管状态
- 准备  GAME/rooms/ROOM_ID/ready
