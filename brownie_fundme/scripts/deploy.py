from brownie import FundMe
from scripts.helpful_scripts import get_account, get_price_feed, get_verify_flag


def deploy_fund_me():
    # account = accounts[0]  # Account from self hosted ganache
    # account = accounts.load("freecodecamp-account") # Account from brownie cli
    # account = accounts.add(config["wallets"]["from_key"]) # Account from .env
    account = get_account()
    fund_me = FundMe.deploy(
        get_price_feed(),
        {"from": account},
        publish_source=get_verify_flag(),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
