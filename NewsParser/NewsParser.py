__author__ = 'Rishijeet Mishra'

from NewsFeeder.InshortsDataParser import InshortsDataParser

class NewsParser(object):
    def __init__(self, tweetlimit, page):
        self.page = page
        self.tweetlimit = tweetlimit
        self.parsed_news_list = []

    def getShortDataforTweet(self):
        isP = InshortsDataParser(self.page)
        print "got the page"
        for news in isP.news_parser():
            if len(news) > self.tweetlimit:
                self.parsed_news_list.extend(self.magicTweetsSplitter(news)[::-1])
            else:
                self.parsed_news_list.append(news)
        return self.parsed_news_list


    def magicTweetsSplitter(self, line):
        return ['T' +str(k) +': ' + line[i:i+self.tweetlimit-4].strip() for k, i in enumerate(range(0, len(line), self.tweetlimit-4), 1)]


if __name__ == "__main__":
    nP = NewsParser(140, 2)
    for line in  nP.getShortDataforTweet()[::-1]:
        print len(line), line