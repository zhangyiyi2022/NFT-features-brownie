from brownie import ERC721Custom
from scripts.helper_functions import get_account

# import from file or insert addresses here
whitelist_addresses = ["0x321312", "0x412526534"]


def add_to_whitelist():
    account = get_account()
    contract = ERC721Custom[len(ERC721Custom) - 1]

    add_tx = contract.addToWhiteList(whitelist_addresses, {"from": account})
    add_tx.wait(1)

    print(f"Added everyone to whitelist succesfully!")


def flip_presale_state():
    account = get_account()
    contract = ERC721Custom[len(ERC721Custom) - 1]

    sale_tx = contract.presaleStateChange({"from": account})
    sale_tx.wait(1)

    print("Presale started!")


def create_presale_nft(mint_amount, presale_mint_price):

    fee = presale_mint_price * mint_amount

    account = get_account()
    contract = ERC721Custom[len(ERC721Custom) - 1]

    create_tx = contract.createTokenPresale(
        mint_amount,
        {"from": account, "value": fee},
    )
    create_tx.wait(1)

    print("Collectible created!")
    print(f"{contract.totalSupply()} total nfts bought!")


def main():
    add_to_whitelist()
    flip_presale_state()
    create_presale_nft(1, 88800000000000000)
