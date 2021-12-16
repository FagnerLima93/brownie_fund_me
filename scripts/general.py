from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"] 

# both of these are for the getPrice function in the FundMe.sol file
DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0: # Here we're checking if there are any MockV3Aggregators already deployed instead of redeploying it everytime we deploy any contracts - remember we can check the length of MockV3Aggregator because running it this way will read a list of all the contracts with this name
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})  # The toWei function will add 18 decimals to the 2000 value
    print("Mocks Deployed.")
