import streamlit as st
from nsepy import get_history
from datetime import datetime, date, timedelta
import time

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

    # Fetch stock data when the refresh button is clicked or when stock is entered
    if stock:
        # Add logic for stock data retrieval here...
        pass  # Placeholder

# ====================
# Option Chain Stats Page
elif page == "Option Chain Stats":
    st.write("Fetching Option Chain Data...")

    # Date dropdown for past 10 days
    date_list = [date.today() - timedelta(days=i) for i in range(10)]
    selected_date = st.selectbox("Select Date", date_list)
    st.write(f"Selected Date: {selected_date}")

    # Time dropdown (for example, selecting hours)
    time_list = [f"{i}:00" for i in range(9, 16)]  # Selecting hours from 9 AM to 3 PM
    selected_time = st.selectbox("Select Time", time_list)
    st.write(f"Selected Time: {selected_time}")

    # Fetch data based on selected date and time
    if selected_date and selected_time:
        st.write(f"Fetching data for {selected_date} at {selected_time}...")

        # Fetch option chain data (Ensure this is correctly adjusted to your market data API)
        try:
            # Adjust to use the actual data fetch logic
            option_data = get_history(symbol="NIFTY", start=selected_date, end=selected_date)
            # Optionally filter the data based on time (if applicable to the data structure)
            
            # Placeholder for data display
            if not option_data.empty:
                st.write(option_data)
            else:
                st.write("No data available for the selected symbol.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
