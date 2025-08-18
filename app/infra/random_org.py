import httpx
from typing import List, Tuple

"""Random.org-based secret provider implementation (for production randomness)."""



class RandomOrgSecretProvider:
    
    BASE_URL = "https://www.random.org/integers/"

    def __init__(self, length: int = 4, min_num: int = 0, max_num: int = 9, timeout: float = 2.0, retries: int = 3):
        self.length = length
        self.min_num = min_num
        self.max_num = max_num
        self.timeout = timeout
        self.retries = retries
    
    def generate_secret(self, length=None, min_num=None, max_num=None) -> Tuple[List[int], str]:
        length = length or self.length
        min_num = min_num if min_num is not None else self.min_num
        max_num = max_num if max_num is not None else self.max_num

        params = {
            "num": length,
            "min": min_num,
            "max": max_num,
            "col": 1,
            "base": 10,
            "format": "plain",
            "rnd": "new"
        }

        response = httpx.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()
        numbers = list(map(int, response.text.strip().split()))
        return numbers, "random_org"
    
    
