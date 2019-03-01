from zipline.api import order, record, symbol, get_datetime
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from datetime import timedelta
df = pd.read_excel(r'C:\Users\Jakub\Desktop\dissertation/base_d.xlsx')
df['date_'] = pd.to_datetime(df['date'])
#vars


shares = 5
def initialize(context):
    pass


def handle_data(context, data):
    today = pd.Timestamp(get_datetime().date())  # get_datetime().replace(minute=0, hour=0, second=0, microsecond=0)
    #unused_indices = df.index()
    transactions = pd.DataFrame(columns = ['idea','ticker','date'])
    if today in list(pd.to_datetime(df['date'])): #- timedelta(days=1)
        print('datez match')  # fine up till here
        to_trade = df[df['date_'] == today]
        if not to_trade.empty:
            print('we have something to trade')
        for i in to_trade.index:
            single_row = df.loc[[i]]
            if single_row.iloc[0]['idea'] == 'buy': # DO make sure this is just a single row

                order(single_row['ticker'], +shares)
                df2 = pd.DataFrame([single_row['idea'], single_row['ticker'], today], columns=['idea','ticker','date'])
                transactions.append(df2)
            if single_row['idea'] == 'sell':
                print('a sell')
                order(single_row['ticker'], -shares)
                df2 = pd.DataFrame([single_row['idea'], single_row['ticker'], today], columns=['idea','ticker','date'])
                transactions.append(df2)

    if today - timedelta(days=5) in list(transactions['date']):
        to_cancel = transactions[transactions['date'] == today]
        for index in to_cancel.index():
            single_row = to_cancel.loc[[index]]
            if single_row['idea'] == 'buy':
                to_tr = -shares
            else:
                to_tr = shares
            order(single_row['ticker'], to_tr)



def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio $ value')
    plt.legend(loc=0)
    plt.show()