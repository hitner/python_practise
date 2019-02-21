## long poll 服务

* longpoll
    - POST :创建一个服务session
    配置选项
    ```buildoutcfg
        session = '', //没有则自动生成唯一session
        dualChannel = 0, //是否有slave
        autoSeq = 0, //auto模式可不用传seq
              //auto模式适应用无中断和重新进入的情形
        cacheNum = 10, // cache的消息数
        autoRemoved = 1 // 是否自动移除
        silenceTick = 120, //自动移除的超时时间
        pollTimeout = 60, //poll的超时时间
    ```
    返回数据格式
    ```buildoutcfg
    {
        session:'foo',
        //所有其它选项
    }
    rcode = 1 //创建失败，session已存在
    rcode = 2 //其它错误
  
    ```

* longpoll/foo/msg
    - POST ？seq=1：没有seq，则为自动模式
    ```buildoutcfg
    {
      //data
    }
    ```
    - GET ?seq=1：获取该session消息

* longpoll/foo/sub-msg
    - dualChannel为1时才会有
    - POST ?seq=1 可以没有seq
    - GET ?seq=1

* longpoll/foo
    - GET 获得配置
    - DELETE 删除
    
    
* 关于内部业务服务器如何通信的问题，RPC调用？