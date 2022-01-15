from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    OPEANSEA_URL,
    get_network_config,
    get_contract,
    get_verify_flag,
)
from brownie import AdvancedCollectible

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        get_network_config("keyhash"),
        get_network_config("fee"),
        {"from": account},
        publish_source=get_verify_flag(),
    )
    fund_with_link(advanced_collectible)
    create_tx = advanced_collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("NFT Created!")
    return advanced_collectible, create_tx


def main():
    deploy_and_create()
