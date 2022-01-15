from scripts.helpful_scripts import get_account, OPEANSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    create_tx = simple_collectible.createCollectible(
        sample_token_uri, {"from": account}
    )
    create_tx.wait(1)
    print(
        f"You can see the NFT at {OPEANSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1 )}"
    )
    return simple_collectible


def main():
    deploy_and_create()
