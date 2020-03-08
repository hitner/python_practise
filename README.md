# my_python_practise


数据文件放在/var/www/rw 下面 都将所有权限改为777
静态文件 /var/www/static 下面

## ai2048
- 提供2048的初始化和移动操作
- 提供2种简单的自动移动策略


## 公共服务器

### long_poll 服务器
端口8801

### websocket_push 广播频道服务
通用频道，广播模式，不鉴权

### 全局推送服务器
tornado websocket 推送服务
global_push 端口 8803
，在线列表变化、好友邀请等从这里来

### 全局常规服务器（flask）
online 端口 8804
拉取消息、获得好友列表



## doudizhu
- 斗地主游戏状态机

## 全局约束

* 接口函数返回字典表示成功，返回其它（None、str）表示失败！这样的接口应该有一个统一的前缀
wi_ (表示web interface, 以便于以后替换tornado)


## 升级游戏概述

* 候机厅服务：提供组队功能
* 
