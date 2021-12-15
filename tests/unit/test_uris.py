import pytest
from brownie import exceptions

amount_minted = 2
price = 1000000000000000
fee = amount_minted * price

contract_uri = "CONTRACTURI HERE"
updated_contract_uri = "NEW CONTRACTURI HERE"
token_uri = "NOT REVEALED URI HERE"
updated_uri = "UPDATED NOT REVEALED URI HERE"
base_uri = "REVEALED URI HERE"


@pytest.mark.contracturi
def test_initial_contracturi(token):
    assert token._contractURI() == contract_uri


@pytest.mark.setcontracturi
def test_set_contracturi(token, test_account):
    token.setContractURI(updated_contract_uri, {"from": test_account})
    assert token._contractURI() == updated_contract_uri


@pytest.mark.notrevealeduri
def test_initial_notrevealeduri(token, test_account):
    token.presaleStateChange({"from": test_account})
    token.addToWhiteList([test_account.address], {"from": test_account})
    token.createTokenPresale(amount_minted, {"from": test_account, "value": fee})
    assert token.tokenURI(1) == token_uri


@pytest.mark.setnotrevealeduri
def test_set_notrevealeduri(token, test_account):
    token.presaleStateChange({"from": test_account})
    token.addToWhiteList([test_account.address], {"from": test_account})
    token.createTokenPresale(amount_minted, {"from": test_account, "value": fee})
    token.setNotRevealedURI(updated_uri, {"from": test_account})
    assert token.tokenURI(1) == updated_uri


@pytest.mark.revealuri
def test_reveal(token, test_account):
    token.reveal({"from": test_account})
    assert token.revealed() == True


@pytest.mark.setbaseuri
def test_set_baseuri(token, test_account):
    token.presaleStateChange({"from": test_account})
    token.addToWhiteList([test_account.address], {"from": test_account})
    token.createTokenPresale(amount_minted, {"from": test_account, "value": fee})
    token.setBaseURI(base_uri, {"from": test_account})
    token.reveal({"from": test_account})
    assert token.tokenURI(1) == base_uri + "1.json"
    assert token.tokenURI(2) == base_uri + "2.json"


@pytest.mark.notokenuri
def no_token_uri(token):
    with pytest.raises(exceptions.VirtualMachineError):
        token.tokenURI(1)
