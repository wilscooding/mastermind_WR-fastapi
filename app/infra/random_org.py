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

        last_exception = None
        for _ in range(self.retries + 1):
            try:
                response = httpx.get(self.BASE_URL, params=params, timeout=self.timeout)
                response.raise_for_status()
                numbers = [int(x) for x in response.text.strip().split()]
                if len(numbers) != self.length:
                    raise ValueError(f"Random.org returned {len(numbers)} numbers, expected {self.length}")
                if any(n < self.min_num or n > self.max_num for n in numbers):
                    raise ValueError("Random.org returned out-of-range digits")
                # ✅ Always return "random_org" label
                return numbers, "random_org"
            except Exception as e:
                last_exception = e

        raise RuntimeError(f"Failed to fetch random numbers from Random.org: {last_exception}")