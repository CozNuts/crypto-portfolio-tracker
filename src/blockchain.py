from web3 import Web3
import requests
from config import Config
from src.utils import PriceFetcher

class BlockchainManager:
    """Handles all blockchain interactions"""
    
    def __init__(self):
        self.config = Config()
        self.w3 = Web3(Web3.HTTPProvider(self.config.INFURA_URL))
        
    def is_connected(self):
        """Check blockchain connection"""
        return self.w3.is_connected()
    
    def get_eth_balance(self, address):
        """Get ETH balance in Ether"""
        try:
            checksum_address = self.w3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(checksum_address)
            return float(self.w3.from_wei(balance_wei, 'ether'))
        except Exception as e:
            print(f"Error getting ETH balance: {e}")
            return 0.0
    
    def get_token_balance(self, token_address, wallet_address):
        """Get ERC20 token balance"""
        try:
            token_contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address),
                abi=self.config.ERC20_ABI
            )
            
            balance = token_contract.functions.balanceOf(
                self.w3.to_checksum_address(wallet_address)
            ).call()
            
            decimals = token_contract.functions.decimals().call()
            return balance / (10 ** decimals)
            
        except Exception as e:
            print(f"Error getting token balance: {e}")
            return 0.0
    
    def get_transaction_history(self, wallet_address, limit=10):
        """Get recent transactions using Etherscan API"""
        if not self.config.ETHERSCAN_API_KEY:
            return []
            
        try:
            url = "https://api.etherscan.io/api"
            params = {
                'module': 'account',
                'action': 'txlist',
                'address': wallet_address,
                'sort': 'desc',
                'apikey': self.config.ETHERSCAN_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=15)
            data = response.json()
            
            if data['status'] == '1':
                transactions = data['result'][:limit]
                formatted_txs = []
                
                for tx in transactions:
                    formatted_txs.append({
                        'hash': tx['hash'],
                        'from': tx['from'],
                        'to': tx['to'],
                        'value': float(tx['value']) / 1e18,  # wei to ETH
                        'timestamp': int(tx['timeStamp'])
                    })
                
                return formatted_txs
            return []
                
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []