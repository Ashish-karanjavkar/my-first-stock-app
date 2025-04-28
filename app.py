import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import datetime

# --- FUNCTIONS ---

@st.cache_data
def fetch_stock_data(symbol="^NSEI"):
    today = datetime.date.today()
    ten_days_ago = today - datetime.timedelta(days=10)
    df = yf.download(symbol, start=ten_days_ago, end=today)
    return df

@st.cache_data
def fetch_option_chain(symbol="NIFTY", expiry_date=None):
    try:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        session = requests.Session()
        response = session.get(url, headers=headers)
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# --- SIDEBAR ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Stock Tracker", "Option Chain Stats", "Past 10 Days Data"])

# --- PAGE 1: Stock Tracker ---
if page == "Stock Tracker":
    st.title("📈 Stock Price Tracker")

    symbol = st.text_input("Enter Symbol (e.g., ^NSEI for Nifty50)", "^NSEI")

    data = fetch_stock_data(symbol)

    if not data.empty:
        st.subheader(f"Stock Data for {symbol}")
        st.line_chart(data['Close'])
    else:
        st.warning("No data available.")

# --- PAGE 2: Option Chain Stats ---
elif page == "Option Chain Stats":
    st.title("📊 Option Chain Stats")

    st.subheader("Select Parameters")
    symbol = st.text_input("Enter Index Symbol", "NIFTY")
    
    # Date selection (not actually used to pull different data — NSE API is live only)
    date_dropdown = st.selectbox("Select Date", pd.date_range(datetime.date.today() - pd.Timedelta(days=10), datetime.date.today()).strftime('%Y-%m-%d'))
    selected_time = st.selectbox(
        "Select Time",
        [f"{hour:02d}:{minute:02d}" for hour in range(9, 16) for minute in (0, 15, 30, 45)]
    )

    st.write(f"Fetching data for {symbol} on {date_dropdown} at {selected_time}...")

    option_data = fetch_option_chain(symbol)

    if option_data:
        st.success("Data fetched successfully!")
        
        spot_price = option_data['records']['underlyingValue']
        st.metric("Spot Price", f"{spot_price:.2f}")

        # --- Calculate basic stats ---
        calls = []
        puts = []

        for item in option_data['records']['data']:
            if 'CE' in item:
                calls.append(item['CE'])
            if 'PE' in item:
                puts.append(item['PE'])

        call_df = pd.DataFrame(calls)
        put_df = pd.DataFrame(puts)

        max_call_oi = call_df.loc[call_df['openInterest'].idxmax()]
        max_put_oi = put_df.loc[put_df['openInterest'].idxmax()]
        second_max_call_oi = call_df.nlargest(2, 'openInterest').iloc[-1]
        second_max_put_oi = put_df.nlargest(2, 'openInterest').iloc[-1]

        pcr = put_df['openInterest'].sum() / call_df['openInterest'].sum()

        # --- Display 4 Columns ---
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Spot", f"{spot_price:.2f}")
            st.metric("Close", f"{spot_price:.2f}")  # You can update this separately if you want
            st.metric("PCR", f"{pcr:.2f}")

        with col2:
            st.metric("Resistance", f"{max_call_oi['strikePrice']} (Max Call OI)")
            st.metric("2nd Resistance", f"{second_max_call_oi['strikePrice']} (2nd Max Call OI)")

        with col3:
            st.metric("Support", f"{max_put_oi['strikePrice']} (Max Put OI)")
            st.metric("2nd Support", f"{second_max_put_oi['strikePrice']} (2nd Max Put OI)")

        with col4:
            st.metric("Max Pain", "N/A (advanced calc)")
            st.metric("KPP Max Pain", "N/A")
            st.metric("Expiry Close", "N/A")
            st.metric("Least Decay", "N/A")
        
        st.info("Note: Max Pain, KPP Max Pain, Expiry Close, Least Decay need more advanced calculations if you want real values.")

    else:
        st.warning(f"No data available for {symbol} on {date_dropdown} at {selected_time}.")

# --- PAGE 3: Past 10 Days Data ---
elif page == "Past 10 Days Data":
    st.title("📜 Past 10 Days NIFTY Open/Close")

    symbol = "^NSEI"

    data = fetch_stock_data(symbol)

    if not data.empty:
        past_data = data[['Open', 'Close']].copy()
        past_data.index = past_data.index.strftime('%Y-%m-%d')
        st.table(past_data)
    else:
        st.warning(f"No data available for {symbol} in the past 10 days.")
