from brownie import FundMe, MockV3Aggregator,network, config
from scripts.general import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fund_me():
    account = get_account()
    
    # if we're on a persistent network like rinkeby, use the associated address
    # otherwise deploy mocks and use a fake aggregator contract address that we've deployed
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"] # This if statement says, if we're not on a development network, pull the address right from ht config
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        
    fund_me = FundMe.deploy(
        price_feed_address,  # passing the price feed address to our fund me contract constructor / Anything we need to pass to a constructor through brownie is done this way
        {"from": account}, 
        publish_source=config["networks"][network.show_active()].get("verify"),  # The publish_source= true statement allows us to publish our source code to etherscan so we can verify our transactions
    )
    
    print(f"Contract deployed to {fund_me.address}")  # This will show us the contract ADRESS after it's been deployed
    return fund_me # This allows us to work with this function in other python TEST files(test_fund_me.py)

def main():
    deploy_fund_me()

# ---------------------------------------------- UNREFACTORED CODE FOR BETTER UNDERSTANDING -------------------------------------------------------------
# def deploy_fund_me():
#     account = get_account()
    
#     # if we're on a persistent network like rinkeby, use the associated address
#     # otherwise deploy mocks and use a fake aggregator contract address that we've deployed
#     if network.show_active() != "development":
#         price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"] # This if statement says, if we're not on a development network, pull the address right from ht config
#     else:
#         print(f"The active network is {network.show_active()}")
#         print("Deploying Mocks...")
#         mock_aggregator = MockV3Aggregator.deploy(18, 2000000000000000000000, {"from": account})  # 5:31
#         price_feed_address = mock_aggregator.address
#         print("Mocks Deployed.")

#     fund_me = FundMe.deploy(
#         price_feed_address,  # passing the price feed address to our fund me contract constructor / Anything we need to pass to a constructor through brownie is done this way
#         {"from": account}, 
#         publish_source=config["networks"][network.show_active()].get("verify"),  # The publish_source= true statement allows us to publish our source code to etherscan so we can verify our transactions
#     )
#     print(f"Contract deployed to {fund_me.address}")  # This will show us the contract ADRESS after it's been deployed