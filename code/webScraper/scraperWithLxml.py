import urllib
import lxml.html
connection = urllib.urlopen('http://www.nytimes.com')

dom =  lxml.html.fromstring(connection.read())

for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
    print(link)
