from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    MockDAI,
    MockWETH,
    Contract,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPEANSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

INITIAL_PRICE_FEED_VALUE = 2000000000000000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_network_config(_config):
    return config["networks"][network.show_active()].get(_config)


def get_verify_flag():
    return config["networks"][network.show_active()].get("verify", False)


contract_to_mock = {
    "fau_token": MockDAI,
    "weth_token": MockWETH,
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        return contract_type[-1]
    contract_address = config["networks"][network.show_active()][contract_name]
    return Contract.from_abi(contract_type._name, contract_address, contract_type.abi)


DECIMALS = 18
INITIAL_VALUE = Web3.toWei(2000, "ether")


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockDAI) <= 0:
        MockDAI.deploy({"from": account})
    if len(MockWETH) <= 0:
        MockWETH.deploy({"from": account})
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print("Deployed!")


def fund_with_link(
    contract_address,
    account=None,
    link_token=None,
    amount=100000000000000000,  # 0.1 Link
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})

    # Alternative: Interact with contracts using interface
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})

    tx.wait(1)
    print("Fund contract!")
    return tx


BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
