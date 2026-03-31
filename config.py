import os
from dotenv import load_dotenv

# Load .env only for local development
load_dotenv()

class Config:
    # Popular ERC20 tokens (address: symbol)
    COMMON_TOKENS = {
        '0xdAC17F958D2ee523a2206206994597C13D831ec7': 'USDT',
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': 'USDC', 
        '0x6B175474E89094C44Da98b954EedeAC495271d0F': 'DAI',
        '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599': 'WBTC'
    }
    
    # ERC20 ABI for token interactions
    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "type": "function"
        }
    ]
    
    def __init__(self):
        # Get secrets based on environment
        try:
            import streamlit as st
            self.INFURA_URL = st.secrets["INFURA_URL"]
            self.ETHERSCAN_API_KEY = st.secrets["ETHERSCAN_API_KEY"]
        except:
            self.INFURA_URL = os.getenv('INFURA_URL')
            self.ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')