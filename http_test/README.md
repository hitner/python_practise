# http_test 后端服务接口

服务器端口： 8800
文件存储路径：/opt/data/http_test/

路径前缀 /testsets/


# 接口
## /testsets/ 
* GET 获取所有测试set的列表
* POST 增加一个测试集，就会储存到文件 100_foobar.json

## /testsets/100
* GET 获取序号为100的测试集信息信息
* DELETE 删除该测试集
* PATCH 修改该测试集

## /testsets/100/interface/
* POST 新增一个接口

## /testsets/100/interface/2
* PUT 替换一个接口
* DELETE 删除一个接口