import urllib.request
from bs4 import BeautifulSoup
import re
import time
import sys
from threading import Thread
from collections import deque
TIMEOUT=15
RANGE=1000
DOMAINNAME="https://www.mctrgit.ac.in"
counter = 0
List=list()
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
    #print(counter,current_url)
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
    root_url = DOMAINNAME
    start_time = time.time() * 1000
    url_dict = {root_url:0}
    url_queue = deque()
    global counter
    global RANGE
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
        #print("Range:",Range,"Dict",len(url_dict))
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
    total_time=int(end_time)-int(start_time)
    #dict_file = open('RangeTesting.txt', 'a')
    #dict_file.write("Range:"+str(RANGE))
    #dict_file.write("Time:"+ str(total_time)+"ms")
    #dict_file.write("Dict size:"+str(len(url_dict)))
    #dict_file.write("Queue size:"+str(len(url_queue)))
    #dict_file.write("\n\n--------------------\n\n")
    #dict_file.write("Deleted size"+str(len(deleted)))
    ll=list()
    ll.append(RANGE)
    ll.append(total_time)
    List.append(ll)
    # print("\n\n--------------------\n\n")
    print("Range",str(RANGE))
    # print("\nTime", int(end_time)-int(start_time), "ms")
    # #print("Dict size", len(url_dict))
    #print("Queue size", len(url_queue))
    #print("Deleted size", len(deleted))
    
    #for e in url_dict:
    #    dict_file.write(e + '\n')
    #dict_file.close()
def trial():
    i=1
    while(i<=2000):
        global RANGE
        RANGE=i
        crawler()
        if i==1:
            i=2
        elif i<50:
            i+=4
        elif i<100:
            i+=8
        else:
            i+=100

def main():
    #dict_file = open('RangeTesting.txt', 'w')
    #dict_file.close()
    global List
    new_list = []
    for _ in range(5):
        trial()
        List.sort(key=lambda a:a[1])
        new_list.append(List)
        List = []

    #List.sort(key=lambda a:a[1])
    print("############################################")
    sys.stdout = open('RangeTesting.txt', 'a')
    print("############################################")
    print("Domain Name",DOMAINNAME)
    print("Range","\tTime")
    print("----------------")
    for k, e in enumerate(new_list):
        print(k)
        for i in e:
            print(i[0],"\t",i[1],"\n")   

    List = []
    for e in new_list:
        for el in e:
            List.append(el)

    List.sort(key = lambda x: x[1])
    print ("#####################CUMMULATIVE#############################")
    fullAvg=0
    for i in List:
        fullAvg+=i[1]
        print(i[0],"\t",i[1],"\n")  
    fullAvg/=len(List)
    print("Average time",fullAvg)
    List.sort()
    avg_list=list()
    temp=list()
    count = 0
    count1=0
    sum=0
    for element in List:
        if(element[1]<fullAvg+1000):
            count1+=1
            sum+=element[1]
        temp.append(element[1])
        if count==len(new_list) - 1:
            avg=sum/count1
            avg_list.append([element[0],avg,temp])
            temp=[]
            sum = 0
            count=0
            count1=0
            continue
        count+=1
    #print(avg_list)

    avg_list.sort(key = lambda x: x[1])    
    for each in avg_list:
        print(each)
    
    
main()    
        
    
        
             

#print(str(urllib.request.urlopen("https://www.yahoo.com/politics/").read()))
