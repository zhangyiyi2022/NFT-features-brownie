from brownie import ERC721Custom
import os
from scripts.helper_functions import get_account

token_uri = "YOUR TOKEN URI"
contract_uri = "YOUR CONTRACT URI"


def deploy_nft():
    account = get_account()

    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False

    custom_nft = ERC721Custom.deploy(
        token_uri,
        contract_uri,
        {"from": account},
        publish_source=publish_source,
    )

    print(f"Token {custom_nft.address} deployed!")


def main():
    deploy_nft()
