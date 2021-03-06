## streamlit_multipage_financial_dashboard  

Created a financial dashboard to testdrive streamlit's python based dashboard building framework.

## Dashboard screenshots

![Financial dashboard built with streamlit](./dash_preview.png?raw=true "Preview of the built dashboard")


## How to Run

1. Clone the repository:
```
$ git clone git@github.com:Monxun/TREE_HAUS.git
$ cd TREE_HAUS
```
2. Install dependencies:
```
$ pip install -r requirements.txt
```
3. Start the application:
```
$ streamlit run app.py
```

## How to add your pages to the dashboard

1. Add a new python file in `pages/` folder with a function named app.

```
# pages/new_page.py

import streamlit as st

def app():
    st.title('New Page')
```

2. Import the view to `app.py`

```
from pages import new_page # import your application pages here

app = MultiApp()

# Add all your application here
app.add_app("New Page", new_page.app)

```

3. Display the dashboard

```
$ streamlit run app.py

```

## References:

Used the python code and ideas for project structure from the below resources.

https://github.com/upraneelnihar/streamlit-multiapps

https://towardsdatascience.com/creating-a-finance-web-app-in-3-minutes-8273d56a39f8

https://github.com/hackingthemarkets/fullstack-trading-app

## Streamlit cheatsheet

https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

