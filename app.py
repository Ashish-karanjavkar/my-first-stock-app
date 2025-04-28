import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="📈 Option Chain Stats", layout="wide")

def fetch_option_chain(symbol="NIFTY"):
    try:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        response = session.get(url, headers=headers)
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def calculate_stats(data):
    records = data['records']['data']
    underlying_value = data['records']['underlyingValue']

    df = pd.json_normalize(records)

    call_oi = []
    put_oi = []
    strike_prices = []

    call_ltp = []
    put_ltp = []

    for record in records:
        if 'CE' in record and 'PE' in record:
            strike_prices.append(record['strikePrice'])
            call_oi.append(record['CE']['openInterest'])
            put_oi.append(record['PE']['openInterest'])
            call_ltp.append(record['CE']['lastPrice'])
            put_ltp.append(record['PE']['lastPrice'])

    call_oi = pd.Series(call_oi, index=strike_prices)
    put_oi = pd.Series(put_oi, index=strike_prices)

    pcr = round(put_oi.sum() / call_oi.sum(), 2)

    max_call_strike = call_oi.idxmax()
    second_max_call_strike = call_oi.drop(max_call_strike).idxmax()

    max_put_strike = put_oi.idxmax()
    second_max_put_strike = put_oi.drop(max_put_strike).idxmax()

    # Max Pain Calculation
    strikes = list(call_oi.index)
    pain = {}
    for strike in strikes:
        total = 0
        for k in strikes:
            call_loss = max(k - strike, 0) * call_oi.get(k, 0)
            put_loss = max(strike - k, 0) * put_oi.get(k, 0)
            total += call_loss + put_loss
        pain[strike] = total
    max_pain_strike = min(pain, key=pain.get)

    # Least Decay
    decay_df = pd.DataFrame({
        'strike': strike_prices,
        'call_ltp': call_ltp,
        'put_ltp': put_ltp
    })
    decay_df['total_ltp'] = decay_df['call_ltp'] + decay_df['put_ltp']
    least_decay_strike = decay_df.loc[decay_df['total_ltp'].idxmin()]['strike']

    stats = {
        "Spot": underlying_value,
        "Close": underlying_value,  # Close is not separately available; using Spot
        "PCR": pcr,
        "Max Call OI": max_call_strike,
        "2nd Max Call OI": second_max_call_strike,
        "Max Put OI": max_put_strike,
        "2nd Max Put OI": second_max_put_strike,
        "Max Pain": max_pain_strike,
        "KPP Max Pain": max_pain_strike,  # For now same as Max Pain
        "Expiry Close": max_pain_strike,  # Approx ATM/Max Pain
        "Least Decay": least_decay_strike,
        "Max Sale": max_call_strike,
        "Resistance": max_call_strike,
        "Overall Support": max_put_strike,
    }

    return stats

# Streamlit App
st.title("📈 Option Chain Statistics")

symbol = st.text_input("Enter Symbol (Default: NIFTY)", value="NIFTY")
btn = st.button("Fetch Option Chain Stats")

if btn:
    with st.spinner(f"Fetching data for {symbol}..."):
        data = fetch_option_chain(symbol)
        if data:
            stats = calculate_stats(data)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Spot", stats["Spot"])
                st.metric("Max Sale", stats["Max Sale"])
                st.metric("Overall Support", stats["Overall Support"])
                st.metric("Max Pain", stats["Max Pain"])

            with col2:
                st.metric("Close", stats["Close"])
                st.metric("Resistance", stats["Resistance"])
                st.metric("Max Put OI", stats["Max Put OI"])
                st.metric("KPP Max Pain", stats["KPP Max Pain"])

            with col3:
                st.metric("PCR", stats["PCR"])
                st.metric("Max Call OI", stats["Max Call OI"])
                st.metric("2nd Max Put OI", stats["2nd Max Put OI"])
                st.metric("Expiry Close", stats["Expiry Close"])

            with col4:
                st.metric("Least Decay", stats["Least Decay"])
                st.metric("2nd Max Call OI", stats["2nd Max Call OI"])

        else:
            st.error("Failed to fetch data.")
