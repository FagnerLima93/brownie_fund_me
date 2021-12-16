from brownie import FundMe, accounts
from scripts.general import get_account 

def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = FundMe[-1].getEntranceFee()
    print(entrance_fee)
    print(f"The current entrance fee is {entrance_fee}.")
    print("Funding...")
    FundMe[-1].fund({"from": account, "value": entrance_fee})

def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    FundMe[-1].withdraw({"from": account})

def main():
    fund()
    withdraw()