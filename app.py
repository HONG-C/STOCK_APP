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
            '1일 평균': average_price(1),
            '1주 평균': average_price(7),
            '1달 평균': average_price(30),
            '3달 평균': average_price(90),
            '6달 평균': average_price(180),
            '1년 평균': average_price(365),
            '10년 평균': average_price('all')
        }

        rows = []
        rows.append(['현재가', f"{current_price:,.1f}"])

        for label, price in average_prices.items():
            color = "🔺" if price < current_price else "🔻" if price > current_price else "➡️"
            rows.append([label, f"{price:,.1f} {color}"])

        result_df = pd.DataFrame(rows, columns=["기간", "가격"])
        st.dataframe(result_df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 문제가 발생했습니다: {e}")
