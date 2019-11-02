# websocket推送服务

端口8803

## 客户端接口

* ws://origin:8803/websocket/listen/FOO_BAR

    监听这个websocket，如果不存在，会在创建成功后失败，或者说get 的时候失败
    
## 内部接口

* /websocket/manager POST 新增一个websocket点
返回值
```buildoutcfg
{
    "rcode":0,
    "data":{
        "channel":"foo_bar"
    }
}
```

* /websocket/manager/FOO_BAR   一个接口的内部操作
    * DELETE 删除一个websocket
    * POST 广播一个消息
    * GET 获取元信息