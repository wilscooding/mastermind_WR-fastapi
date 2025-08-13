# using random.org for true randomness
import httpx
from typing import List, Tuple


class RandomOrgSecretProvider:
    
    BASE_URL = "https://www.random.org/integers/"

    def __init__(self, length: int = 4, min_num: int = 0, max_num: int = 9, timeout: float = 2.0, retries: int = 3):
        self.length = length
        self.min_num = min_num
        self.max_num = max_num
        self.timeout = timeout
        self.retries = retries
    
    def generate_secret(self) -> Tuple[List[int], str]:
        params = {
            "num": self.length,
            "min": self.min_num,
            "max": self.max_num,
            "col": 1,
            "base": 10,
            "format": "plain",
            "rnd": "new"
        }

        try:

            reponse = httpx.get(self.BASE_URL, params=params, timeout=self.timeout)
            reponse.raise_for_status()
            numbers = list(map(int, reponse.text.strip().split()))
            code_str = ''.join(map(str, numbers))
            return numbers, code_str
        except httpx.RequestError as e:
            raise RuntimeError(f"Failed to fetch random numbers: {e}")
        

