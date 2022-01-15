from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def main():
    account = get_account()
    print(f"Deploying to { network.show_active()}")
    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})

    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data(initializer)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    print(f"Proxy deployed to {proxy}, you can now upgrade to V2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # proxy_box.store(1, {"from": account})

    # upgrade
    box_v2 = BoxV2.deploy({"from": account})
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    tx = proxy_box.increment({"from": account})
    tx.wait(1)
    print(proxy_box.retrieve())
