# app.py
import streamlit as st
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📈 주식 평균가 분석기")
st.title("📈 주식 평균가 분석기")

ticker = st.text_input("종목 코드 또는 티커를 입력하세요 (예: 133690, AAPL):", "133690")

if ticker:
    try:
        today = datetime.today()
        start_date = today - timedelta(days=365 * 10)
        df = fdr.DataReader(ticker, start_date.strftime('%Y-%m-%d'))
        df.index = pd.to_datetime(df.index)
        current_price = df['Close'][-1]

        def average_price(days):
            if days == 'all':
                return df['Close'].mean()
            cutoff = today - timedelta(days=days)
            return df[df.index >= cutoff]['Close'].mean()

        average_prices = {
            '1일간 평균': average_price(1),
            '1주일간 평균': average_price(7),
            '1달간 평균': average_price(30),
            '3달간 평균': average_price(90),
            '6달간 평균': average_price(180),
            '1년간 평균': average_price(365),
            '10년간 평균': average_price('all')
        }

        rows = []
        rows.append(['현재가', f"{current_price:,.1f}원"])

        for label, price in average_prices.items():
            color = "🔺" if price > current_price else "🔻" if price < current_price else "➡️"
            rows.append([label, f"{price:,.1f}원 {color}"])

        result_df = pd.DataFrame(rows, columns=["기간", "가격"])
        st.dataframe(result_df, use_container_width=True)

    except:
        st.error("종목 코드를 잘못 입력했거나 데이터를 불러올 수 없습니다.")
