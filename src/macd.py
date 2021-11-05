# import finterstellar as fs
# import matplotlib.pyplot as plt
# symbol = "MSFT"
# df = fs.get_price(symbol, start_date="2020-01-01", end_date="2020-12-31")
# print(type(df))
# fs.macd(df)
# fs.indicator_to_signal(df, factor="macd_oscillator", buy=0, sell=0)
# fs.position(df)
# fs.draw_chart(df, left="position_chart", right="macd_oscillator")
# print(df)
# # plt.plot([1, 2, 3, 4])
# plt.show()

# macd function
# macd signal function
# macd oscillator function

import requests
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0'}

# 1page에 5일치 종가있음 -> 30일치 가져오기 (6 page)
MAX_PAGE = 6
MAX_DAY = 5

for page in range(1, MAX_PAGE + 1):
    print("page", page)
    url = f"https://finance.naver.com/item/sise_day.naver?code=000270&page={page}"
    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

    for num in range(1, MAX_DAY + 1):
        price_a = soup.select_one(f"body > table.type2 > tr:nth-child({num + 2}) > td:nth-child(2) span").text
        date_a = soup.select_one(f"body > table.type2 > tr:nth-child({num + 2}) > td:nth-child(1) span").text

        price_b = soup.select_one(f"body > table.type2 > tr:nth-child({num + 10}) > td:nth-child(2) span").text
        date_b = soup.select_one(f"body > table.type2 > tr:nth-child({num + 10}) > td:nth-child(1) span").text
        print(date_a, price_a, date_b, price_b)
