# app.py
import streamlit as st
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📈 주식 평균가 분석기")
st.title("📈 주식 평균가 분석기")

# 👉 사용자 입력
ticker = st.text_input("종목 코드 또는 티커를 입력하세요 (예: 133690, AAPL):", "133690")

if ticker:
    try:
        today = datetime.today()
        start_date = today - timedelta(days=365 * 10)

        # 👉 데이터 불러오기
        df = fdr.DataReader(ticker, start_date.strftime('%Y-%m-%d'))
        df.index = pd.to_datetime(df.index)
        current_price = df['Close'][-1]

        # 👉 국내/해외 구분
        if ticker.isdigit():
            # 국내 주식
            krx = fdr.StockListing('KRX')
            if ticker in krx['Code'].values:
                stock_name = krx[krx['Code'] == ticker]['Name'].values[0]
            else:
                stock_name = f"Unknown({ticker})"
            currency_unit = "원"
        else:
            # 해외 주식
            stock_name = ticker.upper()  # FinanceDataReader는 해외 종목명 지원 X
            currency_unit = "달러"

        # 👉 평균 가격 계산 함수
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

        # 👉 표 구성
        rows = []
        rows.append(['현재가', f"{current_price:,.1f} {currency_unit}"])

        for label, price in average_prices.items():
            trend_icon = "🔺" if price > current_price else "🔻" if price < current_price else "➡️"
            rows.append([label, f"{price:,.1f} {currency_unit} {trend_icon}"])

        result_df = pd.DataFrame(rows, columns=["기간", "가격"])

        # 👉 출력
        st.subheader(f"📌 {stock_name} ({ticker})")
        st.dataframe(result_df, use_container_width=True)

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
