# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 12:52:50 2014

@author: andreas
"""

from bs4 import BeautifulSoup as Soup
import urllib2
import ast
from matplotlib.cbook import flatten

"""
url = 'http://www.taiwanteacrafts.com/shop/product-category/tea/'
page = urllib2.urlopen(url)
soup = Soup(page)
urls = [link.get('href') for link in soup.find_all('a')]
newurls = []
for i,link in enumerate(urls):
    if 'http://www.taiwanteacrafts.com/product/' in link:
        lst = link.split('/')
        link = '{}//{}/{}/{}/'.format(lst[0],lst[2],lst[3],lst[4])
        newurls.append(link)
newurls = list(set(newurls))
for url in newurls:
    print url
"""
class TeaError(Exception):
    pass
    
class TaiwanTeaDB(object):
    
    def __init__(self, url = 'http://www.taiwanteacrafts.com/shop/product-category/tea/'):
        self.url = url
    
    def get_tea_pages(self, verbose = False):
        pages = []
        self.baseurls = []
        for i in range(1, int(1e4)):
            try:
                url = self.url + 'page/{}/'.format(i)
                page = urllib2.urlopen(url)
                soup = Soup(page)
                pages.append(soup)
                self.baseurls.append(url)
                if verbose:
                    print('Downloaded html from {}'.format(url))
            except:
                break
        if verbose: print('\n')
        return pages
    
    def find_tea_urls(self, soup):
        teaurls = []
        urls = [link.get('href') for link in soup.find_all('a')]
        for link in urls:
            if 'http://www.taiwanteacrafts.com/product/' in link:
                lst = link.split('/')
                newlink = '{}//{}/{}/{}/'.format(lst[0], lst[2], lst[3], lst[4])
                teaurls.append(newlink)
        return teaurls
    
    def get_tea_info(self,teaurl, verbose = False):
        try:
            page = urllib2.urlopen(teaurl)
        except:
            raise TeaError, "The url {} is not a working address".format(teaurl)
        soup = Soup(page)
        name = soup.find_all('h1','product_title entry-title')[0]
        descr = soup.find_all('div',itemprop="description")[0]
        descr = descr.text
        name = name.string
        
        teastyle = None
        if "Green" in name of "green" in name:
            teastyle = "Green"
        if "Black" in name or "black" in name:
            teastyle = "Black"
        if "Oolong" in name or "oolong" in name:
            teastyle = "Oolong"
        else:
            teastyle = "Unknown"
        
        try:
            prices = soup.find_all('form','variations_form cart')[0] #Tins doesn't have this
        except: 
            return False
        prices = prices['data-product_variations']
        prices = prices.replace('false','False'); prices = prices.replace('true','True')
        prices = ast.literal_eval(prices)
        newprice = dict()
        for i, dic in enumerate(prices):
            weightstring = dic['attributes']['attribute_pa_weight']
            try:
                weight = '{}-{}'.format(weightstring.split('-')[0],weightstring.split('-')[1])
                pricestring = dic['price_html']
                pricestring = Soup(pricestring)
                price = tuple(pricestring.get_text().split(' ')) #if there is a sale, more than one price is going to be here
                newprice[weight] = price
            except:
                pass
        try:
            style = tuple(soup.find_all(text='Style of tea')[0].next.next.next.text.split(','))
        except:
            style = False
        try:
            date = tuple(soup.find_all(text='Picking Date')[0].next.next.next.text.split(','))
        except:
            date = False
        try:
            try: #Spelled incorrectly on the webpage. Might be fixed in the near future
                oxidation = tuple(soup.find_all(text='Oxydation level')[0].next.next.next.text.split(','))
            except:
                oxidation = tuple(soup.find_all(text='Oxidation level')[0].next.next.next.text.split(','))
        except:
            oxidation = False
        try:
            roasting = tuple(soup.find_all(text='Roasting Level')[0].next.next.next.text.split(','))
        except:
            roasting = False
        try:
            terroir = tuple(soup.find_all(text='Terroir')[0].next.next.next.text.split(','))
        except:
            terroir = False
        try:
            region = tuple(soup.find_all(text='Administrative Region')[0].next.next.next.text.split(','))
        except:
            region = False
        try:
            picking = tuple(soup.find_all(text='Picking Style')[0].next.next.next.text.split(','))
        except:
            picking = False
        try:
            cultivars = tuple(soup.find_all(text='Cultivar(s) Used')[0].next.next.next.text.split(','))
        except:
            cultivars = False
        try:
            elevation = tuple(soup.find_all(text='Garden Elevation')[0].next.next.next.text.split(','))
        except:
            elevation = False
        if verbose:
            print('Successfully retrieved tea info from {}'.format(teaurl))
        return {'name':name, 'style':teastyle, 'prices':newprice, 'information':{'description':descr,
        'pickdate': date, 'style':style, 'oxidation':oxidation, 'roasting':roasting, 
        'terroir':terroir, 'region':region, 'pickstyle':picking, 'cultivars':cultivars,
        'elevation':elevation},'url':teaurl}
    
    def flatten_urls(self, newurls):
        newurls  = list(set(list(flatten(newurls)))) #Turn it into one list, remove duplicates and turn it into a list again
        return newurls
    
    def main(self, verbose = False):
        basesouplist = self.get_tea_pages(verbose)
        teaurlslist = []
        for soup in basesouplist:
            teaurlslist.append(self.find_tea_urls(soup))
        teaurls = self.flatten_urls(teaurlslist)
        teadb = dict()
        for teaurl in teaurls:
            specteadb = self.get_tea_info(teaurl, verbose)
            if not specteadb == False:
                teadb[specteadb['name']] = specteadb
        if verbose: print('\n')
        return teadb

if __name__ == "__main__":
    obj = TaiwanTeaDB()
#    teaurl = 'http://www.taiwanteacrafts.com/product/1982-sun-moon-lake-aged-black-tea-lot-220/'
#    lst = obj.get_tea_pages()
#    for item in lst:
#        print obj.find_tea_urls(item)
    teadb = obj.main(True)
    print teadb
#    print obj.get_tea_info(teaurl)
            
            
            