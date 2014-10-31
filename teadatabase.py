# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 21:37:11 2014

@author: andreas
"""

import sqlite3, os

class TeaDatabase(object):
    
    def __init__(self, database = 'teadatabase.sqlite'):
        
        sqlite3.register_adapter(list, list_to_string)
        sqlite3.register_adapter(tuple, tuple_to_string)
        
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        
        self.cur.execute('''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name''')
        ans = self.cur.fetchall()

        if not ('tea',) in ans:
            print("Creating table 'tea'...")
            self.cur.execute('''CREATE TABLE tea (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, style TEXT, url TEXT, information INTEGER, prices INTEGER, timestamp TEXT)''')
        
        if not ('information',) in ans:
            print("Creating table 'information'...")
            self.cur.execute('''CREATE TABLE information (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, pickdate TEXT, style TEXT, oxidation TEXT, roasting TEXT, terroir TEXT, region TEXT, pickstyle TEXT, cultivar TEXT, elevation TEXT)''')
        
        if not ('prices',) in ans:
            self.cur.execute('''CREATE TABLE prices (id INTEGER PRIMARY KEY AUTOINCREMENT, 25-g TEXT, 50-g TEXT, 150-g TEXT, 300-g TEXT, 600-g TEXT, timestamp TEXT) ''')
    
    @staticmethod
    def list_to_string(lst):
        s = str(lst)
        s.replace("'", ""); s.replace('"',''); s.replace("[",""); s.replace("]","")
        return s
    
    @staticmethod
    def adapt_list(lst):
        return TeaDatabase.list_to_string(lst)
        
    @staticmethod
    def tuple_to_string(tpl):
        s = str(tpl)
        s.replace("'", ""); s.replace('"',''); s.replace("(",""); s.replace(")","")
        return s
    
    @staticmethod
    def adapt_list(lst):
        return TeaDatabase.tuple_to_string(lst)
        
    def listTeas(self):
        teas = self.cur.execute('SELECT * FROM tea ORDER BY id')
        return teas.fetchall()
    
    def getTea(self, _id):
        tea = self.cur.execute('SELECT * FROM tea WHERE id=?', _id)
        return tea.fetchall()
    
    def getTeaByName(self, _name):
        tea = self.cur.execute('SELECT * FROM tea WHERE name=?', _name)
        return tea.fetchall()
    
    def getTeaByUrl(self, _url):
        tea = self.cur.execute('SELECT * FROM tea WHERE url=?', _url)
        return tea.fetchall()
    
    def getTeasByType(self, _type):
        tea = self.cur.execute('SELECT * FROM tea WHERE type=?', _type)
        return tea.fetchall()
    
    def putTea(self, name, teatype, teaurl, info, prices, timenow = None):
        if timenow == None:
            timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute('INSERT INTO tea VALUES (NULL, ?, ?, ?, ?, ?, ?)', (
        name, teatype, teaurl, info, prices, timenow))
    
    def putPrices(self, g_25 = None, g_50 = None, g_150 = None, g_300 = None, 
                  g_600 = None, timenow = None):
                      
        if timenow == None:
            timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute('INSERT INTO prices VALUES (NULL, ?, ?, ?, ?, ?, ?)', (
        g_25, g_50, g_150, g_300, g_600, timenow))
        return self.cur.lastrowid
    
    def getPrices(self, _id):
        prices = self.cur.execute('SELECT * FROM prices WHERE id=?', _id)
        return prices.fetchall()
    
    def updatePrices(self, priceid g_25 = None, g_50 = None, g_150 = None, g_300 = None, 
                     g_600 = None, timenow = None):
        if timenow == None:
            timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute('UPDATE prices VALUES (NULL, ?, ?, ?, ?, ?, ?) WHERE id = ?', (
        g_25, g_50, g_150, g_300, g_600, timenow), priceid)
                      
    
    def putInformation(self, description = None, pickdate = None, style = None, 
                       oxidation = None, roasting = None, terroir None, 
                       region = None, pickstyle = None, cultivar = None, 
                       elevation = None):
                           
        self.cur.execute('INSERT INTO information VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
        description, pickdate, style, oxidation, roasting, terroir, region, pickstyle, cultivar, elevation))
        return self.cur.lastrowid
    
    def getInformation(self, _id):
        information = self.cur.execute('SELECT * FROM information WHERE id=?', _id)
        return information.fetchall()
    
    def save(self):
        self.conn.commit()
    
    