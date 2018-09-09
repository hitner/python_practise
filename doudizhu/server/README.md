# 斗地主web server

- 使用tornado long polling 方案
- 消息格式
```
	statusId
	stage: // 0:未开始 1：叫分阶段 2：出牌阶段
	action: {
		 player: 
		 cards:
		 cd:
	}
```
	* 由未开始到叫分阶段时，每个player区请求自己的游戏状态
	* 游戏结束由client自己判断（手牌数为0)
- 出牌/不出操作 post，需带上上一个正确的statusId, 有效出牌才进入下一个status
- GET 全局游戏状态
```
	statusId:
	stage:
	turn: //改谁出牌了
	cardsRemain:[] //下两家的剩余牌数
	myCards: [] //我的牌
	publicCards:[] //公共牌 stage == 2时才有

``` 
