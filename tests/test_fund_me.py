# Just like we've done in the deployment python files we want these tests to run independently of what network we're working on
from brownie import network, accounts, config, exceptions # The exeptions import allows us to tell our tests exactly which exceptions we're expecting to see
from scripts.general import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
import pytest

# ------------------------------------------------------------ RUN: BROWNIE TEST to test ------------------------------------------------------------------

def test_can_fund_and_withdraw(): # In this test anyone can withraw the funded amount
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100# We can add the + 100 here just in case we need a lil more money to test
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee # We want to check that our address and the amount we funded is being adequately reported
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing") # RUN brownie test -k test_owner_can_withdraw --network rinkeby TO TEST on "real" TESTNET
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add() # This will give us a blank account
    # fund_me.withdraw({"from": bad_actor}) Having this bit of code here will throw the VirtualMachine error we expect 
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor}) # This tells our test that if this reverts with this VirtualMachineError that it's all good, we were expecting it to happen


    