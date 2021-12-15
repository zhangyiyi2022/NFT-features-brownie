import pytest
from brownie import accounts, exceptions

whitelist_addresses = ["0xasdfdsfa", "0xdasfasdfsadsa"]

amount_minted = 2
price = 1000000000000000
fee = amount_minted * price


@pytest.mark.state
def test_presale_state_change(token, test_account):
    token.presaleStateChange({"from": test_account})
    assert token.presaleOpen() == True
    token.presaleStateChange({"from": test_account})
    assert token.presaleOpen() == False


@pytest.mark.presalelimit
def test_set_presale_mint_limit(token, test_account):
    mint_limit = 10
    assert token.presaleMintLimit() == 5
    token.setPresaleMintLimit(mint_limit, {"from": test_account})
    assert token.presaleMintLimit() == mint_limit


@pytest.mark.whitelist
def test_add_to_whitelist(token, test_account):
    assert token.isOnWhiteList(test_account) == False
    token.addToWhiteList([test_account.address, accounts[1]], {"from": test_account})
    assert token.isOnWhiteList(test_account) == True
    assert token.isOnWhiteList(accounts[1]) == True


@pytest.mark.notstarted
def test_cant_mint_unless_presale_started(token, test_account):
    with pytest.raises(exceptions.VirtualMachineError):
        token.createTokenPresale(amount_minted, {"from": test_account, "value": fee})


@pytest.mark.notonwhitelist
def test_cant_mint_unless_on_whitelist(token, test_account):
    token.presaleStateChange({"from": test_account})
    with pytest.raises(exceptions.VirtualMachineError):
        token.createTokenPresale(amount_minted, {"from": test_account, "value": fee})


@pytest.mark.mintpresale
def test_create_token_presale(token, test_account):
    token.presaleStateChange({"from": test_account})
    token.addToWhiteList([test_account.address], {"from": test_account})
    account_starting_balance = test_account.balance()
    contract_starting_balance = token.balance()
    assert token.totalSupply() == 0
    token.createTokenPresale(amount_minted, {"from": test_account, "value": fee})
    assert token.totalSupply() == amount_minted
    assert token.balanceOf(test_account) == amount_minted
    token.createTokenPresale(1, {"from": test_account, "value": fee / 2})
    assert token.totalSupply() == amount_minted + 1
    assert token.balanceOf(test_account) == 3
    assert test_account.balance() == account_starting_balance - 1.5 * fee
    assert token.balance() == contract_starting_balance + 1.5 * fee
