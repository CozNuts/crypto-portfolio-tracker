from src.portfolio_tracker import PortfolioTracker
from src.utils import PriceFetcher
import argparse

def main():
    parser = argparse.ArgumentParser(description='Crypto Portfolio Tracker')
    parser.add_argument('wallet', help='Ethereum wallet address')
    parser.add_argument('--transactions', '-t', action='store_true', 
                       help='Show transaction history')
    
    args = parser.parse_args()
    
    # Validate address
    if not PriceFetcher().validate_eth_address(args.wallet):
        print("❌ Invalid Ethereum address")
        return
    
    tracker = PortfolioTracker()
    
    if not tracker.blockchain.is_connected():
        print("❌ Not connected to Ethereum network")
        return
    
    print(f"\n🚀 Tracking portfolio for: {args.wallet}\n")
    
    # Get portfolio
    portfolio = tracker.get_portfolio_overview(args.wallet)
    
    if 'error' in portfolio:
        print(f"❌ Error: {portfolio['error']}")
        return
    
    # Display portfolio
    formatted = tracker.format_portfolio_for_display(portfolio)
    
    print(f"📊 Total Portfolio Value: {formatted['total_value']}")
    print("\n💰 Assets:")
    print("-" * 60)
    
    for asset in formatted['assets']:
        print(f"  {asset['symbol']}")
        print(f"    Balance: {asset['balance']}")
        print(f"    Price: {asset['price']}")
        print(f"    Value: {asset['value']}")
        print()
    
    # Show transactions if requested
    if args.transactions:
        print("📊 Recent Transactions:")
        print("-" * 60)
        
        transactions = tracker.get_transaction_history(args.wallet, 3)
        
        if transactions:
            for tx in transactions:
                print(f"  Hash: {tracker.utils.shorten_address(tx['hash'])}")
                print(f"  From: {tracker.utils.shorten_address(tx['from'])}")
                print(f"  To: {tracker.utils.shorten_address(tx['to'])}")
                print(f"  Value: {tx['value']:.4f} ETH")
                print()
        else:
            print("  No transactions found")

if __name__ == "__main__":
    main()