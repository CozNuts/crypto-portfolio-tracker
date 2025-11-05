import requests
from web3 import Web3

class PriceFetcher:
    """Fetch cryptocurrency prices from CoinGecko API"""
    
    @staticmethod
    def get_token_price(token_symbol):
        """Get current token price in USD"""
        try:
            # Map symbols to CoinGecko IDs
            coin_mapping = {
                'ETH': 'ethereum',
                'USDT': 'tether', 
                'USDC': 'usd-coin',
                'DAI': 'dai',
                'WBTC': 'wrapped-bitcoin'
            }
            
            coin_id = coin_mapping.get(token_symbol, 'ethereum')
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {'ids': coin_id, 'vs_currencies': 'usd'}
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            return data.get(coin_id, {}).get('usd', 0)
            
        except Exception:
            return 0
    
    @staticmethod
    def validate_eth_address(address):
        """Validate Ethereum address format"""
        return Web3.is_address(address)

class FormatUtils:
    """Formatting utilities for display"""
    
    @staticmethod
    def format_currency(value):
        """Format currency with commas"""
        return f"${value:,.2f}"
    
    @staticmethod
    def format_crypto(value):
        """Format cryptocurrency amounts appropriately"""
        if value == 0:
            return "0.0000"
        elif value < 0.0001:
            return f"{value:.8f}"
        else:
            return f"{value:.4f}"
    
    @staticmethod
    def shorten_address(address, chars=6):
        """Shorten Ethereum address for display"""
        return f"{address[:chars]}...{address[-chars:]}"