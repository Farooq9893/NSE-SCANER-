
import streamlit as st
import pandas as pd
import requests

st.title("NSE Stock Scanner")

# Sample symbols (for full NSE you'd need to load from a file or API)
symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
API_KEY = "0PKFQNZFI3Z49YZJ"

def get_stock_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": f"{symbol}.NS",
        "interval": "5min",
        "apikey": API_KEY
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    try:
        prices = data["Time Series (5min)"]
        df = pd.DataFrame(prices).T.astype(float)
        df["9 EMA"] = df["4. close"].ewm(span=9).mean()
        df["Volume Avg"] = df["5. volume"].rolling(9).mean()
        latest = df.iloc[-1]
        if (latest["4. close"] > latest["9 EMA"]) and (latest["5. volume"] > 1.5 * latest["Volume Avg"]):
            return symbol
    except Exception:
        pass
    return None

selected = [get_stock_data(sym) for sym in symbols]
selected = [s for s in selected if s]

st.subheader("Matching Stocks:")
if selected:
    for s in selected:
        st.write(s)
else:
    st.write("No stocks matched the criteria.")
