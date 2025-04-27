import streamlit as st

st.title('📈 My First Stock App')
st.write('Welcome! This is my first app built with Python and Streamlit.')

st.header('Sample Stock')
stock = st.text_input('Enter Stock Symbol', 'AAPL')  # default AAPL
st.write(f'You entered: {stock}')
