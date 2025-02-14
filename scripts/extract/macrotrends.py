from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "utilities"))
import util

SOURCE_NAME = 'macrotrends'

def extract_debt_to_equity():
   
    # url
    urlpage = 'https://www.macrotrends.net/stocks/charts/SIVBQ/svb-financial-group/debt-equity-ratio'
    
    req = Request(url=urlpage, headers={'User-Agent':'Mozilla/5.0'})

    # query the web page and return the html
    page = urlopen(req)

    # parse the html and store in variable
    parsed_page = BeautifulSoup(page, 'html.parser')

    # print(parsed_page)

    # find results within the table
    table = parsed_page.find('table', attrs={'class': 'table'})
    results = table.find_all('tr')

    # print('Number of results', len(results))

    # create and write headers to a list
    rows = []
    rows.append(['Date', 'Long Term Debt',
                'Shareholder Equity', 'Debt to Equity Ratio'])
    # print(rows)

    # loop over the results
    for result in results:
        # find all columns per result
        data = result.find_all('td')
        # check that the columns have data
        if len(data) == 0:
            continue
        # write columns to variables
        date = data[0].getText()
        long_term_debt = data[1].getText()
        shareholder_equity = data[2].getText()
        debt_to_equity_ratio = data[3].getText()

        # append the data from the column variables to build the output
        rows.append([date, long_term_debt, shareholder_equity, debt_to_equity_ratio])

    # print rows to display the data from the list
    # print(rows)

    # Make rows a dataframe
    df = pd.DataFrame(rows)
    
    # Make first row column names then drop first row
    df.columns = df.iloc[0]
    df = df[df.index>0]
    
    df.insert(loc=0, column='Ticker', value='SIVBQ')

    return df

def load_raw_debt_to_equity():
    mt_df = extract_debt_to_equity()
    dest_table_name = 'debt_to_equity'
    csv_file_name = SOURCE_NAME + '_' + dest_table_name + '.csv'
    util.load_raw_data(mt_df, csv_file_name)

def extract(table_name='all'):
    if table_name == 'all':
        load_raw_debt_to_equity()
    elif table_name == 'debt_to_equity':
        load_raw_debt_to_equity()
    else:
        print('Invalid table name')