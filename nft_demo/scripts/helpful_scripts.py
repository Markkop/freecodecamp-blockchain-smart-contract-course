from brownie import accounts, network, config, VRFCoordinatorMock, LinkToken, Contract

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPEANSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


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
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
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


def deploy_mocks():
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    LinkToken.deploy({"from": account})
    if len(LinkToken) <= 0:
        LinkToken.deploy({"from": account})
    if len(VRFCoordinatorMock) <= 0:
        VRFCoordinatorMock.deploy(LinkToken[-1], {"from": account})
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
