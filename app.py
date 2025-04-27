import streamlit as st
import yfinance as yf
import pandas as pd

# Title of the app
st.title('📈 Stock Price Tracker (India)')

# Short description
st.write('Welcome! Track latest live stock prices from NSE and BSE markets.')

# Input box for user to type stock symbol
stock = st.text_input('Enter Stock Symbol (Example: RELIANCE, TCS, INFY)')

# Dropdown for selecting the time period
time_period = st.selectbox(
    "Select Time Period",
    ["7d", "30d", "1mo", "3mo", "6mo", "1y", "5y"]
)

if stock:
    st.write(f"You entered: {stock}")

    # Automatically add .NS for NSE stocks if not an index (e.g., Nifty)
    if not stock.startswith('^'):
        stock = stock.upper() + ".NS"
    
    # Fetch Stock Data from Yahoo Finance based on the selected time period
    stock_data = yf.Ticker(stock)  # We use the modified stock symbol
    stock_info = stock_data.history(period=time_period)  # Fetch data for selected time period

    # Get the latest closing price and previous closing price
    latest_price = stock_info['Close'].iloc[-1]
    previous_price = stock_info['Close'].iloc[-2] if len(stock_info) > 1 else latest_price

    # Calculate the percentage change
    change_percentage = ((latest_price - previous_price) / previous_price) * 100 if previous_price != latest_price else 0
    
    # Display the latest price
    st.write(f"Latest price for {stock}: ₹{latest_price:.2f}")
    
    # Display the percentage change with color coding
    if change_percentage >= 0:
        st.markdown(f"**Price Change: +{change_percentage:.2f}%**", unsafe_allow_html=True)
        st.markdown('<span style="color:green;">(Profit)</span>', unsafe_allow_html=True)
    else:
        st.markdown(f"**Price Change: {change_percentage:.2f}%**", unsafe_allow_html=True)
        st.markdown('<span style="color:red;">(Loss)</span>', unsafe_allow_html=True)

    # Plot the historical stock prices (close price) for the selected period
    st.subheader(f"Stock Price Chart for {stock} over the last {time_period}")
    st.line_chart(stock_info['Close'])  # Line chart for closing prices over the selected period
