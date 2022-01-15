from brownie import network
from scripts.helpful_scripts import get_account, get_network_config
from scripts.get_weth import get_weth
from brownie import network, interface
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = get_network_config("weth_token")
    if network.show_active() in ["mainnet-fork-dev"]:
        get_weth()
    lending_pool = get_lending_pool()
    approve_erc20(amount, erc20_address, lending_pool, account)
    deposit_tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    deposit_tx.wait(1)
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("Let's borrow!")
    dai_eth_price_feed = get_network_config("dai_eth_price_feed")
    dai_eth_price = get_asset_price(dai_eth_price_feed)
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    dai_address = get_network_config("dai_address")
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI")
    get_borrowable_data(lending_pool, account)
    repay_all(amount_dai_to_borrow, lending_pool, account)
    print("You just deposited, borrowed and repayed with Aave, Brownie and Chainlink!")


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        get_network_config("dai_address"),
        lending_pool,
        account,
    )
    repay_tx = lending_pool.repay(
        get_network_config("dai_address"),
        Web3.toWei(amount, "ether"),
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repayed!")


def get_asset_price(price_feed_address):
    price_feed = interface.AggregatorV3Interface(price_feed_address)
    (
        roundId,
        answer,
        startedAt,
        updatedAt,
        answeredInRound,
    ) = price_feed.latestRoundData()
    converted_price_feed = Web3.fromWei(answer, "ether")
    print(f"Price: {converted_price_feed}")
    return float(converted_price_feed)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrow_eth} worth of ETH")
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, erc20_address, spender, account):
    print("Approving ERC20 token...")
    erc20_token = interface.IERC20(erc20_address)
    tx = erc20_token.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        get_network_config("lending_pool_addresses_provider")
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
