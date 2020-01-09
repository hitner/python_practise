"""升级引擎
    一把完整的牌的游戏过程
- 依赖
    shengji_core_foundation
- 原理

- 备注
    把洗牌功能挪到外面去。自己不需要提供这样的功能。

"""

class ShengjiEngine:
    def __init__(self):
        self.host_index = -1

    def reset(self):
        self.host_index = -1

