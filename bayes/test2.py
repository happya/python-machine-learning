'''
a test python file for ads apt using feedparser package

@ author yyi
'''

import feedparser
from bayes import *

ny = feedparser.parse('http://newyork.craigslist.org/search/stp?format=rss')
sf = feedparser.parse('http://sfbay.craigslist.org/search/stp?format=rss')
# print ny['entries'][0]['summary']
# vocalList, pSF, pNY = localWords(sf, ny)
getTopWords(ny, sf)