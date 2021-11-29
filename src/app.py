import pandas as pd
from package.scraping import get_daily_price_from_naver
from package.macd import add_macd, add_macd_signal, add_macd_oscillator, add_macd_slope, add_macd_trade_point
from package.rsi import add_rsi, add_rsi_trade_point, get_backtest_rsi
from package.scraping import get_daily_price
from package.inf_trade import get_backtest

## table로 변수 하나 만들자
## naver에서 주가 scraping
df_technical_analyis = get_daily_price_from_naver()

## macd 계산
add_macd(df_technical_analyis, short=12, long=26)
add_macd_signal(df_technical_analyis, span=9)
add_macd_oscillator(df_technical_analyis)
add_macd_slope(df_technical_analyis)
add_macd_trade_point(df_technical_analyis)

## rsi 계산
add_rsi(df_technical_analyis)
add_rsi_trade_point(df_technical_analyis)

# backtest 로직은 더 만들어야 함...
df_rsi_backtest = get_backtest_rsi(df_technical_analyis)
# print(df_rsi_backtest)

# 최종결과물 매수/매도 포인트 정보가 있는 엑셀, 매일 매일
# 우선 개별종목 분석 부터...
# print(df_technical_analyis.columns)

# ETF x3 Leverage Ticker
# FNGU
# TQQQ


df_etf = get_daily_price("FNGU")
get_backtest(df_etf)
print(df_etf)