"""通用工具函数。"""

import random


# 随机种
def random_seed():
    return random.randint(1, 2 ** 31 - 1)
