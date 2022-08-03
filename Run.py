from datetime import datetime, timedelta
from paramiko import *
import pandas as pd
import time
import myconstants


def update_files():
    query_string = 'https://query1.finance.yahoo.com/v7/finance/download/%5EVIX?' \
                   f'period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
    data_frame = pd.read_csv(query_string, usecols=['Date', 'Close'])

    data_frame['Date'] = pd.to_datetime(data_frame['Date'])
    data_frame['Date'] = (data_frame['Date'].dt.strftime('%d-%b-%Y'))

    data_frame['Close'] = data_frame['Close'].astype(float) + 0.0001
    data_frame['Close'] = data_frame['Close'].round(decimals=2)
    print("-" * 57)
    print(data_frame)

    path = "\\\\SERVER\\jdjl\\interest-nz\\interest.co.nz\\chart_data\\confidence\\vix-vix.csv"
    data_frame.to_csv(path, mode='a', index=False, header=False)
    print("-" * 10 + " Vix has been successfully appended! " + "-" * 10)


def ftp_files():
    host = 'nfs.interest.co.nz'
    print(f"Connecting to {host}...")
    transport = Transport(host)
    transport.connect(None, myconstants.USERNAME, myconstants.PASSWORD)
    sftp = SFTPClient.from_transport(transport)
    print(f"Connection to {host} server successful")

    localpath = r'\\SERVER\jdjl\interest-nz\interest.co.nz\chart_data\confidence\\vix-vix.csv'
    remotepath = "/var/www/drupal8.interest.co.nz/web/sites/default/files/charts-csv/chart_data/confidence/vix-vix.csv"
    sftp.put(localpath, remotepath)

    print("")
    print("File successfully uploaded")


if __name__ == '__main__':
    if (datetime.now().strftime('%A')) == "Sunday" or (datetime.now().strftime('%A')) == "Monday":
        exit()
    else:
        period1 = int(time.mktime((datetime.now()).timetuple()))
        period2 = int(time.mktime((datetime.now()).timetuple()))
        update_files()
        ftp_files()