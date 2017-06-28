# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import requests
from lib import myparser
import time

class search_yahoo:

    def __init__(self, word, limit, useragent, proxy=None):
        self.engine_name = "Yahoo"
        self.word = word
        self.total_results = ""
        self.server = "search.yahoo.com"
        self.hostname = "search.yahoo.com"
        self.headers = {'User-agent':useragent}
        self.limit = int(limit)
        self.proxies = proxy
        self.counter = 0

    def do_search(self):
        try:
            url = "http://{0}/search?q={1}&b={2}&pz=10".format(self.server,self.word,self.counter) #  %40=@ 搜索内容如：@meizu.com;在关键词前加@有何效果呢？，测试未发现不同
        except Exception, e:
            print e
        try:
            r = requests.get(url, headers = self.headers, proxies = self.proxies)
            self.results = r.content
            self.total_results += self.results
        except Exception,e:
            print e

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            time.sleep(1)

            print "\tSearching " + str(self.counter) + " results..."
            self.counter += 10

    def get_emails(self):
        rawres = myparser.parser(self.total_results, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.total_results, self.word)
        return rawres.hostnames()
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        print "[-] {0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e))
        return self.d, self.e

if __name__ == "__main__":
        print "[-] Searching in yahoo:"
        useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        search = search_yahoo("meizu.com", '100', useragent)
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts  # test passed