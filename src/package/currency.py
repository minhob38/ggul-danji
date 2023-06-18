import yfinance

def get_won_yen_exchange_rate():
    start_date = '2023-03-01'
    end_date = '2023-03-10'
    data = yfinance.download(['USDKRW=X','JPYKRW=X'],start=start_date, end=end_date)
    print(data)