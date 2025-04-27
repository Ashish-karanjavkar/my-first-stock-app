import streamlit as st
import yfinance as yf

# Title of the app
st.title('📈 Stock Price Tracker (India)')

# Short description
st.write('Welcome! Track latest live stock prices from NSE and BSE markets.')

# Input box for user to type stock symbol
stock = st.text_input('Enter Stock Symbol (Example: RELIANCE, TCS, INFY)')

if stock:
    st.write(f"You entered: {stock}")

    # Automatically add .NS for NSE stocks if not an index (e.g., Nifty)
    if not stock.startswith('^'):
        stock = stock.upper() + ".NS"
    
    # Fetch Stock Data from Yahoo Finance
    stock_data = yf.Ticker(stock)  # We use the modified stock symbol
    stock_info = stock_data.history(period="1d")  # Fetch 1-day data

    # Get the latest closing price
    latest_price = stock_info['Close'].iloc[-1]
    
    # Display the latest price
    st.write(f"Latest price for {stock}: ₹{latest_price:.2f}")
