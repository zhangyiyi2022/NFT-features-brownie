import pytest
from brownie import exceptions

amount_minted = 10
price = 1000000000000000
fee = amount_minted * price

community_address = "0xdsadsadas"
dev_address = "0xdsadsadsa"


# test on rinkeby
@pytest.mark.withdraw
def test_withdraw(token, test_account):
    pytest.skip()
    token.saleStateChange({"from": test_account})
    token.createToken(amount_minted, {"from": test_account, "value": fee})
    token_balance = token.balance()
    assert token.balance() == fee
    token.withdraw({"from": test_account})
    assert token.balance() == 0
    assert community_address.balance() == 0.9 * token_balance
    assert dev_address.balance() == 0.1 * token_balance
