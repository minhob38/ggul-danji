import yfinance
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


### 달러를 기반으로 코드 및 주석이 쓰여있음 (엔화는 달러와 비슷한 원리로 설계되어 있음)

## 환율이 오르는 경우 (원화가치 하락)
# - 달러가격 상승 또는 달러가치 상승
# 달러를 비싸게 사야하므로 매수 X

## 환율이 내리는 경우 (원화가치 상승)
# - 달러가격 하락 또는 달러가치 하락
# 달러지수가 그대로인 경우, 달러가치는 그대로이고 원화가치가 오른것이므로 매수 O
# 달러지수가 내린 경우, 달러가치가 떨어진것이므로 매수 X

# 원/달러 환율 dataframe을 조회
def get_exchange_rate(**kwargs):
    range = kwargs["range"]
    nation = kwargs["nation"]

    start_date = (datetime.now() - timedelta(days=range)).date()
    end_date = datetime.now().date() # 조회 시, end_date 전날까지 가져옴 (오늘은 끝나지 않았으므로)

    if nation == "USA":
        #원/달러 환율 dataframe 조회 (open,high,low,close)
        df = yfinance.download(['USDKRW=X'],start=start_date, end=end_date)
        return df

    if nation == "JAPAN":
        #원/엔 환율 dataframe 조회 (open,high,low,close)
        df = yfinance.download(['JPYKRW=X'],start=start_date, end=end_date)
        return df

###
# * 달러지수: 다른 국가의 통화와 비교한 달러의 가치
# - 대륙간거래소(ICE) 1973년 기준 100 / 6개국(일본,영국,캐나다,스웨덴,스위스,유로) https://finance.yahoo.com/quote/%5ENYICDX?p=^NYICDX&.tsrc=fin-srch, https://kr.investing.com/indices/usdollar
# - 연방준비제도 2006년 기준 100
# ICE 달러지수 dataframe을 조회
# (단, 엔화지수는 없으므로 엔/달러 환율로 지수를 계산)
def get_currency_index(**kwargs):
    range = kwargs["range"]
    nation = kwargs["nation"]

    start_date = (datetime.now() - timedelta(days=range)).date()
    end_date = datetime.now().date() # 조회 시, end_date 전날까지 가져옴 (오늘은 끝나지 않았으므로)

    if nation == "USA":
        # ICE 달러지수 dataframe 조회 (open,high,low,close)
        df = yfinance.download(['^NYICDX'],start=start_date, end=end_date)
        return df

    if nation == "JAPAN":
        # 엔/달러 dataframe 조회 (open,high,low,close)
        df = yfinance.download(['JPYUSD=X'],start=start_date, end=end_date)
        return df

###
# 달러가 달러지수에 수렴한다는 가정하에, 현재 달러가치와 환율을 비교한 값
# 달러갭이 큼 -> 현재 환율이 달러가치를 못 따라오고 있기에, 미래의 환률 변화량이 커 환차익이 큼
# 달러갭이 작음 -> 현재 환율이 달러가치를 쫓아 오기에, 미래의 환율 변화량이 작아 환차익이 적음
# 달러갭 = 달러지수 (비례)
# 달러갭 = 1 / 환율(원/달러) (반비례)
# 달러갭 = 달러지수 / (원/달러) x 100
def get_gap(df_exchange_rate, df_index):
    print(type(df_exchange_rate["Close"]))
    df = (df_index["Close"] / df_exchange_rate["Close"]) * 100
    return df.dropna()

###
# dollar 매수 시점을 찾기 위한 기준 환율 계산
# <달러가치는 절대적 가치이며, 다른 국가들은 화폐가치를 일정하게 유지하기 위한 정책을 펼치기에 아래 전제들이 성립함>
# - 현재 환율이 평균 환율보다 낮을때 (with 평균 환율로 회귀한다는 전제)
# - 현재 달러지수가 평균 달러지수보다 낮을때 (with 평균 달러지수로 회귀한다는 전제)
# - 현재 달러갭이 평균 달러갭보다 높을때 (with 현재환율이 평균보다 달러가치를 못 쫓아오고 있다는 전제)
def calculate_reference_exchange_rate(**kwargs):
    # data 조회 기간 (1년)
    range = kwargs["range"]
    nation = kwargs["nation"]

    # 환율
    df_exchange_rate = get_exchange_rate(range=range, nation=nation)

    # 달러지수
    df_index = get_currency_index(range=range, nation=nation)

    # 달러갭
    df_gap = get_gap(df_exchange_rate, df_index)

    ### 평가환율
    # 현재 달러가치(달러지수)를 보았을때, 평균적인 달러지수와 환율의 차이(달러갭)로부터 환율이 어디쯤 있어야 하는지 계산할수 있음 (달러가치를 기반으로 투자)
    # 평가환율 = (달러지수 / 평균 달러갭) x 100

    # 현재(어제)환율 & 현재달러지수(어제) & 현재달러갭(어제) / 평균환율 & 평균달러지수 & 평균달러갭
    current_date = (datetime.now() - timedelta(days=1)).date().strftime("%Y-%m-%d")
    # 휴장일이 포함되어, current_date 쓰면 안됨
    # current_exchange_rate = df_exchange_rate.loc[current_date]["Close"]
    # current_index = df_index.loc[current_date]["Close"]
    # current_gap = df_gap.loc[current_date]
    current_exchange_rate = df_exchange_rate.iloc[-1]["Close"]
    current_index = df_index.iloc[-1]["Close"]
    current_gap = df_gap.iloc[-1]

    average_exchange_rate = df_exchange_rate["Close"].mean()
    average_index = df_index["Close"].mean()
    average_gap = df_gap.mean()

    # 평가환율
    reference_exchange_rate = (current_index / average_gap) * 100

    currency = ""

    if nation == "USA": currency = "달러"
    if nation == "JAPAN": currency = "엔화"

    print("===== 평균 =====")
    print(f"{currency} 환율 평균(1년)은 {average_exchange_rate}")
    print(f"{currency} 지수 평균(1년)은 {average_index}")
    print(f"{currency} 갭 평균은 {average_gap}")

    print(f"===== 현재(어제) {current_date} =====")
    print(f"현재(어제) {currency} 환율은 {current_exchange_rate}")
    print(f"현재(어제) {currency} 지수는 {current_index}")
    print(f"현재(어제) {currency} 갭은 {current_gap}")

    print("===== 평가환율 =====")
    print(f"{currency} 평가환율은 {reference_exchange_rate}")

    # TODO: 분할 매수/매도 단위 넣기

    # plot
    plt.rc('font', family='AppleGothic')
    plt.title(currency)
    plt.plot(df_exchange_rate["Close"], color="black", label="환율")
    plt.axhline(y=average_exchange_rate, color="r", linestyle=":", label="평균환율")
    plt.axhline(y=reference_exchange_rate, color="blue", linestyle="--", label="평가환율")
    plt.legend(loc=2)
    plt.show()

    if (reference_exchange_rate > current_exchange_rate):
        print(f"{currency} 매수 O")
    else:
        print(f"{currency} 매수 X")

    return reference_exchange_rate
