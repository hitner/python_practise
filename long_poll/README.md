## long poll 服务
端口8801

* longpoll/
    - POST :创建一个服务channel
    配置选项
    ```buildoutcfg
        cacheSize = 10, // cache的消息数
        autoRemove = 1 // 是否自动移除
        removeTimeout = 120, //自动移除的超时时间
        pollTimeout = 60, //poll的超时时间
    ```
    返回数据格式
    ```buildoutcfg
    {
        channel:'foo',
        //所有其它选项
    }
    rcode = 1 //创建失败
  
    ```

* longpoll/foo/message
    - POST ？seq=1：没有seq，则为自动模式 内部接口、屏蔽外部访问（seq的含义为该消息的编号）
    //auto模式适应用无中断和重新进入的情形
                     //非auto主要用于主机需要知道当前状态对应于哪个msg
    ```buildoutcfg
    {
      //data
    }
    ```
    - GET ?seq=1：获取该session消息（seq的含义为，请求编号为seq的消息，及以后的消息）
                     
* longpoll/foo
    - GET 获得配置
    - DELETE 删除
    
    
* 关于内部业务服务器如何通信的问题，gRPC调用。或者先用简单的http 协议