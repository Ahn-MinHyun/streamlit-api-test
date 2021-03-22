import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
# 야후금융에서 주식정보를 제공하는 라이브러리 yfiance이용
# 주식정보를 불러오고 차트그리기(pip install yfinance)

# 해당 주식에 대한 트윗글을 불러올 수 있는 api가 있다. 
# stocktwits.com에서 제공하는 Restful API를 호출해서 데이터를 가져오는 실습
import requests
from fbprophet import Prophet 
def main():
    st.header("Online Stock Price Ticker")


    # symbol = st.text_input('심볼 입력 : ')
    symbol ='AMZN' 

    data = yf.Ticker(symbol)

    today = datetime.now().date().isoformat() #문자열로
    print(today)

#------------------------------------------------------
    df = data.history(start = '2010-06-01', end = today)

    st.dataframe(df)
# --------------------Close차트 -----------------
    st.subheader('종가')
    st.line_chart(df['Close'])

#------------------------------------------------
    st.subheader('거래량')
    st.line_chart(df['Volume'])

# yfinace의 라이브러리만의 정보 
    # data.info
    # data.calendar
    # data.major_holders
    # data.institutional_holders
    # data.recommendations
    div_df =data.dividends #배당금정보
    st.dataframe(div_df.resample('Y').sum())

    new_df = div_df.reset_index()
    new_df['Year'] = new_df['Date'].dt.year

    st.dataframe(new_df)

    fig  = plt.figure()
    plt.bar(new_df['Year'],new_df['Dividends'])
    st.pyplot(fig)

    # 여러주식 한번에 보여주기

    favorites = ['msft','aapl','amzn','tsla','nvda']

    f_df = pd.DataFrame()  
    for stock in favorites:
        f_df[stock] = yf.Ticker(stock).history(start='2010-01-01', end =today)['Close']

    st.dataframe(f_df)
# 차트그리기
    st.line_chart(f_df)
#=============================stocktwits===================================
# 스탁 트윗 API 호출
    res = requests.get('https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(symbol))
# json 형식이므로 .json()이용
    res_data = res.json()
# 파이썬의 딕셔너리와 리스트로 활용
    # st.write(res_data)

    for massage in res_data['messages']:

        col1, col2=st.beta_columns([1,4]) #영역 잡기(비율)

        with col1 : 
            st.image(massage['user']['avatar_url']) #아바타 사진
        with col2 :
            st.write('유저이름 : ' + massage['user']['username'])
            st.write('트윗 내용 : ' + massage['body'])
            st.write('올린 시간 : ' +massage['created_at'])
    p_df =df.reset_index()

    p_df.rename(columns = {'Date':'ds','Close':'y'}, inplace = True)

    st.dataframe(p_df)
    #예측 가능
    m = Prophet()
    m.fit(p_df)

    future = m.make_future_dataframe(periods =365)
    forecast = m.predict(future)

    st.dataframe(forecast)

    fig1 = m.plot(forecast)
    st.pyplot(fig1)

    fig2 = m.plot_components(forecast)
    st.pyplot(fig2)
    
    pass

if __name__ == '__main__':
    main()