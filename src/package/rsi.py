import pandas as pd
import numpy as np

def add_rsi(df_technical_analyis):
    diff = df_technical_analyis["price"].diff()
    u = np.where(diff > 0, abs(diff), 0)
    d = np.where(diff < 0, abs(diff), 0)
    au = pd.DataFrame(u).rolling(window=14).mean()
    ad = pd.DataFrame(d).rolling(window=14).mean()
    rsi = (au / (au + ad)) * 100

    # df_technical_analyis에 열을 추가하기 위해, 같은 index를 붙여야함.
    rsi["date"]= pd.Series(df_technical_analyis.index)
    rsi = rsi.set_index("date")

    df_technical_analyis['rsi'] = rsi
    return

def add_rsi_trade_point(df_technical_analyis):
    def get_rsi_trade_strategy(table):
        if table["rsi"] > 70:
            return "sell"
        elif table["rsi"] < 30:
            return "buy"
        else:
            return "hold"

    df_technical_analyis["rsi_trade_point"] = df_technical_analyis.apply(get_rsi_trade_strategy, axis=1)
    return

def get_backtest_rsi(df_technical_analyis):
    def get_rsi_trade_point(table):
        if table["rsi_trade_point"] == "buy":
            return -table["price"]
        elif table["rsi_trade_point"] == "sell":
            return table["price"]
        else:
            return 0

    df_rsi_backtest = pd.DataFrame(columns=["price"], data=df_technical_analyis["price"])
    trade_price = df_technical_analyis.apply(get_rsi_trade_point, axis=1)
    df_rsi_backtest["trade_price"] = trade_price
    df_rsi_backtest["total_trade_price"] = trade_price.cumsum()

    return df_rsi_backtest