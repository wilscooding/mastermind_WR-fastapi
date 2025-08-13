from typing import List, Tuple

class CombinedSecretProvider:
    def __init__(self, primary, fallback):
        self.primary = primary
        self.fallback = fallback
    
    def generate_secret(self, length: int = 4, min_num: int = 0, max_num: int = 9) -> Tuple[List[int], str]:
        try:
            return self.primary.generate_secret(length, min_num, max_num)
        except Exception as e:
            return self.fallback.generate_secret(length, min_num, max_num)
        