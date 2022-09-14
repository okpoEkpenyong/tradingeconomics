import tradingeconomics as te
import pandas as pd
from datetime import datetime, timedelta

from getEarningsPerShareTTM import getEarningsPerShareTTM

te.login('guest:guest')

## Without a client key only a small sample of data will be given.

## With no output_type defined, the result will be of the dictionary type.
## Use output_type='df' to display in pandas dataframe. 

# To get intraday P/E Ratio. Empty date returns the last P/E Ratio.
def getPERatio(symbols=None, date=None, output_type=None):
    if date == None:
        date = str((datetime.now()).date())

    endDate = datetime.strptime(str(date), '%Y-%m-%d')
    endDate = str((endDate + timedelta(days=1)).date())

    data = pd.DataFrame(te.getMarketsIntraday(symbols=symbols, initDate=date, endDate=endDate, output_type='raw'))

    stockPriceLastRow = data.iloc[-1]
    eps = getEarningsPerShareTTM(symbols=symbols, date=date, output_type='df')

    peRatio = round(stockPriceLastRow['Close']/eps, 2)

    return peRatio

mydata = getPERatio(symbols='aapl:us', date='2022-09-12', output_type='df')
print(mydata)
