# 斗地主

## 状态机存储

- 游戏内容存储格式
```
    cursor ：光标
    stage ： 游戏状态 0 未开始 1 叫地主阶段 3出牌阶段 （因为2用来做事件通知了！）
    players[3] : 每个玩家的牌
    back_3 : 三张底牌
    master : 地主编号
    pre_deals[] : 之前出的牌
        {
            actor cards pattern weight
        }
    
    可选缓存
    cards_pool : 已经出过的牌的合集，用于下次洗牌和发牌
    
    重要方法
    get_current_index()
    pre_cd() 获取要跟的牌型（因为有不要的存在），pattern0表示可以重新出牌
    
```

## web server

- 使用tornado long polling 方案
- pollchanges 返回的消息格式
```
	cursor : 类似于消息id，房间内自增
	stage : 0 游戏未开始 1 叫地主阶段（在收到此阶段消息后，获取自己的私有游戏状态）
	        2 xx叫地主成功
	back_3 游戏底牌
	master 地主编号
	        3 出牌阶段
	actor : 0-2表示出牌的玩家
	cards : 出的牌
	pattern : 该牌的类型 0 表示不出
	weight : 该牌的权值
	
```
	
	其它说明：
	    游戏结束由client自己判断（手牌数为0)

- getmycards 获取玩家私有游戏状态
```
	cursor:
	stage: 0 未开始 1 叫地主阶段 3出牌阶段
	cardsRemain[]: 所有玩家剩余的牌数
	myCards:  我的牌
	back_3: 公共牌 stage == 3时才有
	pre_deals[] : 只返回最后两次出牌的操作，（若支持记牌器或机器AI，则返回所有的出牌历史）
	    { actor cards pattern weight }

``` 


- dealcard 出牌


- askformaster 叫地主
    * 目前的策略是先到先得