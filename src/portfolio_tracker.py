from src.blockchain import BlockchainManager
from src.utils import PriceFetcher, FormatUtils
from config import Config
import time

class PortfolioTracker:
    """Main portfolio tracking functionality"""
    
    def __init__(self):
        self.blockchain = BlockchainManager()
        self.config = Config()
        self.utils = FormatUtils()
        self.price_fetcher = PriceFetcher()
    
    def get_portfolio_overview(self, wallet_address):
        """Get complete portfolio breakdown"""
        if not self.blockchain.is_connected():
            return {"error": "Not connected to blockchain"}
        
        if not self.price_fetcher.validate_eth_address(wallet_address):
            return {"error": "Invalid Ethereum address"}
        
        portfolio = {
            'wallet_address': wallet_address,
            'assets': {},
            'total_value_usd': 0
        }
        
        # Get ETH balance and value
        eth_balance = self.blockchain.get_eth_balance(wallet_address)
        eth_price = self.price_fetcher.get_token_price('ETH')
        eth_value = eth_balance * eth_price
        
        portfolio['assets']['ETH'] = {
            'balance': eth_balance,
            'price_usd': eth_price,
            'value_usd': eth_value
        }
        portfolio['total_value_usd'] += eth_value
        
        # Get ERC20 token balances
        for token_address, symbol in self.config.COMMON_TOKENS.items():
            balance = self.blockchain.get_token_balance(token_address, wallet_address)
            
            if balance > 0:
                price = self.price_fetcher.get_token_price(symbol)
                token_value = balance * price
                
                portfolio['assets'][symbol] = {
                    'balance': balance,
                    'price_usd': price,
                    'value_usd': token_value
                }
                portfolio['total_value_usd'] += token_value
        
        return portfolio
    
    def get_transaction_history(self, wallet_address, limit=10):
        """Get transaction history"""
        return self.blockchain.get_transaction_history(wallet_address, limit)
    
    def format_portfolio_for_display(self, portfolio):
        """Format portfolio data for display"""
        if 'error' in portfolio:
            return portfolio
        
        formatted = {
            'wallet_address': self.utils.shorten_address(portfolio['wallet_address']),
            'total_value': self.utils.format_currency(portfolio['total_value_usd']),
            'assets': []
        }
        
        for symbol, asset in portfolio['assets'].items():
            formatted['assets'].append({
                'symbol': symbol,
                'balance': self.utils.format_crypto(asset['balance']),
                'price': self.utils.format_currency(asset['price_usd']),
                'value': self.utils.format_currency(asset['value_usd'])
            })
        
        return formatted