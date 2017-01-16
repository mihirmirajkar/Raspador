import urllib.request
from bs4 import BeautifulSoup
import re
import time
from threading import Thread
from collections import deque
TIMEOUT=15
RANGE=1000
DOMAINNAME="https://en.wikipedia.org"
counter = 0

def linkConstruction(parent,urls):
    for i,url in enumerate(urls):
        if url[0]=='#':
            url = parent
        if url == '\\':
            url = parent        #lot of scope for optimization here!
        try:
            domain_index = parent.index('/',8)
            parent = parent[:domain_index]
        except Exception:
            pass
        if(url[0] == '/'):
            try:
                if(url[1] == '/'):
                    urls[i] = "https:" + url
                
                else:
                    urls[i] = parent + url
            except Exception:
                urls[i] = parent + url
        else:
            if url[:4] != 'http':
                urls[i] = parent + '/' + url
                
                
    return urls

def search_links(current_url,threadUrls):
    global counter
    urls=list()
    page_content=""
    try:
        page_content = str(urllib.request.urlopen(current_url,timeout=TIMEOUT).read())
    except Exception as e:
        return
    urls = re.findall('href=[\'"]?([^\'" >]+)',page_content)
    urls = linkConstruction(current_url, urls)
    #print("Inside",urls)
    threadUrls.append(urls)
    print(counter,current_url)
    counter+=1
    #print("ThreadUrls",threadUrls)

def update_struct(url_dict,urls,url_queue):
    #print("URLS",urls)
    for url in urls:
        if url not in url_dict:
            url_dict[url] = 0
            url_queue.append(url)
    return url_dict, url_queue

def reduce_links(threadUrls):
    #print("ThreadUrls",threadUrls)
    tempUrlDict={}
    flag=0
    for each in threadUrls:
        for url in each:
            if url not in tempUrlDict:
                flag=1
                tempUrlDict[url] = 0
    urls=list()
    if flag == 0:
        return urls
    #print("Dict",tempUrlDict)
    for key, value in tempUrlDict.items():
        urls.append(key)
    return urls    

def crawler():
    domainName=DOMAINNAME
    root_url = "https://en.wikipedia.org/wiki/Sun"
    start_time = time.time() * 1000
    url_dict = {root_url:0}
    url_queue = deque()
    global counter
    page_content = str(urllib.request.urlopen(root_url,timeout=TIMEOUT).read())
    #print(page_content)
    urls = re.findall('href=[\'"]?([^\'" >]+)',page_content)
    #print(urls)
    urls = linkConstruction(root_url, urls)
    url_dict,url_queue = update_struct(url_dict, urls, url_queue)
    url_dict[root_url] = 1
    #deleted = list()
    #print(counter, root_url)
    #counter += 1
    while len(url_queue) > 0:
        Range=RANGE        #This is the number of threads you want to create
        if(len(url_queue)<Range):
            Range=len(url_queue)
        threads=list()
        threadUrls=list()
        #print("Range",Range)
        print("Range:",Range,"Dict",len(url_dict))
        for i in range(Range):
            try:
                current_url = url_queue.popleft()
            except:
                break
            try:
                domain_index = current_url.index('/',8)
                parent = current_url[:domain_index]
            except Exception:
                parent=current_url
            if(parent!=domainName):
                Range+=1
                continue
            threads.append(Thread(target=search_links, args=(current_url,threadUrls)))
            #print(counter, current_url)
            #counter+=1
            #deleted.append(current_url)
        try:
            for x in threads:
                x.start()
                #print("Started",x)
            for x in threads:
                x.join()
                #print("Ended",x)
            
        except:
            print ("Error: unable to start thread no.",current_url)
        #print("ThreadUrls",threadUrls)
        urls=reduce_links(threadUrls)
        url_dict,url_queue=update_struct(url_dict, urls, url_queue)
        url_dict[current_url] = 1
          
        if counter > 5000: #Counter changes here
            break
    end_time = time.time() * 1000
    dict_file = open('dict_thread2.txt', 'w')
    dict_file.write("Time"+ str(int(end_time)-int(start_time))+"ms")
    dict_file.write("Dict size"+str(len(url_dict)))
    dict_file.write("Queue size"+str(len(url_queue)))
    #dict_file.write("Deleted size"+str(len(deleted)))
    
    print("Time", int(end_time)-int(start_time), "ms")
    print("Dict size", len(url_dict))
    print("Queue size", len(url_queue))
    #print("Deleted size", len(deleted))
    
    for e in url_dict:
        dict_file.write(e + '\n')
    dict_file.close()
        
crawler()
#print(str(urllib.request.urlopen("https://www.yahoo.com/politics/").read()))
