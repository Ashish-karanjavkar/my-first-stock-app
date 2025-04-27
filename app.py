import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Title of the app
st.title('📈 Stock Price Tracker (India)')

# Short description
st.write('Welcome! Track latest live stock prices from NSE and BSE markets.')

# Input box for user to type stock symbol
stock = st.text_input('Enter Stock Symbol (Example: RELIANCE, TCS, INFY)')

# Date picker for start and end date
start_date = st.date_input('Select Start Date', datetime.today())
end_date = st.date_input('Select End Date', datetime.today())

# Dropdown for selecting the time period (for fallback)
time_period = st.selectbox(
    "Select Time Period (For fallback)",
    ["7d", "30d", "1mo", "3mo", "6mo", "1y", "5y"]
)

# Show the dates chosen by the user
st.write(f"Selected Dates: {start_date} to {end_date}")

# Fetch stock data if the stock symbol is provided
if stock:
    st.write(f"You entered: {stock}")

    # Automatically add .NS for NSE stocks if not an index (e.g., Nifty)
    if not stock.startswith('^'):
        stock = stock.upper() + ".NS"
    
    # Convert date inputs to strings for the yfinance API
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    # Fetch Stock Data from Yahoo Finance
    stock_data = yf.Ticker(stock)
    
    # Try to get data for the custom date range first, fallback to time_period if no custom dates selected
    try:
        stock_info = stock_data.history(start=start_date_str, end=end_date_str)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        stock_info = stock_data.history(period=time_period)  # Fallback to pre-defined time period
    
    # If no data available, show a message
    if stock_info.empty:
        st.write("No data available for the selected date range.")
    else:
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
        st.subheader(f"Stock Price Chart for {stock} from {start_date_str} to {end_date_str}")
        st.line_chart(stock_info['Close'])  # Line chart for closing prices over the custom date range
