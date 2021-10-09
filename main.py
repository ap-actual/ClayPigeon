import pandas as pd
import yfinance as yf
from utils import normalize_tick

if __name__ == '__main__':

    msft = yf.Ticker("MSFT")

    # get historical market data
    hist = msft.history(period="10y")

    years_back = 10
    np_len = years_back*52*5

    df_norm = normalize_tick(hist, np_len)

    print(df_norm)
