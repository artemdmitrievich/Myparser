import krakenex
import pandas as pd
from math import sqrt


def calc_volatility_coeff(coin1, coin2, duration):
    if duration == 1:
        interval = 5
        duration = 288
    elif duration > 1 and duration <= 7:
        interval = 15
        duration = duration * 96
    elif duration > 7 and duration <= 29:
        interval = 60
        duration = duration * 24
    else:
        interval = 1440

    try:
        response = krakenex.API().query_public(
            "OHLC", {"pair": f"{coin1.upper()}{coin2.upper()}", "interval": interval}
        )
    except:
        return "error"

    if response["error"]:
        return "error"
    else:
        data = response["result"][list(response["result"].keys())[0]]

        prices = pd.DataFrame(data).iloc[:, 4].iloc[duration * (-1) :].astype(float)
        ema = prices.ewm(span=20, adjust=False).mean()

        coeff = 1 / (sqrt(((prices - ema) ** 2).mean()) / prices.mean() * 100)

        return coeff


if __name__ == "__main__":
    print(calc_volatility_coeff("usdt", "usd", 1))
