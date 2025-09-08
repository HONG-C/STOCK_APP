# app.py
import streamlit as st
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import pandas as pd

# ✅ 페이지 설정
st.set_page_config(page_title="📈 주식 평균가 분석기")
st.title("📈 주식 평균가 분석기")

# ✅ 사용자 입력
ticker = st.text_input("종목 코드 또는 티커를 입력하세요 (예: 133690, AAPL):", "133690")

# ✅ 오늘 날짜 & 시작일자
today = datetime.today()
start_date = today - timedelta(days=365 * 10)

# ✅ 국내 종목 코드 리스트 미리 불러오기
try:
    krx = fdr.StockListing('KRX')
except:
    krx = pd.DataFrame(columns=['Code', 'Name'])

# ✅ 함수: 평균가 계산
def average_price(df, days):
    if days == 'all':
        return df['Close'].mean()
    cutoff = today - timedelta(days=days)
    return df[df.index >= cutoff]['Close'].mean()

# ✅ 분석 시작
if ticker:
    try:
        df = fdr.DataReader(ticker, start_date.strftime('%Y-%m-%d'))
        df.index = pd.to_datetime(df.index)
        current_price = df['Close'][-1]

        # ✅ 국내 종목 확인
        ticker_str = str(ticker).zfill(6)
        if ticker_str in krx['Code'].values:
            stock_name = krx[krx['Code'] == ticker_str]['Name'].values[0]
            currency = "원"
        else:
            stock_name = fdr.DataReader(ticker, start_date.strftime('%Y-%m-%d')).columns.name or "Unknown"
            currency = "달러"

        # ✅ 평균가들 계산
        average_prices = {
            '1일 평균': average_price(df, 1),
            '1주 평균': average_price(df, 7),
            '1달 평균': average_price(df, 30),
            '3달 평균': average_price(df, 90),
            '6달 평균': average_price(df, 180),
            '1년 평균': average_price(df, 365),
            '10년 평균': average_price(df, 'all')
        }

        # ✅ 결과 정리
        rows = []
        rows.append(['현재가', f"{current_price:,.1f} {currency}"])

        for label, price in average_prices.items():
            color = "🔺" if price < current_price else "🔻" if price > current_price else "➡️"
            rows.append([label, f"{price:,.1f} {currency} {color}"])

        result_df = pd.DataFrame(rows, columns=["기간", "가격"])

        # ✅ 종목명 표시
        st.markdown(f"### 📌 {ticker} - {stock_name}")
        st.dataframe(result_df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 문제가 발생했습니다: {e}")
