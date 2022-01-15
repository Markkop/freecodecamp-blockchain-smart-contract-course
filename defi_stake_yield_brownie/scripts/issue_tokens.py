from brownie import TokenFarm
from scripts.helpful_scripts import get_account


def issue_tokens():
    token_farm = TokenFarm[-1]
    print(f"Using TokenFarm {token_farm.address}")
    tx = token_farm.issueTokens({"from": get_account()})
    tx.wait(1)
    print(f"Tokens issued at {tx}")


def main():
    issue_tokens()
