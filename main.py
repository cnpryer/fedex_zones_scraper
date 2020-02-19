import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

import os

# current directory
CD = os.path.dirname(os.path.abspath(__file__))

# shipments data filepath.
FILENAME = ''
FILEPATH = os.path.join(CD, 'tmp', FILENAME)

# other shipments data configuration.
ORIGIN_COL = ''
DEST_COL = ''

# zone type either 'Express' or 'Ground'.
ZONE_TYPE = ''

def init():
    """return pd.Dataframe and initial zones list"""
    ext = FILENAME.split('.')[-1]
    print('input:', FILEPATH)
    if ext == 'xlsx' or ext == 'xls':
        return pd.read_excel(FILEPATH, sheet_name='Sheet1'), []
    elif ext == 'csv':
        return pd.read_csv(FILEPATH), []
    else:
        print('File must be .csv, .xlsx, .xls.')
        return pd.DataFrame(), []

def get_response_soup(origin:str, dest:str):
    """return soup of html to parse. Session init could be abstracted."""
    session = requests.session()
    url = 'http://www.fedex.com/ratetools/RateToolsMain.do;OTHERRATETOOLSSESSIONID=eZFaiytexLZ4nU67JFGPNSxgutLH1nF0aEv64w9UPYlOVqlujg85!-1418544371'
    data = {
        'method': 'FindZones',
        'origPostalCd': origin,
        'destCountryCd': 'us',
        'destPostalCd': dest
    }

    response = session.post(url, data=data)
    return BeautifulSoup(response.content, 'html.parser')

def parse_response_soup(soup:BeautifulSoup):
    """return zone from soup."""
    zone = np.nan
    count = 0
    td = soup.select('td')
    for name, value in zip(td, td[1:]):
            if '%s Zone:' % ZONE_TYPE in name.text and value.text and count != 1:
                try:
                    zone = int(value.text.strip())
                except:
                    pass
                break
            count += 1
    return zone

def main():
    df, zones = init()

    for i in range(len(df)):
        origin = str(df[ORIGIN_COL].iloc[i]).zfill(5)
        dest = str(df[DEST_COL].iloc[i]).zfill(5)
        print('running unique index:', i, '%:', i/(len(df)-1), 'origin:', origin, 'dest:', dest)

        soup = get_response_soup(origin, dest)
        zones.append(parse_response_soup(soup))
    
    df['zone'] = zones
    path = os.path.join(os.path.dirname(FILEPATH), 'output.csv')
    print('output:', path)
    df.to_csv(path, index=False)

if __name__ == '__main__':
    main()