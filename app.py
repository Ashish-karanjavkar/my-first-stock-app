import streamlit as st
import yfinance as yf
from nsepy import get_history
from datetime import datetime, date
import plotly.graph_objects as go  # For candlestick chart
import time  # For auto-refresh logic

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

    # Test fetching data for Nifty with a shorter date range for debugging
    try:
        nifty_options = get_history(symbol="NIFTY", index=True, start=date(2023, 1, 1), end=date.today())
        st.write("Data fetched successfully!")

        if not nifty_options.empty:
            # Show the first few rows to debug and check the data
            st.write("Data Sample:")
            st.write(nifty_options.head())

            # Calculate Spot (Last closing price)
            spot_price = nifty_options['Close'].iloc[-1]  # Last available closing price
            st.write(f"Spot Price: ₹{spot_price:.2f}")

            # Calculate Close Price (this is same as spot here)
            close_price = spot_price  # Could use any other closing price logic if required
            st.write(f"Close Price: ₹{close_price:.2f}")

            # PCR: Put-Call Ratio (total Put OI / total Call OI)
            total_call_oi = nifty_options[nifty_options['OptionType'] == 'CE']['OpenInterest'].sum()
            total_put_oi = nifty_options[nifty_options['OptionType'] == 'PE']['OpenInterest'].sum()
            pcr = total_put_oi / total_call_oi if total_call_oi != 0 else 0
            st.write(f"Put-Call Ratio (PCR): {pcr:.2f}")

            # Max Call OI (Maximum Open Interest for Call options)
            max_call_oi = nifty_options[nifty_options['OptionType'] == 'CE'].groupby('StrikePrice')['OpenInterest'].max().idxmax()
            st.write(f"Max Call OI Strike Price: ₹{max_call_oi:.2f}")

            # Max Put OI (Maximum Open Interest for Put options)
            max_put_oi = nifty_options[nifty_options['OptionType'] == 'PE'].groupby('StrikePrice')['OpenInterest'].max().idxmax()
            st.write(f"Max Put OI Strike Price: ₹{max_put_oi:.2f}")

            # Resistance: Can be derived from the max Call OI strike price
            resistance = max_call_oi
            st.write(f"Resistance: ₹{resistance:.2f}")

            # Support: Can be derived from the max Put OI strike price
            support = max_put_oi
            st.write(f"Support: ₹{support:.2f}")

            # Max Pain: The strike price with the maximum pain point (most options expiring worthless)
            # This would require some calculation based on open interest
            max_pain = nifty_options.groupby('StrikePrice')['OpenInterest'].sum().idxmin()
            st.write(f"Max Pain: ₹{max_pain:.2f}")

            # KPP Max Pain (you can add logic for calculating this if you have specific rules for it)
            kpp_max_pain = max_pain  # Placeholder (you can adjust this calculation based on your logic)
            st.write(f"KPP Max Pain: ₹{kpp_max_pain:.2f}")

            # Expiry Close: The closing price on expiry (take the latest close)
            expiry_close = nifty_options['Close'].iloc[-1]  # Placeholder, assuming it's the most recent
            st.write(f"Expiry Close: ₹{expiry_close:.2f}")

            # Least Decay: Find the strike price with the least change in Open Interest
            nifty_options['Decay'] = nifty_options['OpenInterest'].pct_change()  # Percentage change in OI
            least_decay_strike = nifty_options.groupby('StrikePrice')['Decay'].mean().idxmin()
            st.write(f"Least Decay Strike Price: ₹{least_decay_strike:.2f}")

        else:
            st.error("No data available for the selected symbol")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
