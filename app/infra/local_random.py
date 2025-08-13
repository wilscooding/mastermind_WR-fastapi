import random
from typing import List, Tuple

class LocalRandomSecretProvider:
    def generate_secret(self, length: int = 4, min_num: int = 0, max_num: int = 9) -> Tuple[List[int], str]:
        numbers = [random.randint(min_num, max_num) for _ in range(length)]
        return numbers, "fallback"