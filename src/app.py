import pandas as pd
from package.scraping import get_daily_price_from_naver
from package.macd import add_macd, add_macd_signal, add_macd_oscillator, add_macd_slope, add_macd_trade_point
from package.rsi import add_rsi, add_rsi_trade_point

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

print(df_technical_analyis)

    # print(df)
    # data frame에 넣어서, 이평선 계산하기
    # macd function
    # macd signal function
    # macd oscillator function

    # 볼린저 밴드


# 모든 종목 가격 크롤링 (csv에서 종목코드 가져오기)
# mongo db 연결

# 최종결과물 매수/매도 포인트 정보가 있는 엑셀, 매일 매일
# 우선 개별종목 분석 부터...
# print(df_technical_analyis.columns)
