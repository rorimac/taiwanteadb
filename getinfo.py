# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 12:52:50 2014

@author: andreas
"""

from bs4 import BeautifulSoup as Soup
import urllib2

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
    
class TaiwanTeaDB(object):
    
    def __init__(self):
        self.url = 'http://www.taiwanteacrafts.com/shop/product-category/tea/'
    
    def get_tea_pages(self):
        pages = []
        for i in range(1, 1e10):
            try:
                url = self.url + 'page/{}/'.format(i)
                page = urllib2.urlopen(self.url)
                soup = Soup(page)
                pages.append([url,soup])
            except:
                break
        return pages
    
    def find_tea_urls(self, page):        
        teaurls = []
        urls = [link.get('href') for link in soup.find_all('a')]
        for link in urls:
            if 'http://www.taiwanteacrafts.com/product/' in link:
                lst = link.split('/')
                newlink = '{}//{}/{}/{}/'.format(lst[0], lst[2], lst[3], lst[4])
                teaurls.append(newlink)
            
            
            
            