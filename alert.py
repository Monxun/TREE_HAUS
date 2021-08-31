# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 00:40:47 2021

@author: mike
"""

import ccxt, yfinance
import pandas as pd
import pandas_ta as ta
import requests

####################################################################
# CRYPTO EXCHANGE DATA
exchange = ccxt.binance()

symbol = 'ETH/USDT'

bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='5m', limit=500)

df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

print(df)

####################################################################
# CRYPTO W/ INDICATORS

# adx = ta.adx(df['high'], df['low'], df['close'])

adx = df.ta.adx()
macd = df.ta.macd()
rsi = df.ta.rsi()

# call 'pd.concat([df, ...]) to combine the indicators to original df
df = pd.concat([df, adx, macd, rsi], axis=1)

last_row = df.iloc[-1]

WEBHOOK_URL = ""



if last_row['ADX_14'] >= 25:
    
    if last_row['DMP_14'] > last_row['DMN_14']:
        message = f"STRONG UPTREND!!! The ADX for {symbol} is {last_row['ADX_14']:.2f} +DI {last_row['DMP_14']} -DI {last_row['DMN_14']}"
        print(message)
        
    if last_row['DMN_14'] > last_row['DMP_14']:
        message = f"STRONG DOWNTREND!!! The ADX for {symbol} is {last_row['ADX_14']:.2f} +DI {last_row['DMP_14']} -DI {last_row['DMN_14']}"
        print(message)
        
    
if last_row['ADX_14'] < 25:
    message = f"NO TREND: The ADX for {symbol} is {last_row['ADX_14']:.2f} +DI {last_row['DMP_14']} -DI {last_row['DMN_14']}"
    print(message)
    
    
#INSERT MESSAGE INTO PAYLOAD 
payload = {
        "username": "alertbot",
        "content": message
        }
    
requests.post(WEBHOOK_URL, json=payload)


# ####################################################################
# # CRYPTO W/ INDICATORS AND CONDITIONALS

# # filter for just those rows below 30 'RSI_14'
# df_x_rsi = df[df['RSI_14'] < 30]
# print(df_x_rsi)

# ####################################################################
# # STOCK EXCHANGE DATA

# ticker = yfinance.Ticker("TSLA")
# df_2 = ticker.history(period="1y")

# print(df_2)

# ####################################################################
# # STOCK W/ INDICATORS
