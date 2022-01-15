from brownie import OurToken
from scripts.helpful_scripts import get_account
from web3 import Web3

INITIAL_SUPPLY = Web3.toWei(1000, "ether")


def deploy_token():
    account = get_account()
    token = OurToken.deploy(INITIAL_SUPPLY, {"from": account})
    return token


def main():
    deploy_token()
