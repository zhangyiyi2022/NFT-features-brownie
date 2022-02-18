import pytest

token_uri = "INSERT TOKENURI HERE"
contract_uri = "INSERT CONTRACTURI HERE"


@pytest.fixture(scope="module")
def token(ERC721Custom, accounts):
    return ERC721Custom.deploy(token_uri, contract_uri, {"from": accounts[0]})


@pytest.fixture(scope="module")
def test_account(accounts):
    return accounts[0]
