import ccxt
import base64
import requests
import pandas as pd
import pandas_ta as ta
import streamlit as st
import plotly.graph_objects as go



# BACKGROUND IMAGES
####################################################################################################################

main_bg = "background.jpg"
main_bg_ext = "jpg"

side_bg = "side.jpg"
side_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)

####################################################################################################################
# INITIALIZE GUI

st.sidebar.title("TREE_HAUS")
st.sidebar.write("by: monxun")

symbol_type = st.sidebar.radio('type', ["CRYPTO","STOCK"])

if "CRYPTO" in symbol_type:
    st.sidebar.write("enter currency pair")
    symbol = st.sidebar.text_input('format: XXX/XXX', value='BTC/USDT')
else:
    st.sidebar.write("enter stock symbol")
    symbol = st.sidebar.text_input('format: XXXX', value='GME')


timeframe = st.sidebar.selectbox('timeframe', ['1d','1m','1y'])

limit = st.sidebar.number_input('limit', value=500)

run_flag = st.sidebar.button('RUN')

####################################################################
# CRYPTO EXCHANGE DATA FUNCTION
def crypto(symbol=symbol, timeframe='5m', limit=500):

    exchange = ccxt.binance()

    bars = exchange.fetch_ohlcv(f'{symbol}', timeframe=timeframe, limit=limit)

    df_crypto = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_crypto['time'], open=df_crypto['open'], high=df_crypto['high'], low=df_crypto['low'], close=df_crypto['close']))

    st.plotly_chart(fig)
    st.dataframe(df_crypto)
    


####################################################################
# CRYPTO EXCHANGE DATA FUNCTION
def stock(symbol=symbol, period="1y"):

    ticker = yfinance.Ticker(f"{symbol}")
    df_stock = ticker.history(period=period)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_stock['time'], open=df_stock['open'], high=df_stock['high'], low=df_stock['low'], close=df_stock['close']))

    st.plotly_chart(fig)

    st.dataframe(df_stock)
    


####################################################################
# MAKE GRAPHS / WRITE DATA

while run_flag:
    if "CRYPTO" in symbol_type:
        crypto(symbol, timeframe, limit)
        run_flag=False
    else:
        stock(symbol, period=timeframe)
        run_flag=False


####################################################################
# CRYPTO W/ INDICATORS

# adx = ta.adx(df['high'], df['low'], df['close'])

# adx = df.ta.adx()
# macd = df.ta.macd()
# rsi = df.ta.rsi()

# # call 'pd.concat([df, ...]) to combine the indicators to original df
# df = pd.concat([df, adx, macd, rsi], axis=1)

# last_row = df.iloc[-1]