# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:34:55 2014

@author: andreas
"""

import getinfo as gi
import teadatabase as tea
import numpy as np

class TeaError(Exception):
    pass

class TaiwanTea(object):
    def __init__(self, url = 'http://www.taiwanteacrafts.com/shop/product-category/tea/', database = 'teadatabase.sqlite'):
        self.db = tea.TeaDatabase(database)
        self.gettea = gi.TaiwanTeaDB(url)
        self.url = url
        self.teapages = []
        self.teaurls = []
        self.baseurls = []
    
    @staticmethod
    def list_to_string(lst):
        s = str(lst)
        s.replace("'", ""); s.replace('"',''); s.replace("[",""); s.replace("]","")
        return s
        
    @staticmethod
    def tuple_to_string(tpl):
        s = str(tpl)
        s.replace("'", ""); s.replace('"',''); s.replace("(",""); s.replace(")","")
        return s
    
    def getTeaPages(self, verbose = False):
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
        
    def findTeaUrls(self, soup):
        teaurls = []
        urls = [link.get('href') for link in soup.find_all('a')]
        for link in urls:
            if 'http://www.taiwanteacrafts.com/product/' in link:
                lst = link.split('/')
                newlink = '{}//{}/{}/{}/'.format(lst[0], lst[2], lst[3], lst[4])
                teaurls.append(newlink)
        return teaurls
    
    def getTeaInfo(self, teaurl, verbose = False):
        try:
            page = urllib2.urlopen(teaurl)
        except:
            raise TeaError, "The url {} is not a working address".format(teaurl)
        soup = Soup(page)
        name = soup.find_all('h1', 'product_title entry-title')[0]
        descr = soup.find_all('div', itemprop="description")[0]
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
            prices = soup.find_all('form', 'variations_form cart')[0] #Tins doesn't have this
        except: 
            return False
        prices = prices['data-product_variations']
        prices = prices.replace('false', 'False'); prices = prices.replace('true', 'True')
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
    
    def addTeaToDatabase(self, teadict):
        teaname = teadict['name']
        teanamesdb = self.db.listTeas()
        timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not teaname in teanamesdb:
            try:
                priceid = db.putPrices(**teadict['prices'])
                informationid = db.putInformation(**teadict['information'])
                db.putTea(teaname, teadict['style'], teadict['url'], informationid, priceid)
            except:
                raise TeaError, "The tea weren't in the database but couldn't be added to it."
            
        elif teaname in teanamesdb:
            teaentry = db.getTeaByName(teaname)
            if len(teaentry) > 1:
                raise TeaError, "More than one tea with the name {} exist in the database".format(teaname)
            teaentry = teaentry[0]
            priceid = teaentry[-2]
            priceentry = db.getPrices(priceid)[0]
            entryprices = [priceentry[i].split(',') for i in range(1,len(priceentry)-1)]
            teaprices = [self.tuple_to_string(price) for price in teaentry['prices'].values()]
            if not (np.sort(entryprices) == np.sort(teaprices)).all():
                pass
            
            
        