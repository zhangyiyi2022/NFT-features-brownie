from brownie import CustomNFT
import os
from scripts.helper_functions import get_account

token_uri = "YOUR TOKEN URI"
contract_uri = "YOUR CONTRACT URI"


def deploy_nft():
    account = get_account()

    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False

    madcroc_nft = CustomNFT.deploy(
        token_uri,
        contract_uri,
        {"from": account},
        publish_source=publish_source,
    )

    print(f"Token {madcroc_nft.address} deployed!")


def main():
    deploy_nft()
