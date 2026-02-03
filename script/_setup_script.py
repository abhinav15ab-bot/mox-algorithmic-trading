from boa.contracts.abi.abi_contract import ABIContract
from typing import Tuple
from moccasin.config import get_active_network
import boa

STARTING_ETH_BALANCE = int(1000e18)
def _add_eth_balance():
    boa.env.set_balance(boa.env.eoa, STARTING_ETH_BALANCE)

def _add_token_balance(usdc, weth, active_network):
    
    
    pass

def setup_scrupt() -> Tuple[ABIContract, ABIContract, ABIContract, ABIContract]:
    print("Starting setup script...")

    # 1. Give ourselves some ETH
    # 2. Give ourselves some USDC and WETH
    active_network = get_active_network()

    usdc = active_network.manifest_named("usdc")
    weth = active_network.manifest_named("weth")

    if active_network.is_local_or_forked_network():
        _add_eth_balance()
        _add_token_balance(usdc, weth, active_network)
        