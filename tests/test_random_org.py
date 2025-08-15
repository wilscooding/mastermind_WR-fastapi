import httpx
from app.infra.random_org import RandomOrgSecretProvider
import types
import pytest
import os


class DummyResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise httpx.HTTPStatusError("Error", request=None, response=None)

def test_random_org_provider_returns_label(monkeypatch):
    # Arrange: fake API returns "1\n2\n3\n4\n"
    def fake_get(url, params=None, timeout=None):
        return DummyResponse("1\n2\n3\n4\n")

    monkeypatch.setattr(httpx, "get", fake_get)

    provider = RandomOrgSecretProvider(length=4, min_num=0, max_num=9)

    # Act
    numbers, label = provider.generate_secret()

    # Assert
    assert numbers == [1, 2, 3, 4]
    assert label == "random_org"


def test_generate_secret():
    provider = RandomOrgSecretProvider(length=4, min_num=0, max_num=9)
    secret, code_str = provider.generate_secret()
    
    assert len(secret) == 4
    assert all(0 <= num <= 9 for num in secret)
    assert isinstance(code_str, str)
    assert code_str == "random_org"

def test_random_org_provider_easy_mode(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        return DummyResponse("7\n8\n9\n")

    monkeypatch.setattr(httpx, "get", fake_get)

    provider = RandomOrgSecretProvider(length=3)
    secret, label = provider.generate_secret()

    assert secret == [7, 8, 9]
    assert label == "random_org"    

def test_random_org_provider_hard_mode(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        return DummyResponse("0\n1\n2\n3\n4\n")

    monkeypatch.setattr(httpx, "get", fake_get)

    provider = RandomOrgSecretProvider(length=5)
    secret, label = provider.generate_secret()

    assert secret == [0, 1, 2, 3, 4]
    assert label == "random_org"
    