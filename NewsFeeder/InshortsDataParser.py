__author__ = 'Rishijeet Mishra'

from bs4 import BeautifulSoup
import requests
import urllib2
import re

URL = "https://www.inshorts.com/en"
NEWS_ID = "" # default key


class InshortsDataParser(object):

    def __init__(self, max_news_page):
        self.url_post = URL + "/ajax/more_news"
        self.min_news_id = NEWS_ID
        self.max_news_page = max_news_page
        self.url_main = URL + "/read"

    def other_pages_read(self):
        i = 0
        news_list = []
        while (i < self.max_news_page):
            payload = {"category":"", "news_offset": self.min_news_id}
            # POST with form-encoded data
            r = requests.post(self.url_post, data=payload)
            key_new = eval(r.text)['min_news_id']
            html = eval(r.text)['html']
            self.min_news_id = key_new
            news_list.append([self.min_news_id, html])
            i += 1
        return news_list

    def news_parser(self):
        tweet_list = []
        for (key, html) in self.all_pages():
            print "called with key = " + str(key)
            soup = BeautifulSoup(html, 'html.parser')
            all_divs = soup.find_all('div', itemprop="articleBody")
            for item in all_divs:
                tweet_list.append(str(item).split("<div itemprop=\"articleBody\">")[1].split("</div>")[0])
        return tweet_list

    def first_page_read(self):
        page = urllib2.urlopen(self.url_main).read()
        soup = BeautifulSoup(page, 'html.parser')
        key_page_list = []
        find_text_for_key = soup.find_all('script', type="text/javascript")
        for item in find_text_for_key:
            m = re.search('var\s+min_news_id\s+=\s+"(.*)";', str(item))
            if m:
                self.min_news_id = m.group(1)
                print "first key found = " + str(self.min_news_id)
                key_page_list.append([self.min_news_id, page])
        return key_page_list

    def all_pages(self):
        first_page_list = self.first_page_read()
        subsequent_page_list = self.other_pages_read()
        return first_page_list + subsequent_page_list

if __name__ == "__main__":
    c = InshortsDataParser(10)
    for tw in c.news_parser():
        print tw

