import urllib.request
import re

def linkConstruction(parent,urls):
    for i,url in enumerate(urls):
        if(url[0]=='/'):
            urls[i]=parent+url
            
    return urls
    
def crawler():
    
    root_url="http://www.duckduckgo.com"
    page_content=str(urllib.request.urlopen(root_url).read())
    #print(page_content)
    urls = re.findall('href=[\'"]?([^\'" >]+)',page_content)
    urls=linkConstruction(root_url, urls)
    print(urls)
        
crawler()

