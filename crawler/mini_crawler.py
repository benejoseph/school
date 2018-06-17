import re
import requests
from Queue import Queue
import sys
import argparse

LINK_REGEX='href=[\'"]?([^\'" >]+)'
DOMAIN_REGEX= 'http[s]?://[www]?[\w|\.]+/'
TEXT_REGEX='<p>.*</p>'

class Crawler(object):
  def __init__(self):
    self.links_re = re.compile(LINK_REGEX)
    self.domain_re = re.compile(DOMAIN_REGEX)
    self.text_re = re.compile(TEXT_REGEX)
    self.max_depth = 10
    self.max_links = 100
    self.n = 0  
 
  def get_domain(self, url):
    #this method needs some work, it definitely misses 
    # foo.mydomain.com vs bar.mydomain.com will yield different domains
    try:
      my_domain = self.domain_re.search(url).group(0)
    except Exception:
      return None
 
    return my_domain.split('/')[-2]

  # Does breadth-first search of all links which have the same domain
  def get_outgoing_links(self, url):
    my_domain = self.get_domain(url)
    print 'Domain=%s' % (my_domain)

    if my_domain is None:
      return

    q = Queue()
    q.put(url)

    while not q.empty():
      self.n += 1
      if self.n > self.max_links:
        return

      url = q.get()
      print url
      v = requests.get(url)
      if not v.ok:
        continue


      #TODO put parsing of page text here
      print self.text_re.findall(v.text)
      links = self.links_re.findall(v.text)
      for link in links:
        if link == url:
          continue

        domain = self.get_domain(link)

        if domain != my_domain:
          continue

        q.put(link)

if __name__ == '__main__':
  c = Crawler()
  c.get_outgoing_links('https://littleseedschildrenscenter.com/')
