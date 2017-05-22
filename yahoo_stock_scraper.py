import requests
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

    def current_value(self, soup):
        crnt_price = soup.find('span', {'data-reactid': '36'}).get_text()
        return crnt_price

    def get_info(self):

        def get_value(table, row):
            table_row = list(table.children)[row]
            value = list(table_row.children)[1].get_text()
            return value

        soup = self.soupify_page()
        stock_info = {}

        # after 4pm EST curent price is the closing prices as well
        crnt_price = self.current_value(soup)
        stock_info['cur. price'] = crnt_price

        '''get left side table info'''
        table_left_side = self.get_left_side_info_table(soup)
        left_values = ['prev close', 'open price', 'bid value', 'ask value', "day's range",
                  '52 week range', 'volume', 'avg. volume']
        for i, value in enumerate(left_values):
            stock_info[value] = get_value(table_left_side, i)

        '''get right side table info'''
        table_right_side = self.get_right_side_info_table(soup)
        right_values = ['market cap', 'beta', 'PE ratio', 'EPS', 'earnings date',
                       'dividend and yield', 'ex-dividend date', '1 yr target est.']
        for i, value in enumerate(right_values):
            stock_info[value] = get_value(table_right_side, i)

        return stock_info

'''
#usage:
quote = YahooStockQuote('MMM')
print(quote.symbol, quote.stock_info)
'''
