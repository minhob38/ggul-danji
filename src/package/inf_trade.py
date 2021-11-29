import math
import pandas as pd

def create_inf_table(df, **kwargs):
    return_rate = kwargs["close_price"] / kwargs["blended_price"] - 1
    profit = return_rate * kwargs["buy_amount"] 

    row = {
        "Nth": kwargs["n"],
        "DATE": kwargs["date"],
        "ETF-PRICE[$]": kwargs["close_price"],
        "BLENDED-PRICE[$]": kwargs["blended_price"],
        "RETURN-RATE[%]": return_rate * 100,
        "PROFIT[$]": profit,
        "BUY AMOUNT[$]": kwargs["buy_amount"],
        "BLENDED BUY PRICE[$]": kwargs["blended_price"] if kwargs["is_blended_buy"] else 0,
        "BLENDED BUY COIN[-]": kwargs["blended_try_coin"] if kwargs["is_blended_buy"] else 0,
        "BIG BUY PRICE[$]": kwargs["close_price"] if kwargs["is_big_buy"] else 0,
        "BIG BUY COIN[-]": kwargs["big_try_coin"] if kwargs["is_big_buy"] else 0,
        "IS BLENDED BUY": kwargs["is_blended_buy"],
        "IS BIG BUY": kwargs["is_big_buy"]
    }

    return df.append(row, ignore_index=True)


def get_backtest(df):
    seed = 10000 # seed money
    division = 40 # 40회 분할
    goal = 10 # 10% 수익률
    cycle = 1 # 매수 싸이클
    begin = '2018-01-26'
    dates = df.index.strftime('%Y-%m-%d').tolist()
    begin_idx = dates.index(begin)
    end_idx = len(df) - 1

    buy_amount = 0
    # 2회 이상 살 수 있는 시도액이여아 함
    # (seed / division)

    blended_price = 0
    total_coin = 0

    # 절반은 큰수 매수, 절반은 평단 매수
    big_try_money = (seed / division) * 0.5
    blended_try_money = (seed / division) * 0.5
    print(big_try_money, blended_try_money)

    # 미국주식무한매수법 dataframe
    df_inf_trade = pd.DataFrame()

    n = 0
    for i in range(begin_idx, end_idx + 1):
        date = df.index[i]
        n = n + 1
        is_blended_buy = False
        is_big_buy = False

        close_price = df.iloc[i]["Close"]

        if (math.floor(big_try_money / close_price) < 1):
            raise Exception('small money : (')

        # 첫 매수는 종가 매수
        if n == 1:
            big_try_coin = 2 * math.floor(big_try_money / close_price)
            total_coin = big_try_coin
            buy_amount = big_try_coin * close_price
            blended_price = close_price
            is_big_buy = True

            df_inf_trade = create_inf_table(
                df_inf_trade,
                n=n,
                date=date,
                close_price=close_price,
                blended_price=blended_price,
                buy_amount=buy_amount,
                blended_try_coin=0,
                big_try_coin=big_try_coin,
                is_blended_buy=is_blended_buy,
                is_big_buy=is_big_buy
            )

            continue

        # 10% 수익률이면 거래 종료
        if (close_price > 1.1 * blended_price):
            df_inf_trade = create_inf_table(
                df_inf_trade,
                n=n,
                date=date,
                close_price=close_price,
                blended_price=blended_price,
                buy_amount=buy_amount,
                blended_try_coin=blended_try_coin,
                big_try_coin=big_try_coin,
                is_blended_buy=is_blended_buy,
                is_big_buy=is_big_buy
            )
            print("break : )")
            break

        # 두번쨰 매수부터 반은 큰수 매수, 반은 평단 메수
        big_try_coin = math.floor(big_try_money / close_price)
        blended_try_coin = math.floor(blended_try_money / blended_price)

        # 평단매수 실행 (평단가 지정가 매수)
        if (close_price <= blended_price):
            blended_price = (blended_price * total_coin
                + blended_price * blended_try_coin) / (total_coin + blended_try_coin)

            total_coin = total_coin + blended_try_coin 
            buy_amount = buy_amount + blended_try_coin * blended_price
            is_blended_buy = True

        # loc지정가가 종가이상이면, 큰수매수 실행 (종가 매수)
        big_try_price = 1.1 * blended_price
        if big_try_price >= close_price:
            blended_price = (blended_price * total_coin
                + close_price * big_try_coin) / (total_coin + big_try_coin)

            total_coin = total_coin + big_try_coin
            buy_amount = buy_amount + big_try_coin * close_price
            is_big_buy = True

        df_inf_trade = create_inf_table(
            df_inf_trade,
            n=n,
            date=date,
            close_price=close_price,
            blended_price=blended_price,
            buy_amount=buy_amount,
            blended_try_coin=blended_try_coin,
            big_try_coin=big_try_coin,
            is_blended_buy=is_blended_buy,
            is_big_buy=is_big_buy
        )

    print(df_inf_trade)

    # blended price buy
    # big_buy
