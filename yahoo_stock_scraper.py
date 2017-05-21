import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


class YahooStockQuote:
    QUOTE_PAGE = "https://finance.yahoo.com/quote/"

    def __init__(self, symbol):
        self.symbol = symbol
        self.stock_info = self.get_info()

    def get_yahoo_stock_page(self):
        page = requests.get(self.QUOTE_PAGE + self.symbol)
        return page

    def soupify_page(self):
        page = self.get_yahoo_stock_page()
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def get_info_table(self, soup, side=0):
        """ side = 0 for left side <-- default
            side = 1 for right side
        """
        quote_summary = soup.find(id="quote-summary")
        table_div = list(quote_summary.children)[side]
        table = list(table_div.children)[0]
        table_body = list(table.children)[0]
        return table_body

    def get_left_side_info_table(self, soup):
        """ uses get_info_table()
            use to get: previous close, open, bid, ask, day's range,
                52 week range, volume, avg. volume """
        table_info = self.get_info_table(soup, 0)
        return table_info

    def get_right_side_info_table(self, soup):
        """ uses get_info_table()
            use to get: market cap, beta, PE ratio, eps, earnings date,
                dividend and yeild, ex-dividend date, 1y target est """
        table_info = self.get_info_table(soup, 1)
        return table_info

    def get_info(self):

        def get_value(table, row):
            table_row = list(table.children)[row]
            value = list(table_row.children)[1].get_text()
            return value

        soup = self.soupify_page()
        stock_info = {}

        # TODO get date/time
        # TODO get current price --> after close current price is close price

        '''get left side table info'''

        ''' replace with:
        table_left_side = self.get_left_side_info_table(soup)
        values = ['prev close', 'open price', bid value', ...]
        for i, value in enumerate(values):
            stock_info[value] = get_value(table_left_side, i)
        '''
        table_left_side = self.get_left_side_info_table(soup)
        prev_close_value = get_value(table_left_side, 0)
        stock_info['prev close'] = prev_close_value
        open_value = get_value(table_left_side, 1)
        stock_info['open value'] = open_value
        bid_value = get_value(table_left_side, 2)
        stock_info['bid value'] = bid_value
        ask_value = get_value(table_left_side, 3)
        stock_info['ask value'] = ask_value
        days_range = get_value(table_left_side, 4)
        stock_info["day's range"] = days_range
        fifty_two_week_range = get_value(table_left_side, 5)
        stock_info['52 week range'] = fifty_two_week_range
        volume = get_value(table_left_side, 6)
        stock_info['volume'] = volume
        avg_volume = get_value(table_left_side, 7)
        stock_info['avg. volume'] = avg_volume

        '''get right side table info'''
        table_right_side = self.get_right_side_info_table(soup)
        market_cap = get_value(table_right_side, 0)
        stock_info['market cap'] = market_cap
        beta = get_value(table_right_side, 1)
        stock_info['beta'] = beta
        pe_ratio = get_value(table_right_side, 2)
        stock_info['PE ratio'] = pe_ratio
        eps = get_value(table_right_side, 3)
        stock_info['EPS'] = eps
        earnings_date = get_value(table_right_side, 4)
        stock_info['earnings date'] = earnings_date
        dividend_and_yield = get_value(table_right_side, 5)
        stock_info['dividend and yeild'] = dividend_and_yield
        ex_dividend_date = get_value(table_right_side, 6)
        stock_info['ex-dividend date'] = ex_dividend_date
        one_year_target_est = get_value(table_right_side, 7)
        stock_info['1 yr target est.'] = one_year_target_est

        return stock_info

''' usage:
quote = YahooStockQuote('MMM')
print(quote.symbol, quote.stock_info)
'''
