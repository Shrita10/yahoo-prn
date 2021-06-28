# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 23:42:01 2020

@author: Shrita
"""

import streamlit as st
st.header('Yahoo-PRNewswire stocks')
st.write('Time series of Stock symbols')
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

page = requests.get("https://www.prnewswire.com/news-releases/")
soup = BeautifulSoup(page.content, 'html.parser')
Result = soup.find_all('a',class_ ="news-release")
url1 = "https://www.prnewswire.com/{}"
def html_page_str(url):
    headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'    
    }
    response = requests.get(url,headers=headers)
    response_str = '' 
    if response.status_code == 200:
        response_str = response.content.decode()
    return response_str 
#function ends here
list1 = []
for i in Result:
    url2= i['href'] 
    mainurl = url1.format(url2)
    news_page_str = html_page_str(mainurl) 
    bs1 = BeautifulSoup(news_page_str)
    tag = bs1.find("a", class_ = 'ticket-symbol')
    if tag != None:
        list1.append(tag.text)
print(list1) 
list2 = []
list3 = []
final_df = pd.DataFrame()
for i in list1:
    list2.append(yf.Ticker(i))
    for j in list2:
        df = pd.DataFrame(j.history(period = '5d'))
        df['stocksymbol'] = i
    final_df = final_df.append(df)
print(final_df)
def plot(x):
    i = final_df[final_df['stocksymbol'] == x]   
    fig1 = plt.figure(figsize=(20,7))
    ax1=fig1.add_subplot(121)
    sns.lineplot(data = i, x = 'Date',  y = 'Close')
    plt.xticks(rotation=45)
    ax1=fig1.add_subplot(122)
    sns.lineplot(data = i, x = 'Date',  y = 'Volume')
    plt.xticks(i.index, rotation=45)
    st.pyplot(fig1)

x = st.sidebar.selectbox('Here are the matched symbols from Yahoo-PRNewswire. Select a symbol to view the visualization',list1)
if st.sidebar.button('Click here to view the visualization'):
    plot(x)










