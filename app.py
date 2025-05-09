
import streamlit as st
import pandas as pd
import requests

st.title("NSE Stock Scanner")

# Sample symbols (for full NSE you'd need to load from a file or API)
symbols = ["HINDUNILVR.NS", "MARUTI.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS",
    "NESTLEIND.NS", "BAJAJ-AUTO.NS", "SIEMENS.NS", "CIPLA.NS", "TITAN.NS",
    "DRREDDY.NS", "DIVISLAB.NS", "HEROMOTOCO.NS", "APOLLOHOSP.NS", "ADANIPORTS.NS",
    "BRITANNIA.NS", "TATACONSUM.NS", "GODREJCP.NS", "PIDILITIND.NS", "ABB.NS",
    "TRENT.NS", "LODHA.NS", "AMBUJACEM.NS", "AUROPHARMA.NS", "LUPIN.NS",
    "GLENMARK.NS", "NATCOPHARM.NS", "BIOCON.NS", "MARKSANS.NS", "CANFINHOME.NS",
    "CHOLAFIN.NS", "MANAPPURAM.NS", "L&TFH.NS", "AAVAS.NS", "IDFCFIRSTB.NS",
    "BANDHANBNK.NS", "LICHSGFIN.NS", "MUTHOOTFIN.NS", "BHEL.NS", "KALPATPOWR.NS",
    "GMRINFRA.NS", "KEC.NS", "ENGINERSIN.NS", "THERMAX.NS", "CUMMINSIND.NS",
    "ZENSARTECH.NS", "PERSISTENT.NS", "COFORGE.NS", "MPHASIS.NS", "LTIM.NS",
    "TECHM.NS", "HCLTECH.NS", "INFY.NS", "TCS.NS", "WIPRO.NS",
    "DMART.NS", "JUBLFOOD.NS", "PAGEIND.NS", "ABFRL.NS", "BERGEPAINT.NS",
    "COLPAL.NS", "DABUR.NS", "EMAMILTD.NS", "GODREJIND.NS", "HATSUN.NS",
    "HAWKINCOOK.NS", "JYOTHYLAB.NS", "KAYA.NS", "MARICO.NS", "PGHH.NS",
    "RADICO.NS", "TATACHEM.NS", "VBL.NS", "VGUARD.NS", "WHIRLPOOL.NS",
    "ZYDUSWELL.NS", "AARTIIND.NS", "ATUL.NS", "DEEPAKNTR.NS", "FLUOROCHEM.NS",
    "NAVINFLUOR.NS", "PIIND.NS", "SRF.NS", "UPL.NS", "VINATIORGA.NS",
    "ALKYLAMINE.NS", "BALAMINES.NS", "CAMLINFINE.NS", "FINEORG.NS", "GALAXYSURF.NS",
    "LXCHEM.NS", "NEOGEN.NS", "PRIVISCL.NS", "ROSSARI.NS", "TATVA.NS",
    "VIKASECO.NS", "YASHO.NS"
]
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
