# ====================
# Option Chain Stats Page
elif page == "Option Chain Stats":
    st.write("Fetching Option Chain Data...")

    # Dropdown for selecting the date (last 10 days)
    date_dropdown = st.selectbox("Select Date", pd.date_range(datetime.today() - pd.Timedelta(days=10), datetime.today()).strftime('%Y-%m-%d'))

    # Dropdown for selecting the time
    time_dropdown = st.selectbox("Select Time", ["09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", "15:00"])

    # Combine selected date and time into datetime object
    selected_datetime_str = f"{date_dropdown} {time_dropdown}"
    selected_datetime = datetime.strptime(selected_datetime_str, "%Y-%m-%d %H:%M")

    # Print the selected date and time for debugging
    st.write(f"Fetching data for {selected_datetime}...")

    # Fetch Option Chain Data (replace NIFTY with your symbol)
    try:
        nifty_options = get_history(symbol="NIFTY", index=True, start=date(2023, 1, 1), end=date.today())
        
        # Log the data to verify what you're getting
        st.write(f"Fetched data for NIFTY: {nifty_options.head()}")

        if not nifty_options.empty:
            # Calculate stats (you can modify this based on what you're looking for)
            call_oi = nifty_options[nifty_options['OptionType'] == 'CE']['OpenInterest'].sum()
            put_oi = nifty_options[nifty_options['OptionType'] == 'PE']['OpenInterest'].sum()

            # Display stats
            st.subheader("Option Chain Stats")
            st.write(f"Total Call Open Interest (OI): {call_oi}")
            st.write(f"Total Put Open Interest (OI): {put_oi}")
        else:
            st.error("No data available for the selected symbol.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
