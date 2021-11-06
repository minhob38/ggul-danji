import pandas as pd

def get_ema(df_technical_analyis, **kwargs):
    return df_technical_analyis["price"].ewm(span=kwargs["span"]).mean()

def add_macd(df_technical_analyis, **kwargs):
    ema_short = get_ema(df_technical_analyis, span=kwargs["short"])
    ema_long = get_ema(df_technical_analyis, span=kwargs["long"])
    macd = ema_short - ema_long
    df_technical_analyis["macd"] = macd
    return

def add_macd_signal(df_technical_analyis, **kwargs):
    macd_signal = df_technical_analyis["macd"].ewm(span=kwargs["span"]).mean()
    df_technical_analyis["macd_signal"] = macd_signal
    return

def add_macd_oscillator(df_technical_analyis):
    df_technical_analyis["macd_oscillator"] = df_technical_analyis.apply(
        lambda row: row["macd"] - row["macd_signal"], axis=1
    )
    return

def add_macd_slope(df_technical_analyis):
    df_technical_analyis["macd_slope"] = df_technical_analyis["macd"].diff()
    return

def func(table):
    if (table["macd"] > table["price"] * 0.05 and table["macd"] < table["price"] * 0.05) and table["macd_slope"] > 0 and table["macd_oscillator"] > 0:
        return "buy"
    elif table["macd"] > 0 and table["macd_oscillator"] > 0:
        return "hold"
    elif table["macd"] < 0 and table["macd_oscillator"] < 0:
        return "sell"
    else:
        return "hold"

def add_macd_trade_point(df_technical_analyis):
    df_technical_analyis["macd_trade_point"] = df_technical_analyis.apply(func, axis=1)
    return
