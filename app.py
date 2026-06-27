import streamlit as st
import pandas as pd
import ccxt

st.set_page_config(page_title="Crypto Volatility Screener", layout="wide")

@st.cache_data(ttl=60) # Caches data for 60 seconds
def get_crypto_data():
    # Connect to Binance's public API (no keys needed)
    exchange = ccxt.binance()
    tickers = exchange.fetch_tickers()
    
    data = []
    for symbol, ticker in tickers.items():
        # Filter for standard USDT trading pairs
        if symbol.endswith('/USDT') and ticker.get('quoteVolume') is not None:
            data.append({
                'Symbol': symbol,
                'Price (USDT)': ticker.get('last', 0),
                '24h Change (%)': ticker.get('percentage', 0),
                '24h Volume (USDT)': ticker.get('quoteVolume', 0)
            })
            
    df = pd.DataFrame(data)
    return df.dropna()

def main():
    st.title("⚡ Crypto Volatility & Volume Screener")
    st.markdown("Live data fetched directly via standard exchange APIs.")
    
    df = get_crypto_data()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 Top 10 High Volatility (Gainers)")
            # Sort by highest percentage change
            volatility_df = df.sort_values(by='24h Change (%)', ascending=False).head(10)
            st.dataframe(volatility_df, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("📊 Top 10 Abnormal Volume")
            # Sort by highest volume traded
            volume_df = df.sort_values(by='24h Volume (USDT)', ascending=False).head(10)
            st.dataframe(volume_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
