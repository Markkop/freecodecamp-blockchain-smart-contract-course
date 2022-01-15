from brownie import accounts, SimpleStorage, network, config


def deploy_simple_storage():
    # account = accounts[0]  # Account from self hosted ganache
    # account = accounts.load("freecodecamp-account") # Account from brownie cli
    # account = accounts.add(config["wallets"]["from_key"]) # Account from .env
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_store_value = simple_storage.retrieve()
    print(updated_store_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
