### Project Evolution

Initially, this repository focused on learning DeFi primitives by executing
basic Uniswap V3 swaps on a Tenderly fork.

<img width="1918" height="967" alt="image" src="https://github.com/user-attachments/assets/36a7cb84-dbda-40e8-b58b-2a603252f582" />

<img width="1920" height="1080" alt="Screenshot (297)" src="https://github.com/user-attachments/assets/7aee0d2d-f36b-4511-a4c0-c86c83e1b02d" />



In a new branch, I extended the project into a portfolio rebalance bot that:
- Values assets in USD using Chainlink oracles
- Decides BUY / SELL / HOLD actions
- Rebalances WETH ↔ USDC safely on Uniswap V3
- Simulates real execution costs and risks

The original project remains unchanged on `main`.
