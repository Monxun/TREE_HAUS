import streamlit as st
from multiapp import MultiApp
from pages import home, dash, analysis, da, fundamentals, corr # import your application pages here

app = MultiApp()

st.sidebar.title('TREE_HAUS')
st.sidebar.image('logo.png')
st.sidebar.header('Navigation')
# Import all your application views here

app.add_app("About", home.app)
app.add_app("Fundamentals", fundamentals.app)
app.add_app("Sentiment Tracker", dash.app)
app.add_app("Technical Analysis", analysis.app)
app.add_app('Data Analysis', da.app)
app.add_app('Correlation', corr.app)


# The main app
app.run()

st.sidebar.write('MADE BY: Monxun')