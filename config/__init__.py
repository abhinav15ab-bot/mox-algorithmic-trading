from config.tenderly import TENDERLY_RPC_URL
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(TENDERLY_RPC_URL))
