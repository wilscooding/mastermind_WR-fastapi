import random
from typing import List, Tuple

class LocalRandomSecretProvider:
    def __init__(self, length: int = 4, min_num: int = 0, max_num: int= 9):
        self.length = length
        self.min_num = min_num
        self.max_num = max_num

    def generate_secret(self, length=None, min_num=None, max_num=None) -> Tuple[List[int], str]:
        length = length or self.length
        min_num = min_num if min_num is not None else self.min_num
        max_num = max_num if max_num is not None else self.max_num

        return [random.randint(min_num, max_num) for _ in range(length)], "fallback"