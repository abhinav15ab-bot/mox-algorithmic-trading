from eth_utils import to_wei
from moccasin.config import get_config

# Load config and network
config = get_config()
network = config.get_active_network()

# Contracts from moccasin.toml
weth = network.manifest_named("weth")
usdc = network.manifest_named("usdc")
router = network.manifest_named("uniswap_swap_router")

# EOA
account = network.get_default_account()
sender = account.address

amount_in = to_wei(0.1, "ether")

print("Wrapping ETH into WETH...")
weth.deposit(
    value=amount_in,
    sender=sender
)

print("Approving Uniswap router...")
weth.approve(
    router.address,
    amount_in,
    sender=sender
)

print("Swapping WETH → USDC...")
# router.exactInputSingle(
#     (
#         weth.address,
#         usdc.address,
#         3000,        # fee tier
#         sender,      # recipient
#         0,           # deadline
#         amount_in,   # amountIn
#         0            # sqrtPriceLimitX96
#     ),
#     sender=sender
# )

router.exactInputSingle(
    (
        weth.address,
        usdc.address,
        3000,
        account.address,
        amount_in,
        0,
        0
    )
)


print("✅ Swap executed successfully on Tenderly")
