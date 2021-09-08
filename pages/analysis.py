import base64
import requests
import talib
import datetime as dt
import pandas as pd
from yahoo_fin import stock_info as si
import datetime as dt
import streamlit as st
import yfinance as yf
import mplfinance as mf

yf.pdr_override()

def app():

    st.title('Technical Analysis')
    st.sidebar.write('Enter Ticker and date below')

    today = dt.date.today()
    ticker_type = st.sidebar.radio('', ['Stock', 'Crypto'])

    def user_input_features():

        if ticker_type == 'Stock': 
            ticker = st.sidebar.text_input("Ticker", 'AAPL')
        else:
            ticker_crypto = st.sidebar.text_input("Ticker", 'BTC')
            base = st.sidebar.text_input("Base Currency", 'USD')
            ticker = st.sidebar.text_input("Ticker", f'{ticker_crypto}-{base}')

        start_date = st.sidebar.text_input("Start Date", '2019-01-01')
        end_date = st.sidebar.text_input("End Date", f'{today}')
        return ticker, start_date, end_date


    symbol, start, end = user_input_features()


    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    # Read data
    
    data = yf.download(symbol,start,end)
        

    #################################################################
    # INDICATOR METHOD

    def get_indicators(df):
        indicators_dispatcher = {
            'adx': df.ta.adx,
            'macd': df.ta.macd,
            'rsi': df.ta.rsi,
            'sma': df.ta.sma,
            'ema': df.ta.ema,
            'squeeze': df.ta.squeeze,
            'rvi': df.ta.rvi,
            'vwap': df.ta.vwap,
            'obv': df.ta.obv,
            'bbands': df.ta.bbands,
            'vwma': df.ta.vwma,
            'ohlc4': df.ta.ohlc4,
            'fwma': df.ta.fwma,
            'linreg': df.ta.linreg,
            'supertrend': df.ta.supertrend
        }

        print(indicator_flags['adx'])
        indicator_que = [key for (key, value) in indicator_flags.items() if value == True]
        print(indicator_que)

        for i in indicator_que:
            indicator = indicators_dispatcher[i]()
            df = pd.concat([df, indicator], axis=1)

        return df
    

        ####################
    # INDICATOR CHECKBOX

    st.sidebar.write('_' * 40)

    with st.sidebar.expander("Indicators"):

        sma_1 = int(st.text_input('SMA - Blue', value=10))
        sma_2 = int(st.text_input('SMA - Pink', value=20))
        st.write('-' * 40)
        st.subheader('select indicators:')
        adx_box = st.checkbox('ADX')
        macd_box = st.checkbox('MACD')
        rsi_box = st.checkbox('RSI')
        sma_box = st.checkbox('SMA')
        ema_box = st.checkbox('EMA')
        squeeze_box = st.checkbox('Squeeze')
        rvi_box = st.checkbox('RVI')
        vwap_box = st.checkbox('VWAP')
        obv_box = st.checkbox('OBV')
        bbands_box = st.checkbox('Bollinger Bands')
        vwma_box = st.checkbox('VWMA')
        ohlc4_box = st.checkbox('OHLC4 Avg.')
        fwma_box = st.checkbox('FWMA')
        linreg_box = st.checkbox('Linear Regression')
        supertrend_box = st.checkbox('Supertrend')


        indicator_flags = {
            'adx': adx_box,
            'macd': macd_box,
            'rsi': rsi_box,
            'sma': sma_box,
            'ema': ema_box,
            'squeeze': squeeze_box,
            'rvi': rvi_box,
            'vwap': vwap_box,
            'obv': obv_box,
            'bbands': bbands_box,
            'vwma': vwma_box,
            'ohlc4': ohlc4_box,
            'fwma': fwma_box,
            'linreg': linreg_box,
            'supertrend': supertrend_box
        }

    
    #################################################################
    
    st.write('')
    st.title(symbol)

    fig = mf.plot(data, mav = (sma_1, sma_2), type = 'candle', volume = True)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)

    
        