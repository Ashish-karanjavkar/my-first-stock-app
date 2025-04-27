import streamlit as st
import yfinance as yf
import pandas as pd

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
    stock_info = stock_data.history(period="7d")  # Fetch last 7 days data

    # Get the latest closing price and previous closing price
    latest_price = stock_info['Close'].iloc[-1]
    previous_price = stock_info['Close'].iloc[-2]

    # Calculate the percentage change
    change_percentage = ((latest_price - previous_price) / previous_price) * 100
    
    # Display the latest price
    st.write(f"Latest price for {stock}: ₹{latest_price:.2f}")
    
    # Display the percentage change with color coding
    if change_percentage >= 0:
        st.markdown(f"**Price Change: +{change_percentage:.2f}%**", unsafe_allow_html=True)
        st.markdown('<span style="color:green;">(Profit)</span>', unsafe_allow_html=True)
    else:
        st.markdown(f"**Price Change: {change_percentage:.2f}%**", unsafe_allow_html=True)
        st.markdown('<span style="color:red;">(Loss)</span>', unsafe_allow_html=True)

    # Plot the historical stock prices (close price)
    st.subheader(f"Stock Price Chart for {stock}")
    st.line_chart(stock_info['Close'])  # Line chart for closing prices over the last 7 days
