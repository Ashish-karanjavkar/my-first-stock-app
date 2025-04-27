import streamlit as st
from datetime import datetime, timedelta
import nsepy
from nsepy.derivatives import get_expiry_date
import pandas as pd

# Function to fetch data based on selected date and time
def get_option_data(symbol, selected_date, selected_time):
    try:
        st.write(f"Fetching data for {selected_date} at {selected_time}...")

        # Ensure date is within market hours
        market_open_time = datetime.strptime(f"{selected_date} 09:15", "%Y-%m-%d %H:%M")
        market_close_time = datetime.strptime(f"{selected_date} 15:30", "%Y-%m-%d %H:%M")

        selected_time_dt = datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M")

        if selected_time_dt < market_open_time or selected_time_dt > market_close_time:
            st.write("The selected time is outside market hours.")
            return
        
        # Fetch data for NIFTY using NSEpy API
        nifty_data = nsepy.get_history(symbol="NIFTY", start=selected_date, end=selected_date)
        
        if nifty_data.empty:
            st.write(f"No data available for {symbol} on {selected_date}.")
            return
        else:
            st.write(f"Data fetched successfully for {symbol} on {selected_date}.")
            st.write(nifty_data)

            # Example: Fetching the Call Option data for NIFTY
            # Adjust the strike price as necessary
            strike_price = 9500  # Example strike price
            expiry_date = get_expiry_date(selected_date)
            option_data = nsepy.get_history(symbol="NIFTY", start=selected_date, end=selected_date, option_type='CE', strike_price=strike_price, expiry_date=expiry_date)

            if option_data.empty:
                st.write(f"No options data available for NIFTY on {selected_date}.")
            else:
                st.write("Options data fetched successfully.")
                st.write(option_data)

    except Exception as e:
        st.write(f"Error fetching data: {e}")

# Add a dropdown for the date selection (last 10 days)
date_options = [datetime.today() - timedelta(days=i) for i in range(10)]
date_str = [date.strftime("%Y-%m-%d") for date in date_options]
selected_date = st.selectbox("Select Date", date_str)

# Add a dropdown for time (available hours for NSE market: 09:15 to 15:30)
time_options = [f"{h:02}:{m:02}" for h in range(9, 16) for m in [0, 15, 30, 45]]
selected_time = st.selectbox("Select Time", time_options)

# When the user clicks the "Fetch Data" button
if st.button("Fetch Option Data"):
    get_option_data("NIFTY", selected_date, selected_time)
