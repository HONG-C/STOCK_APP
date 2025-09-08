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

        # 국내 종목 여부 확인
        try:
            stock_list = fdr.StockListing('KRX')
            is_domestic = ticker in stock_list['Code'].values
            if is_domestic:
                stock_name = stock_list[stock_list['Code'] == ticker]['Name'].values[0]
                currency = "원"
            else:
                stock_name = ticker
                currency = "달러"
        except:
            stock_name = ticker
            currency = "원"

        st.subheader(f"📊 [{stock_name}] 현재가 분석 ({currency} 기준)")

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
        rows.append(['현재가', f"{current_price:,.1f} {currency}", '✅'])

        for label, price in average_prices.items():
            if price > current_price:
                trend = "🔻 낮음"
            elif price < current_price:
                trend = "🔺 높음"
            else:
                trend = "➡️ 동일"
            rows.append([label, f"{price:,.1f} {currency}", trend])

        result_df = pd.DataFrame(rows, columns=["기간", f"가격 ({currency})", "분석"])
        st.dataframe(result_df, use_container_width=True)

    except Exception as e:
        st.error("❌ 종목 코드를 잘못 입력했거나 데이터를 불러올 수 없습니다.")
        st.exception(e)
