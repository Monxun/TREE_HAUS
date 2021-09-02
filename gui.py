import ccxt
import base64
import requests
import pandas as pd
import pandas_ta as ta
import streamlit as st
import plotly.graph_objects as go
import yfinance

symbol=''

# METHODS ##########################################################
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
# STOCK EXCHANGE DATA FUNCTION
def stock(symbol=symbol, period="1y"):

    ticker = yfinance.Ticker(f"{symbol}")
    df_stock = ticker.history(period=period)

    # fig = go.Figure()
    # fig.add_trace(go.Candlestick(x=df_stock['DateTime'], open=df_stock['Open'], high=df_stock['High'], low=df_stock['Low'], close=df_stock['Close']))

    # st.plotly_chart(fig)

    st.dataframe(df_stock)



# GUI ##############################################################
####################################################################
# INITIALIZE GUI

st.sidebar.image('logo.png')

st.sidebar.title("TREE_HAUS")
st.sidebar.write("by: monxun")

screen_type = st.sidebar.radio('PHASE', ["KRONOS - recon","ORIKLE - forecasting", "HERMEZ - trading AI"])

st.sidebar.write('-' * 40)


#KRONOS############################################################
if "KRONOS" in screen_type:

    screen = st.sidebar.selectbox("View", ('Analysis', 'Backtesting', 'Strategy', 'Twitter', 'Sentiment', '--select--'), index=5)
    st.sidebar.write('-' * 40)

    ###############################################################
    # BACKGROUND IMAGES
    main_bg = "background_1.jpg"
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

#ORIKLE############################################################
elif "ORIKLE" in screen_type:

    screen = st.sidebar.selectbox("View", ('ML', 'AI', 'Auto_ML', 'Time-Series Pipeline', 'Sentiment / Data Forecasting', 'AI Enhanced Backtesting'), index=0)
    st.sidebar.write('-' * 40)

    ###############################################################
    # BACKGROUND IMAGES
    main_bg = "background_2.jpg"
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

#HERMEZ###########################################################
elif "HERMEZ" in screen_type:

    screen = st.sidebar.selectbox("View", ('Strategy Selection', 'Deploymnet', 'Performance', 'Network', 'Outlook'), index=0)
    st.sidebar.write('-' * 40)

    ##############################################################
    # BACKGROUND IMAGES
    main_bg = "background_3.jpg"
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

#################################################################
# ANALYSIS PARAMETERS

# SIDEBAR
if screen == 'Analysis':

    st.sidebar.title(screen)

    symbol_type = st.sidebar.radio('type', ["CRYPTO","STOCK"])

    if "CRYPTO" in symbol_type:
        st.sidebar.write("enter currency pair")
        symbol = st.sidebar.text_input('format: XXX/XXX', value='BTC/USDT')

    else:
        st.sidebar.write("enter stock symbol")
        symbol = st.sidebar.text_input('format: XXXX', value='GME')

################
# TIME SELECTION
    if "STOCK" in symbol_type:
        time_cursor = st.sidebar.radio('choose:', ["date","period"])

        date_flag = False
    else:
        time_cursor = "timeframe"

    
    if 'date' in time_cursor and symbol_type == 'STOCK':
        timeframe_a = st.sidebar.date_input('start date')
        timeframe_b = st.sidebar.date_input('end date')
        date_flag = True

    else:
        timeframe = st.sidebar.selectbox('period', ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y','10y'])

    interval = st.sidebar.selectbox('interval', ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1hr', '1d', '1wk', '1mo', '3mo'])
    limit = st.sidebar.number_input('limit', value=500)

####################
# INDICATOR CHECKBOX
    indicator_container = st.sidebar.checkbox('add indicators')

    if indicator_container:
        st.sidebar.write('-' * 40)
        st.sidebar.subheader('select indicators:')
        adx_box = st.sidebar.checkbox('ADX')
        macd_box = st.sidebar.checkbox('MACD')
        rsi_box = st.sidebar.checkbox('RSI')

        indicator_flags = {
            'adx': adx_box,
            'macd': macd_box,
            'rsi': rsi_box
        }

    


#################################################################
# RUN ANALYSIS
    run_flag = st.sidebar.button('RUN')
    while run_flag:
        if "CRYPTO" in symbol_type:
            crypto(symbol, timeframe, limit)
            indicator_que = [i for i in indicator_flags if i == True]
            st.sidebar.write(indicator_que)
            run_flag=False

        elif date_flag:
            stock(symbol, start=timeframe_a, end=timeframe_b, interval=interval)
            indicator_que = [i for i in indicator_flags if i == True]
            st.sidebar.write(indicator_que)
            run_flag=False

        else:
            stock(symbol, period=timeframe, interval=interval)
            indicator_que = [i for i in indicator_flags if i == True]
            st.sidebar.write(indicator_que)
            run_flag=False

#################################################################






    
###################################################################
# MAKE GRAPHS / WRITE DATA




###################################################################
# CRYPTO W/ INDICATORS

# adx = ta.adx(df['high'], df['low'], df['close'])

# adx = df.ta.adx()
# macd = df.ta.macd()
# rsi = df.ta.rsi()

# # call 'pd.concat([df, ...]) to combine the indicators to original df
# df = pd.concat([df, adx, macd, rsi], axis=1)

# last_row = df.iloc[-1]