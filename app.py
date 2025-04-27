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
