from bs4 import BeautifulSoup
import requests

""" This script grabs the Symbol, Company Name, and Industry for
    every stock in the S&P 500 from the wikipedia page that contains
    the list of S&P 500 companies.

    The script is broken up into 5 fuctions which handle each aspect of
    the web scraping process

    get_wiki_page() retrives the page returned by requests using the embedded
    wiki link.

    soupify() takes the page from get_wiki_page() as an argument and using
    BeautifulSoup() and returns a soup

    get_sp_500_table() takes the soup from soupify as an argument and filters
    through the soup to get the table containing the S&P information
    and returns a list of rows in that table

    get_sp_500_holdings() takes the table rows returned from get_sp_500_table as
    an argument and returns a list of dictionaires for each stock holding in the
    format: {'symbol': symbol, 'company_name': company, 'sector': sector}
"""
class ScrapeWikiSP500:
    WIKI = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    HEADER = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self):
        self.sp_500_holdings = self.get_sp_500_holdings()

    def get_wiki_page(self):
        page = requests.get(self.WIKI, headers=self.HEADER)
        return page

    def soupify(self):
        page = self.get_wiki_page()
        soup = BeautifulSoup(page.content, 'lxml')
        return soup

    def get_sp_500_table(self):
        soup = self.soupify()
        table = soup.find('table', {'class': ['wikitable', 'sortable', 'jquery-tablesorter']})
        table_rows = table.find_all('tr')
        return table_rows

    def get_sp_500_holdings(self):
        table_rows = self.get_sp_500_table()
        sp_500_holdings = []
        num_symbols = len(table_rows)
        # in the for loop below, range starts at 1 because index 0 is table header info
        for i in range(1, num_symbols):
            index = i
            row = table_rows[index].find_all('td')
            symbol = row[0].a.get_text()
            company = row[1].a.get_text()
            sector = row[3].get_text()
            sp_500_holdings.append({'symbol': symbol, 'company_name': company, 'sector': sector})
        return sp_500_holdings



''' usage:
sp = ScrapeWikiSP500()
holdings = sp.sp_500_holdings
print(holdings)
'''
