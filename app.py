# app.py
import streamlit as st
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📈 주식 평균가 분석기")
st.title("📈 주식 평균가 분석기")

# ✅ 종목 입력
ticker = st.text_input("종목 코드 또는 티커를 입력하세요 (예: 133690, AAPL):", "133690")

if ticker:
    try:
        # ✅ 국내 종목 코드 리스트 불러오기
        krx_list = fdr.StockListing('KRX')
        is_domestic = ticker.isdigit() and ticker in krx_list['Code'].values

        # ✅ 종목 이름 및 단위 설정
        if is_domestic:
            stock_name = krx_list[krx_list['Code'] == ticker]['Name'].values[0]
            currency = "원"
        else:
            stock_name = ticker.upper()
            currency = "달러"

        # ✅ 데이터 수집
        today = datetime.today()
        start_date = today - timedelta(days=365 * 10)
        df = fdr.DataReader(ticker, start_date.strftime('%Y-%m-%d'))
        df.index = pd.to_datetime(df.index)
        current_price = df['Close'][-1]

        # ✅ 평균가 계산 함수
        def average_price(days):
            if days == 'all':
                return df['Close'].mean()
            cutoff = today - timedelta(days=days)
            return df[df.index >= cutoff]['Close'].mean()

        # ✅ 평균가 계산
        average_prices = {
            '1일간 평균': average_price(1),
            '1주일간 평균': average_price(7),
            '1달간 평균': average_price(30),
            '3달간 평균': average_price(90),
            '6달간 평균': average_price(180),
            '1년간 평균': average_price(365),
            '10년간 평균': average_price('all')
        }

        # ✅ 표 정리 및 색상 이모지 표시
        rows = []
        rows.append(['현재가', f"{current_price:,.1f} {currency}"])

        for label, price in average_prices.items():
            color = "🔺" if price > current_price else "🔻" if price < current_price else "➡️"
            rows.append([label, f"{price:,.1f} {currency} {color}"])

        result_df = pd.DataFrame(rows, columns=["기간", "가격"])

        # ✅ 종목명 & 단위 출력
        st.markdown(f"### 📌 종목명: **{stock_name}**")
        st.markdown(f"### 💰 통화 단위: **{currency}**")

        st.dataframe(result_df, use_container_width=True)

    except Exception as e:
        st.error("❌ 종목 코드를 잘못 입력했거나 데이터를 불러올 수 없습니다.")
        st.exception(e)
