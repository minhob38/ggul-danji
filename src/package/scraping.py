import pandas as pd
import requests
from bs4 import BeautifulSoup
import FinanceDataReader as fdr

def get_daily_price_from_naver():
    # 1page에 5일치 종가있음 -> 30일치 가져오기 (6 page)
    MAX_PAGE = 6
    MAX_DAY = 5

    df = pd.DataFrame()

    for page in range(1, MAX_PAGE + 1):
        # print("page", page)
        headers = {'User-Agent' : 'Mozilla/5.0'}
        url = f"https://finance.naver.com/item/sise_day.naver?code=005930&page={page}"
        response = requests.get(url, headers=headers)
        if (response.status_code == 200):
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

        for num in range(1, MAX_DAY + 1):
            # if tag 없을때 에러처리 필요해 보임
            price_a = soup.select_one(f"body > table.type2 > tr:nth-child({num + 2}) > td:nth-child(2) span").text
            date_a = soup.select_one(f"body > table.type2 > tr:nth-child({num + 2}) > td:nth-child(1) span").text

            price_b = soup.select_one(f"body > table.type2 > tr:nth-child({num + 10}) > td:nth-child(2) span").text
            date_b = soup.select_one(f"body > table.type2 > tr:nth-child({num + 10}) > td:nth-child(1) span").text

            price_a = price_a.replace(",", "")
            price_b = price_a.replace(",", "")

            row_a = { "date": date_a, "price": price_a }
            row_b = { "date": date_b, "price": price_b }
            df = df.append(row_a, ignore_index=True)
            df = df.append(row_b, ignore_index=True)

    df["price"] = df["price"].apply(pd.to_numeric)
    df = df.sort_values("date")
    return df.set_index("date")

def get_daily_price(ticker):
    df = fdr.DataReader(ticker)
    return df

