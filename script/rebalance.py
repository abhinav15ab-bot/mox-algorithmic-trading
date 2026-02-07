# from eth_utils import to_wei
# from moccasin.config import get_config

# # -----------------------------
# # Setup
# # -----------------------------
# config = get_config()
# network = config.get_active_network()

# # Contracts
# weth = network.manifest_named("weth")
# usdc = network.manifest_named("usdc")
# router = network.manifest_named("uniswap_swap_router")

# eth_usd = network.manifest_named("eth_usd")
# usdc_usd = network.manifest_named("usdc_usd")

# account = network.get_default_account()
# sender = account.address

# # -----------------------------
# # Helpers
# # -----------------------------
# def price(feed):
#     return feed.latestAnswer() / 1e8  # Chainlink uses 8 decimals


# def balances():
#     return weth.balanceOf(sender), usdc.balanceOf(sender)


# def portfolio():
#     weth_bal, usdc_bal = balances()

#     weth_usd = (weth_bal / 1e18) * price(eth_usd)
#     usdc_usd_val = (usdc_bal / 1e6) * price(usdc_usd)

#     total = weth_usd + usdc_usd_val
#     return weth_usd, usdc_usd_val, total


# def decision(weth_usd, total):
#     ratio = weth_usd / total

#     if ratio > 0.55:
#         return "SELL_WETH"
#     elif ratio < 0.45:
#         return "BUY_WETH"
#     else:
#         return "NO_ACTION"


# # -----------------------------
# # Rebalance Logic
# # -----------------------------
# weth_usd, usdc_usd_val, total = portfolio()

# print(f"WETH USD : {weth_usd:.2f}")
# print(f"USDC USD : {usdc_usd_val:.2f}")
# print(f"TOTAL    : {total:.2f}")

# action = decision(weth_usd, total)
# print("Action:", action)

# if action == "NO_ACTION":
#     print("✅ Portfolio already balanced")
#     exit()

# # Rebalance only the excess
# target = total / 2
# delta_usd = abs(weth_usd - target)

# eth_price = price(eth_usd)
# delta_weth = delta_usd / eth_price
# amount_in = to_wei(delta_weth, "ether")

# # -----------------------------
# # Execute Swap
# # -----------------------------
# if action == "SELL_WETH":
#     print("🔁 Rebalancing: WETH → USDC")

#     weth.approve(router.address, amount_in, sender=sender)

#     router.exactInputSingle(
#         (
#             weth.address,
#             usdc.address,
#             3000,        # Uniswap V3 0.3% pool
#             sender,
#             amount_in,
#             0,           # amountOutMinimum (unsafe but OK for demo)
#             0
#         ),
#         sender=sender
#     )

# elif action == "BUY_WETH":
#     print("🔁 Rebalancing: USDC → WETH")
#     print("⚠️ BUY path intentionally skipped for v1")

# print("✅ Rebalance completed")

from eth_utils import to_wei
from moccasin.config import get_config

# =============================
# Config & Network
# =============================
config = get_config()
network = config.get_active_network()

weth = network.manifest_named("weth")
usdc = network.manifest_named("usdc")
router = network.manifest_named("uniswap_swap_router")

eth_usd = network.manifest_named("eth_usd")
usdc_usd = network.manifest_named("usdc_usd")

account = network.get_default_account()
sender = account.address

# =============================
# Parameters (Simulation)
# =============================
MEV_PENALTY = 0.005   # 0.5% adverse execution (simulated)
LOWER = 0.45
UPPER = 0.55

# =============================
# Helpers
# =============================
def price(feed):
    return feed.latestAnswer() / 1e8  # Chainlink


def balances():
    return weth.balanceOf(sender), usdc.balanceOf(sender)


def portfolio():
    weth_bal, usdc_bal = balances()

    weth_usd = (weth_bal / 1e18) * price(eth_usd)
    usdc_usd_val = (usdc_bal / 1e6) * price(usdc_usd)

    total = weth_usd + usdc_usd_val
    return weth_usd, usdc_usd_val, total


def decision(weth_usd, total):
    ratio = weth_usd / total

    if ratio > UPPER:
        return "SELL_WETH"
    elif ratio < LOWER:
        return "BUY_WETH"
    else:
        return "NO_ACTION"


# =============================
# Snapshot for HODL baseline
# =============================
initial_weth, initial_usdc = balances()

def hodl_value():
    return (
        (initial_weth / 1e18) * price(eth_usd)
        + (initial_usdc / 1e6) * price(usdc_usd)
    )


# =============================
# Rebalance Logic
# =============================
weth_usd, usdc_usd_val, total = portfolio()

print(f"WETH USD : {weth_usd:.2f}")
print(f"USDC USD : {usdc_usd_val:.2f}")
print(f"TOTAL    : {total:.2f}")

action = decision(weth_usd, total)
print("Action:", action)

if action == "NO_ACTION":
    print("✅ Portfolio already balanced")
    exit()

# Target = 50 / 50
target = total / 2
delta_usd = abs(weth_usd - target)

# =============================
# MEV Simulation (Quantification)
# =============================
mev_cost = delta_usd * MEV_PENALTY
print(f"Rebalance size (USD): {delta_usd:.2f}")
print(f"Simulated MEV cost (0.5%): {mev_cost:.2f}")

eth_price = price(eth_usd)
delta_weth = delta_usd / eth_price

# =============================
# Execute Rebalance
# =============================
if action == "SELL_WETH":
    print("🔁 Rebalancing: WETH → USDC")

    amount_in = to_wei(delta_weth, "ether")

    weth.approve(router.address, amount_in, sender=sender)

    router.exactInputSingle(
        (
            weth.address,
            usdc.address,
            3000,
            sender,
            amount_in,
            0,
            0
        ),
        sender=sender
    )

elif action == "BUY_WETH":
    print("🔁 Rebalancing: USDC → WETH")

    amount_in_usdc = int(delta_usd * 1e6)
    assert usdc.balanceOf(sender) >= amount_in_usdc, "Not enough USDC"

    usdc.approve(router.address, amount_in_usdc, sender=sender)

    router.exactInputSingle(
        (
            usdc.address,
            weth.address,
            3000,
            sender,
            amount_in_usdc,
            0,
            0
        ),
        sender=sender
    )

# =============================
# Post-rebalance Evaluation
# =============================
_, _, rebalanced_total = portfolio()
hodl = hodl_value()

print("——— Evaluation ———")
print(f"HODL value        : {hodl:.2f}")
print(f"Rebalanced value  : {rebalanced_total:.2f}")
print(f"Delta vs HODL     : {rebalanced_total - hodl:.2f}")
print(f"Estimated MEV drag: {-mev_cost:.2f}")

print("✅ Rebalance + simulation completed")
