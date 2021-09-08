import streamlit as st
import pandas as pd
import numpy as np
import requests
import tweepy
import config
from requests.api import options


def app():

    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    traders_list = list(config.TWITTER_USERNAMES)

    st.title('SENTIMENT TRACKER')

    col1, col2, col3 = st.columns(3)

    with col1:

        st.title('___Target___')

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

        st.title('___Traders___')

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

        st.title('___StockTwits___')

        st.subheader('Symbol')

        stock_symbol = st.text_input("", value='GME', max_chars=5)

        r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{stock_symbol}.json")

        data = r.json()

        for message in data['messages']:
            st.image(message['user']['avatar_url'])
            st.write(message['user']['username'])
            st.write(message['created_at'])
            st.write(message['body'])

 