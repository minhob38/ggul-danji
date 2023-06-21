import yfinance
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


## 환율이 오르는 경우 (원화가치 하락)
# - 달러가격 상승 또는 달러가치 상승
# 달러를 비싸게 사야하므로 매수 X

## 환율이 내리는 경우 (원화가치 상승)
# - 달러가격 하락 또는 달러가치 하락
# 달러지수가 그대로인 경우, 달러가치는 그대로이고 원화가치가 오른것이므로 매수 O
# 달러지수가 내린 경우, 달러가치가 떨어진것이므로 매수 X

# 원/달러 환율 dataframe을 조회
def get_won_dollar_exchange_rate(range):
    # 1년동안 data를 가져오기
    start_date = (datetime.now() - timedelta(days=range)).date()
    end_date = datetime.now().date()

    #원/달러 환율 dataframe 조회 (open,high,low,close)
    df = yfinance.download(['USDKRW=X'],start=start_date, end=end_date)

    # mean = df["Close"].mean()
    # df["Close"].plot()
    # plt.show()
    return df


# * 달러지수: 다른 국가의 통화와 비교한 달러의 가치
# - 대륙간거래소(ICE) 1973년 기준 100 / 6개국(일본,영국,캐나다,스웨덴,스위스,유로) https://finance.yahoo.com/quote/%5ENYICDX?p=^NYICDX&.tsrc=fin-srch, https://kr.investing.com/indices/usdollar
# - 연방준비제도 2006년 기준 100
# 원/달러 환율 dataframe을 조회
def get_dollar_index(range):
        # 1년동안 data를 가져오기
    start_date = (datetime.now() - timedelta(days=range)).date()
    end_date = datetime.now().date()

    # ICE 달러지수 dataframe 조회 (open,high,low,close)
    df = yfinance.download(['^NYICDX'],start=start_date, end=end_date)
    # df["Close"].plot()
    # plt.show()
    return df

# 달러가 달러지수에 수렴한다는 가정하에, 현재 달러가치와 환율을 비교한 값
# 달러갭이 큼 -> 현재 환율이 달러가치를 못 따라오고 있기에, 미래의 환률 변화량이 커 환차익이 적음
# 달러갭이 작음 -> 현재 환율이 달러가치를 쫓아 오기에, 미래의 환율 변화량이 작아 환차익이 적음
# 달러갭 = 달러지수 (비례)
# 달러갭 = 1 / 환율(원/달러) (반비례)
# 달러갭 = 달러지수 / (원/달러) x 100
def get_dollar_gap(df_won_dollar_exchange_rate, df_dollar_index):
    df = (df_dollar_index["Close"] / df_won_dollar_exchange_rate["Close"]) * 100
    return df

# 엔화 연평균
def get_won_yen_exchange_rate():
    start_date = '2023-03-06'
    end_date = '2023-03-08'
    data = yfinance.download(['JPYKRW=X'],start=start_date, end=end_date)
    print(data)
    mean = data["Close"].mean()
    print(mean)