import streamlit as st
import pandas as pd
import plotly.express as px
from src.portfolio_tracker import PortfolioTracker

# Page configuration
st.set_page_config(
    page_title="Crypto Portfolio Tracker",
    page_icon="🚀",
    layout="wide"
)

def main():
    st.title("🚀 Crypto Portfolio Tracker")
    st.markdown("Track your Ethereum wallet balances and token holdings")
    
    # Initialize tracker
    tracker = PortfolioTracker()
    
    # Sidebar with connection status
    st.sidebar.header("Settings")
    if tracker.blockchain.is_connected():
        st.sidebar.success("✅ Connected to Ethereum")
    else:
        st.sidebar.error("❌ Not connected to Ethereum")
    
    # Wallet input
    wallet_address = st.text_input(
        "Enter Ethereum Wallet Address:",
        placeholder="0x742e4c2f4c7c1b3b8be68c2a8b5e8d2a0b7e8f2a"
    )
    
    if wallet_address:
        if not tracker.price_fetcher.validate_eth_address(wallet_address):
            st.error("❌ Please enter a valid Ethereum address")
        else:
            # Display portfolio
            with st.spinner('🔄 Fetching portfolio data...'):
                portfolio = tracker.get_portfolio_overview(wallet_address)
            
            if 'error' in portfolio:
                st.error(f"Error: {portfolio['error']}")
            else:
                display_portfolio(portfolio, tracker, wallet_address)

def display_portfolio(portfolio, tracker, wallet_address):
    """Display portfolio information"""
    
    # Portfolio summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Portfolio Value", tracker.utils.format_currency(portfolio['total_value_usd']))
    
    with col2:
        eth_balance = portfolio['assets'].get('ETH', {}).get('balance', 0)
        st.metric("ETH Balance", f"{eth_balance:.4f}")
    
    with col3:
        num_tokens = len(portfolio['assets'])
        st.metric("Tokens Held", num_tokens)
    
    st.markdown("---")
    
    # Assets table
    st.subheader("💰 Assets")
    
    if portfolio['assets']:
        # Create data for table
        assets_data = []
        for symbol, asset in portfolio['assets'].items():
            assets_data.append({
                'Token': symbol,
                'Balance': tracker.utils.format_crypto(asset['balance']),
                'Price': tracker.utils.format_currency(asset['price_usd']),
                'Value': tracker.utils.format_currency(asset['value_usd'])
            })
        
        # Display as dataframe
        df = pd.DataFrame(assets_data)
        st.dataframe(df, use_container_width=True)
        
        # Portfolio pie chart
        if len(portfolio['assets']) > 1:
            st.subheader("📊 Portfolio Allocation")
            
            chart_data = []
            for symbol, asset in portfolio['assets'].items():
                chart_data.append({'Asset': symbol, 'Value': asset['value_usd']})
            
            chart_df = pd.DataFrame(chart_data)
            fig = px.pie(chart_df, values='Value', names='Asset')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No assets found in this wallet")
    
    # Transaction history
    st.markdown("---")
    st.subheader("📊 Recent Transactions")
    
    with st.spinner('Fetching transaction history...'):
        transactions = tracker.get_transaction_history(wallet_address, 5)
    
    if transactions:
        tx_data = []
        for tx in transactions:
            tx_data.append({
                'Hash': tracker.utils.shorten_address(tx['hash']),
                'From': tracker.utils.shorten_address(tx['from']),
                'To': tracker.utils.shorten_address(tx['to']),
                'Value': f"{tx['value']:.4f} ETH"
            })
        
        tx_df = pd.DataFrame(tx_data)
        st.dataframe(tx_df, use_container_width=True)
    else:
        st.info("No recent transactions found")

if __name__ == "__main__":
    main()