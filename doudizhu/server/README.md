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

- 出牌/不出操作 post，需带上上一个正确的statusId, 有效出牌才进入下一个status
