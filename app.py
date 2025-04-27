import streamlit as st
import yfinance as yf
from nsepy import get_history
from datetime import datetime, date
import plotly.graph_objects as go  # For candlestick chart
import time  # For auto-refresh logic
import pandas as pd

# Title of the app
st.title('📈 Stock Price Tracker and Option Chain Stats')

# Sidebar for page selection
page = st.sidebar.radio("Select Page", ["Stock Tracker", "Option Chain Stats"])

# ====================
# Stock Tracker Page
if page == "Stock Tracker":
    st.write('Welcome! Track live stock prices from NSE and BSE markets.')

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

    # Refresh button
    refresh = st.button("Refresh Data")

    # Fetch stock data when the refresh button is clicked or when stock is entered
    if stock or refresh:
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

            # Plot the candlestick chart for the stock data
            st.subheader(f"Candlestick Chart for {stock} from {start_date_str} to {end_date_str}")

            # Prepare the data for the candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x=stock_info.index,
                open=stock_info['Open'],
                high=stock_info['High'],
                low=stock_info['Low'],
                close=stock_info['Close'],
                name="Candlestick"
            )])

            # Update the layout of the chart for better visibility
            fig.update_layout(
                title=f"{stock} Candlestick Chart",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                xaxis_rangeslider_visible=False
            )
            
            # Show the candlestick chart in the Streamlit app
            st.plotly_chart(fig)

        # Option to automatically refresh every minute
        if refresh:
            time.sleep(60)  # Wait for 60 seconds before refreshing (you can adjust this time)

# ====================
# Option Chain Stats Page
elif page == "Option Chain Stats":
    st.write("Fetching Option Chain Data...")

    # Input box for symbol to fetch option chain data
    symbol_input = st.text_input("Enter the Symbol (e.g., Nifty50, Nifty, etc.)", "NIFTY50")

    # Date selection dropdown for the last 10 days
    date_dropdown = st.selectbox("Select Date", pd.date_range(datetime.today() - pd.Timedelta(days=10), datetime.today()).strftime('%Y-%m-%d'))
    st.write(f"Selected Date: {date_dropdown}")

    # Time selection dropdown
    time_dropdown = st.selectbox("Select Time", pd.date_range(datetime.today(), datetime.today() + pd.Timedelta(hours=1), freq="15T").strftime('%H:%M'))
    st.write(f"Selected Time: {time_dropdown}")

    # Fetch the data when the user selects a symbol, date, and time
    if symbol_input:
        st.write(f"Fetching data for {symbol_input} on {date_dropdown} at {time_dropdown}...")
        
        # Fetch Option Chain Data for the selected symbol, date, and time
        try:
            option_data = get_history(symbol=symbol_input, index=True, start=datetime.strptime(date_dropdown, '%Y-%m-%d'), end=datetime.strptime(date_dropdown, '%Y-%m-%d'))
            
            if not option_data.empty:
                # Display fetched data
                st.write(option_data)
            else:
                st.write(f"No data available for {symbol_input} on {date_dropdown} at {time_dropdown}.")
        except Exception as e:
            st.write(f"Error fetching data: {e}")
