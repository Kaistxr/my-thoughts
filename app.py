import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd


st.title("Kai's Blog ")
st.markdown("Sharing market insights, charts, and thoughts.")


category = st.sidebar.radio("Choose category:", ["Market News", "Stock Picks", "Options Markets"])
market_news_posts = {
    "July 2nd Update": {
        "ticker": "TSLA",
        "commentary": """
        For Mrs Maddy
        Tesla** shares rose **4.3%** after reporting **443,956 Q2 deliveries**, slightly above expectations. 
        While EV sales dipped ~5% year-over-year, strong performance in the **energy storage division** signalled a shift toward business diversification.
        """,
    },
    "July 2025 Market Recap": {
        "ticker": "AAPL",
        "commentary": """
        Apple has shown strong resilience in July, with steady price gains amid macroeconomic uncertainty. 
        Here's a look at the last month's closing prices.
        """,
    },
    "Tech Sector Outlook": {
        "ticker": "MSFT",
        "commentary": """
        Microsoft continues to lead in cloud growth. Despite market volatility, MSFT's fundamentals remain solid.
        Let's check the price trend over the last 3 months.
        """,
    },
    "Forex Focus: EUR/USD": {
        "ticker": "EURUSD=X",
        "commentary": """
        The EUR/USD pair has experienced volatility due to recent ECB policy statements.  
        Here is the daily closing price over the last 6 months.
        """,
    },
}

# Sample data for Stock Picks
stock_picks = {
    "Apple (AAPL)": {
        "ticker": "AAPL",
        "reason": "Strong product pipeline and solid earnings growth expected next quarter.",
    },
    "Tesla (TSLA)": {
        "ticker": "TSLA",
        "reason": "Leading EV market share with aggressive expansion plans.",
    },
    "Amazon (AMZN)": {
        "ticker": "AMZN",
        "reason": "Dominant cloud business with long-term growth potential.",
    },
}


if category == "Market News":
    st.header("Market News")
    selected_post = st.selectbox("Choose a blog post:", list(market_news_posts.keys()))
    post = market_news_posts[selected_post]

    st.subheader(selected_post)
    st.write(post["commentary"])

    data = yf.download(post["ticker"], period="6mo", interval="1d")
    if data.empty:
        st.error("No data found for this ticker.")
    else:
        fig = px.line(x=data.index, y=data["Close"].squeeze(), title=f"{post['ticker']} Closing Prices (6 months)")
        st.plotly_chart(fig)

elif category == "Stock Picks":
    st.header("My Stock Picks") 
    selected_pick = st.selectbox("Select a stock pick:", list(stock_picks.keys()))
    pick = stock_picks[selected_pick]

    st.subheader(selected_pick)
    st.write(pick["reason"])

    data = yf.download(pick["ticker"], period="1y", interval="1d")
    if data.empty:
        st.error("No data found for this ticker.")
    else:
        fig = px.line(x=data.index, y=data["Close"].squeeze(), title=f"{pick['ticker']} Closing Prices (1 year)")
        st.plotly_chart(fig)

elif category == "Options Markets":
    ticker_input = st.text_input("Enter ticker symbol (e.g. AAPL, TSLA):", "AAPL")
    ticker = yf.Ticker(ticker_input)
    st.header(f"Options Market Data for {ticker_input.upper()}")
    spot_price = ticker.history(period="1d")['Close'][-1]

    st.markdown(f"**Current Spot Price:** ${spot_price:.2f}")

    options_dates = ticker.options
    if options_dates:
        expiry = st.selectbox("Choose expiry date", options_dates)

        opt_chain = ticker.option_chain(expiry)
        calls = opt_chain.calls[['contractSymbol', 'strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility', 'volume', 'openInterest']]
        puts = opt_chain.puts[['contractSymbol', 'strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility', 'volume', 'openInterest']]

        calls.columns = ['Call Symbol', 'Strike', 'Last Price', 'Bid', 'Ask', 'IV', 'Volume', 'Open Interest']
        puts.columns = ['Put Symbol', 'Strike', 'Last Price', 'Bid', 'Ask', 'IV', 'Volume', 'Open Interest']

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Calls")
            st.dataframe(calls.style.format({
                'Last Price': '${:.2f}',
                'Bid': '${:.2f}',
                'Ask': '${:.2f}',
                'IV': '{:.2%}',
                'Volume': '{:,}',
                'Open Interest': '{:,}'
            }))

        with col2:
            st.subheader("Puts")
            st.dataframe(puts.style.format({
                'Last Price': '${:.2f}',
                'Bid': '${:.2f}',
                'Ask': '${:.2f}',
                'IV': '{:.2%}',
                'Volume': '{:,}',
                'Open Interest': '{:,}'
            }))
    else:
        st.write("No options data available for this ticker.")



st.markdown("---")
