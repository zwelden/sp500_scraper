import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

from wiki_sp500_stock_list import get_sp_500

def get_yahoo_stock_page(symbol):
    page = requests.get("https://finance.yahoo.com/quote/" + symbol)
    return page

def soupify_page(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_info_table(soup, side=0):
    """ side = 0 for left side <-- default
        side = 1 for right side
    """
    quote_summary = soup.find(id="quote-summary")
    table_div = list(quote_summary.children)[side]
    table = list(table_div.children)[0]
    table_body = list(table.children)[0]
    return table_body

def get_left_side_info_table(soup):
    """ uses get_info_table()
        use to get: previous close, open, bid, ask, day's range,
            52 week range, volume, avg. volume """
    table_info = get_info_table(soup, 0)
    return table_info

def get_right_side_info_table(soup):
    """ uses get_info_table()
        use to get: market cap, beta, PE ratio, eps, earnings date,
            dividend and yeild, ex-dividend date, 1y target est """
    table_info = get_info_table(soup, 1)
    return table_info

def get_open_price(info_table):
    table_open_row = list(info_table.children)[1]
    stock_open_value = list(table_open_row.children)[1].get_text()
    price = stock_open_value
    return price

def get_info(symbol_list, choice=0):
    """ takes a stock ticker or list of stock tickers and returns
        a list of stock ticker: opening value pairs
        choice list:  <<build choice list>> """
    # set choice value here

    if type(symbol_list) is not list:
        symbols = list(symbol_list)
    else:
        symbols = symbol_list

    info_list = []
    for symbol in symbols:
        page = get_yahoo_stock_page(symbol)
        soup = soupify_page(page)
        info_table = get_left_side_info_table(soup)
        price = get_open_price(info_table) ####
        info_list.append({symbol: price})
        time.sleep(.1)
    return info_list




companies = get_sp_500()
symbol_list = []
for i in range(5):
    # symbol = companies[i]["symbol"]
    # page = requests.get("https://finance.yahoo.com/quote/" + symbol)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # quote_summary = soup.find(id="quote-summary")
    # table_div = list(quote_summary.children)[0]
    # table = list(table_div.children)[0]
    # table_body = list(table.children)[0]
    # table_open_row = list(table_body.children)[1]
    # stock_open_value = list(table_open_row.children)[1].get_text()
    # prices[symbol] = stock_open_value

    # time.sleep(.1)
    symbol_list.append(companies[i]['symbol'])

open_price_list = get_info(symbol_list)
print(open_price_list)
