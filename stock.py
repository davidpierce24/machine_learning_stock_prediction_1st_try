# import requests
# import matplotlib.pyplot as plt
# import math
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as py
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly


start = '2012-01-01'
today = date.today().strftime("%Y-%m-%d")

st.title("Stock Predictions")

callSign = st.text_input('Stock Ticker Symbol', value = 'tsla')
# callSign = input('Ticker?')
callSignDisplay = callSign.upper()

n_years = st.slider("Years of Prediction:", 1, 4)
period = n_years * 365


@st.cache
def load_data():
    data = yf.download(callSign, start, today)
    data.reset_index(inplace = True)
    return data

data = load_data()

st.subheader(callSignDisplay + ' data')
st.write(data.tail())

stock = [data['Open'], data['Close']]


fig = px.line(x= data['Date'], y=stock, title=callSignDisplay + " Stock Prices")
fig.update_layout(
    xaxis_title = "Time",
    yaxis_title = "Stock Price", 
    xaxis_rangeslider_visible =True
)
# fig.show()

st.plotly_chart(fig, use_container_width=True)


df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns = {"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods = period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())


st.write('Forecast Data')
fig2 = plot_plotly(m, forecast)
fig2.update_layout(
    xaxis_title = "Time",
    yaxis_title = "Stock Price", 
    xaxis_rangeslider_visible =True
)
st.plotly_chart(fig2)

st.write('Forecast Components')
fig3 = m.plot_components(forecast)
st.write(fig3)


# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={callSign}&outputsize=compact&apikey=1TON9HITVA38HZQ5'
# r = requests.get(url)
# data = r.json()

# priceData = []
# timeStamp = []
# count = 0
# for each in data["Weekly Time Series"]:
#     if count < 10:
#         timeStamp.append(each)
#         priceData.append(math.floor(int(float(data["Weekly Time Series"][each]["1. open"]))))
#         count +=1

# callSignDispaly = callSign.upper()
# chartTitle = callSignDispaly + " Stock Prices"
# plt.plot(timeStamp, priceData, color='red', marker='o')
# plt.title(chartTitle, fontsize=14)
# plt.xlabel('Time', fontsize=14)
# plt.ylabel('Price', fontsize=14)
# plt.grid(True)
# plt.show()

# df = pd.DataFrame({'time':timeStamp, 'price':priceData})
# fig = px.line(df, x="time", y="price", title=callSignDispaly + " Stock Prices") 
# # fig.show()


# st.plotly_chart(fig, use_container_width=True)


# st.write('The current movie title is', callSign)