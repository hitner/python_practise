# 斗地主

## 状态机存储

- 房间管理器

| 字段名 |类型 | 说明 |
| --- | --- | --- |
| cursor | int | 光标,数据发送改变就自增 从1开始 |


- 游戏状态机


| 字段名 |类型 | 说明 |
| --- | --- | --- |
| stage | int | 游戏状态<br>0 未开始 1 叫地主阶段 2出牌阶段 |
| playerHand | array | 每个玩家的牌 |
| bottomCards | array | 三张底牌 |
| master | int | 地主编号[ 0 1 2 ] |
| playingTrack | array | 之前出牌 |
| deadwood | array | 已经出过的牌的合集，用于下次洗牌和发牌 |

* 出牌的结构体 

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| player | int | |
| cards | array | |
| pattern | int | |
| weight | int | |
 
    
* 重要方法
    * get_current_index()
    * pre_cd() 获取要跟的牌型（因为有不要的存在），pattern0表示可以重新出牌
    


## web server
- 错误码
    * 100 参数错误
    * 110 不在此房间
    * 120 比赛未开始
    * 121 无效出牌
- 使用tornado long polling 方案
- pollchanges 返回的消息格式

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| cursor | int | 类似于消息id，房间内自增 |
| eventType |int | 事件类型 |
| eventContent | struct | 事件内容 |

- 开始叫地主事件 100

收到该事件时，去获取自己的牌，开始抢地主 eventContent为空

- 确定地主事件 110

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| bottomCards | string | 游戏底牌 |
| master | int | 地主编号 |

- 出牌事件 111
    - 事件内容为出牌结构体

	- 其它说明：
	    游戏结束由client自己判断（手牌数为0)

- getmycards 获取玩家私有游戏状态 (进房间成功后调用，获得cursor)

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| cursor | int | id |
| stage | int | 0 未开始(0时只返回stage) <br> 1 叫地主阶段<br>2 出牌阶段 |
| cardsRemain| array | 所有玩家剩余的牌数 |
| myCards | array | 我的牌
| myIndex | int | 我的游戏编号
| master | int | stage == 2 时才有 地主
| bottomCards | int | stage == 2时才有 公共牌
| playingTrack | array |stage == 2 时 <br> 只返回最后两次出牌的操作<br>（若支持记牌器或机器AI，则返回所有的出牌历史）

- React 的state状态
除了上述getmycards里面的之外还有 一个choosedCard


- dealcard 出牌


- askformaster 叫地主
    * 目前的策略是先到先得
    


# 包牌

## 状态核心

* 核心

| 字段名 |类型 | 说明 |
| --- | --- | --- |
| stage | int | 0 未开始 <br> 1 叫分阶段 <br> 2 出牌阶段 | 
| playerHand | array | 四个人手上的牌 |
| bidList | array | 叫分列表，最后一个是trumpMaker <br> {player, point} |
| trumpSuit | int | 主牌花色 |
| bottoms | array | 底牌 |
| replacedBottoms | array | 置换的底牌 |
| picked | array | 已上分的列表 |
| playingTrack | array | 出牌列表 |

* 一次出牌

| 字段名 |类型 | 说明 |
| --- | --- | --- |
| player | int | 玩家编号（略微的冗余设计）
| cards | array | 牌面 |
| suit | int | 3种副牌和花色 和无花色的弃牌 |
| pattern | int | 单牌、对子、连队 这几种类型 |
| weight | int | 权值，比较大小 |
