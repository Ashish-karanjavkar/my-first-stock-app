import streamlit as st

# Title of the app
st.title('📈 Stock Price Tracker (India)')

# Short description
st.write('Welcome! Track latest live stock prices from NSE and BSE markets.')

# Input box for user to type stock symbol
stock = st.text_input('Enter Stock Symbol (Example: RELIANCE, TCS, INFY)')

# Show what user typed
if stock:
    st.write(f"You entered: {stock}")
