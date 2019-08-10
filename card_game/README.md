
# 牌的通用表示法
包括三哥部分 程序内部表示 手写输入表示法 、 命令行展示输入法

## 内部表示法

一个字节（8bit）表示一张牌
最高两位表示花色，后六位表示牌型
* 花色
    - 00 方块 （如果要去掉花色，可以全部变为00）
    - 01 梅花
    - 10 红桃
    - 11 黑桃
    
* 牌型
小王 01 0000
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

d 方块 diamond
c 梅花 club
h 红桃 heart
s 黑桃 splade

s2  ... s0 sJ sQ sK sA

!V 小王   !W 大王

## 命令行展示法


前端表示法

## 传输编码
有两种，base16 或者 base64，为了简单起见，还是之间base16 节约多少?
base64可以节省3分之一的字节？平时出牌都很简单，所以还是用base16吧










传输编码 必须要字符串化，可以base64！


逻辑处理表示法：这个就依据不同的牌，有不同的做法了

比方说 斗地主的时候 2 可以安排成15，应该留给最后的函数
但是在升级里面， 就是 单独判断了
"""