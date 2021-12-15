import pytest
from brownie import accounts, exceptions

amount_minted = 2
price = 1000000000000000
fee = amount_minted * price


@pytest.mark.statechange
def test_state_change(token, test_account):
    token.saleStateChange({"from": test_account})
    assert token.saleOpen() == True
    token.saleStateChange({"from": test_account})
    assert token.saleOpen() == False


@pytest.mark.getmintlimit
def test_get_sale_mint_limit(token, test_account):
    assert token.getMintLimit() == 15


@pytest.mark.salelimit
def test_set_sale_mint_limit(token, test_account):
    mint_limit = 100
    assert token.getMintLimit() == 15
    token.setMintLimit(mint_limit, {"from": test_account})
    assert token.getMintLimit() == mint_limit


@pytest.mark.notstartedsale
def test_cant_mint_unless_sale_started(token, test_account):
    with pytest.raises(exceptions.VirtualMachineError):
        token.createToken(amount_minted, {"from": test_account, "value": fee})


@pytest.mark.totalsupply
def test_total_supply(token, test_account):
    token.saleStateChange({"from": test_account})
    token.createToken(amount_minted, {"from": test_account, "value": fee})
    assert token.totalSupply() == amount_minted


@pytest.mark.mintsale
def test_create_token_sale(token, test_account):
    token.saleStateChange({"from": test_account})
    account_starting_balance = test_account.balance()
    contract_starting_balance = token.balance()
    assert token.totalSupply() == 0
    token.createToken(amount_minted, {"from": test_account, "value": fee})
    assert token.totalSupply() == amount_minted
    assert token.balanceOf(test_account) == amount_minted
    token.createToken(1, {"from": test_account, "value": fee / 2})
    assert token.totalSupply() == amount_minted + 1
    assert token.balanceOf(test_account) == 3
    assert test_account.balance() == account_starting_balance - 1.5 * fee
    assert token.balance() == contract_starting_balance + 1.5 * fee


@pytest.mark.gettokenprice
def test_get_token_price(token):
    assert token.getTokenPrice() == 1000000000000000


@pytest.mark.settokenprice
def test_set_token_price(token, test_account):
    token.setTokenPrice(2000000000000000, {"from": test_account})
    assert token.getTokenPrice() == 2000000000000000


@pytest.mark.reserve
def test_reserve_tokens(token, test_account):
    token.reserveTokens(test_account, 10, {"from": test_account})
    assert token.balanceOf(test_account) == 10

