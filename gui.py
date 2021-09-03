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
# GET INDICATORS FUNCTION

def get_indicators(indicator_que, df):

    indicators_dispatcher = {
        'adx': df.ta.adx,
        'macd': df.ta.macd,
        'rsi': df.ta.rsi
    }

    for i in indicator_que:
        indicator = indicators_dispatcher[i]()
        df = pd.concat([df, indicator], axis=1)

    df = df.dropna() # optional 

    return df

    
####################################################################
# CRYPTO EXCHANGE DATA FUNCTION

def crypto(symbol=symbol, timeframe='5m', limit=500):

    exchange = ccxt.binance()

    bars = exchange.fetch_ohlcv(f'{symbol}', timeframe=timeframe, limit=limit)

    df_crypto = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume']) ### TODO!!!!! CONVERT TIME to DATETIME OR SOMETHING ELSE USABLE
 

    #CHARTS
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_crypto['time'], open=df_crypto['open'], high=df_crypto['high'], low=df_crypto['low'], close=df_crypto['close']))

    st.plotly_chart(fig)

    #INDICATORS
    indicator_que = [key for key in indicator_flags if key]
    df_crypto = get_indicators(indicator_que, df=df_crypto)
    # get_indicators(indicator_que, df=df_crypto)
    st.dataframe(df_crypto)

    last_row = df_crypto.iloc[-1]

    st.write(last_row)


####################################################################
# STOCK EXCHANGE DATA FUNCTION

def stock(symbol=symbol, period="1y"):

    ticker = yfinance.Ticker(f"{symbol}")
    df_stock = ticker.history(period=period)

    #CHARTS
    st.line_chart(df_stock)

    #INDICATORS
    indicator_que = [key for key in indicator_flags if key]
    df_stock = get_indicators(indicator_que, df=df_stock)
    st.dataframe(df_stock)

    last_row = df_crypto.iloc[-1]

    st.write(last_row)


# GUI ##############################################################
####################################################################
# INITIALIZE GUI

st.sidebar.image('logo.png')

st.sidebar.title("TREE_HAUS")
st.sidebar.write("by: monxun")

screen_type = st.sidebar.radio('', ["KRONOS - recon","ORIKLE - forecasting", "HERMEZ - trading AI"])

st.sidebar.write('-' * 40)


#KRONOS############################################################
if "KRONOS" in screen_type:
    
    screen = st.sidebar.selectbox("", ('Analysis', 'Backtesting', 'Strategy', 'Twitter', 'Sentiment', '--select--'), index=5)


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

    screen = st.sidebar.selectbox("View", ('ML', 'AI', 'Auto_ML', 'Time-Series Pipeline', 'Sentiment / Data Forecasting', 'AI Enhanced Backtesting', '--select one--'), index=6)

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

    screen = st.sidebar.selectbox("View", ('Strategy Selection', 'Deploymnet', 'Performance', 'Network', 'Outlook', '--select one--'), index=5)

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



# KRONOS
#############################################################################################################################################################################################################################################################################
# ANALYSIS PARAMETERS

if screen == 'Analysis':

    col1, col2 = st.columns([2, 3])

    with col1:

        st.title(screen)

        symbol_type = st.radio('type', ["CRYPTO","STOCK"])
        st.write('-' * 40)

    
        st.subheader('Symbol')
        if "CRYPTO" in symbol_type:
            symbol = st.text_input('format: XXX/XXX', value='BTC/USDT')

        else:
            st.write("enter stock symbol")
            symbol = st.text_input('format: XXXX', value='GME')

        ################
        # TIME SELECTION

        st.write('-' * 40)
        st.subheader('Time')

        if "STOCK" in symbol_type:
            time_cursor = st.radio('choose:', ["date","period"])

            date_flag = False
        else:
            time_cursor = "timeframe"

        
        if 'date' in time_cursor and symbol_type == 'STOCK':
            timeframe_a = st.date_input('start date')
            timeframe_b = st.date_input('end date')
            date_flag = True

        else:
            timeframe = st.selectbox('period', ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y','10y'])

        interval = st.selectbox('interval', ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1hr', '1d', '1wk', '1mo', '3mo'])
        limit = st.number_input('limit', value=500)

        ####################
        # INDICATOR CHECKBOX

        with st.expander("Indicators"):

            st.write('-' * 40)
            st.subheader('select indicators:')
            adx_box = st.checkbox('ADX')
            macd_box = st.checkbox('MACD')
            rsi_box = st.checkbox('RSI')

            indicator_flags = {
                'adx': adx_box,
                'macd': macd_box,
                'rsi': rsi_box
            }


        #################################################################
        # RUN ANALYSIS
    
    with col2:

        st.write('')
        st.write('')
        if "CRYPTO" in symbol_type:
            crypto(symbol, timeframe, limit)
            run_flag=False

        elif date_flag:
            stock(symbol, start=timeframe_a, end=timeframe_b, interval=interval)
            run_flag=False

        else:
            stock(symbol, period=timeframe, interval=interval)
            run_flag=False


#############################################################################################################################################################################################################################################################################
# Twitter

if screen == 'Twitter':

    import tweepy
    import config 

    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    traders_list = list(config.TWITTER_USERNAMES)

    # SIDEBAR
    st.sidebar.write('-' * 40)
    st.sidebar.subheader('Objective:')
    objective = st.sidebar.radio('', ['feeds', 'backtest'])

    
  
    if objective == 'feeds':

        col1, col2, col3 = st.columns([4, 5, 4])

        with col1:

            st.title('Target')

            st.subheader('username:')
            username = st.text_input('', value='ohheytommy')

            user = api.get_user(username)
            tweets = api.user_timeline(username)

            user_add = st.button('ADD TRADER')
            if user_add:
                traders_list = traders_list.append(username)

            st.subheader(username)
            st.image(user.profile_image_url)

            for tweet in tweets:
                if '$' in tweet.text:
                    words = tweet.text.split(' ')
                    for word in words:
                        if word.startswith('$') and word[1:].isalpha():
                            symbol = word[1:]
                            st.write(symbol)
                            st.write(tweet.text)
                            st.image(f"https://finviz.com/chart.ashx?t={symbol}")

        with col2:

            st.title('Traders')

            st.subheader('List')

            st.write('')
            st.write('')
            with st.expander("See traders"):
                for i in traders_list:
                    st.write(i)

            for username in traders_list:
                user = api.get_user(username)
                tweets = api.user_timeline(username)

                st.subheader(username)
                st.image(user.profile_image_url)
                
                for tweet in tweets:
                    if '$' in tweet.text:
                        words = tweet.text.split(' ')
                        for word in words:
                            if word.startswith('$') and word[1:].isalpha():
                                symbol = word[1:]
                                st.write(symbol)
                                st.write(tweet.text)
                                st.image(f"https://finviz.com/chart.ashx?t={symbol}")

        with col3:

            st.title('Stocktwits')

            st.subheader('Symbol')

            stock_symbol = st.text_input("", value='GME', max_chars=5)

            r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{stock_symbol}.json")

            data = r.json()

            for message in data['messages']:
                st.image(message['user']['avatar_url'])
                st.write(message['user']['username'])
                st.write(message['created_at'])
                st.write(message['body'])

