import httpx
from app.infra.random_org import RandomOrgSecretProvider
import pytest
import os

def test_generate_secret():
    provider = RandomOrgSecretProvider(length=4, min_num=0, max_num=9)
    secret, code_str = provider.generate_secret()
    
    assert len(secret) == 4
    assert all(0 <= num <= 9 for num in secret)
    assert isinstance(code_str, str)
    assert len(code_str) == 4
    assert all(char.isdigit() for char in code_str)