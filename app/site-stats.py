from lxml import etree
import requests, sys
import urllib.request
from time import time

pages = []
r = requests.get("http://hypercharged.herokuapp.com/sitemap.xml", headers={'User-Agent': 'Mozilla/5.0'})
root = etree.fromstring(r.content)
#   print "The number of sitemap tags are {0}".format(len(root))
for sitemap in root:
    pages.append(sitemap.getchildren()[0].text)
for page in pages:
    p = urllib.request.urlopen(page)
    b = time()
    output = p.read()
    p.close()
    e = time()
    p.close()
    print(e-b, page, "Fast" if (e-b < 0.5) else "Slow")
