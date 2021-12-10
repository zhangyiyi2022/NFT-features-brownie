from brownie import CustomNFT
from scripts.helper_functions import get_account


def flip_presale_state():
    account = get_account()
    contract = CustomNFT[len(CustomNFT) - 1]

    sale_tx = contract.presaleStateChange({"from": account})
    sale_tx.wait(1)

    print("Presale closed!")


def set_new_token_price(new_price):
    account = get_account()
    contract = CustomNFT[len(CustomNFT) - 1]

    set_tx = contract.setTokenPrice(new_price, {"from": account})
    set_tx.wait(1)
    print(f"New token price of {new_price} WEI adjusted")


def flip_sale_state():
    account = get_account()
    contract = CustomNFT[len(CustomNFT) - 1]

    sale_tx = contract.saleStateChange({"from": account})
    sale_tx.wait(1)

    print("Sale started!")


def create_nft(mint_amount, mint_price):

    fee = mint_price * mint_amount

    account = get_account()
    contract = CustomNFT[len(CustomNFT) - 1]

    create_tx = contract.createToken(
        mint_amount,
        {"from": account, "value": fee},
    )
    create_tx.wait(1)

    print("Collectible created!")
    print(f"{contract.totalSupply()} total nfts bought!")


def main():
    flip_presale_state()
    set_new_token_price(99900000000000000)
    flip_sale_state()
    create_nft(1, 99900000000000000)
