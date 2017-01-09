import urllib.request
import re
import time

def linkConstruction(parent,urls):
    for i,url in enumerate(urls):
        if(url[0]=='/'):
            try:
                domain_index=parent.index('/',8)
                parent=parent[:domain_index]
            except Exception:
                pass
            try:
                if(url[1]=='/'):
                    urls[i]="http:"+url
                
                else:
                    urls[i]=parent+url
            except Exception:
                urls[i]=parent+url
    return urls
def update_struct(url_dict,urls,url_queue):
    for url in urls:
        if url not in url_dict:
            url_dict[url]=0
            url_queue.append(url)
    return url_dict,url_queue
def crawler():
    
    root_url="https://en.wikipedia.org/wiki/Sun"
    counter=0
    start_time=time.time()*1000
    url_dict={root_url:0}
    url_queue=list()
    page_content=str(urllib.request.urlopen(root_url).read())
    #print(page_content)
    urls = re.findall('href=[\'"]?([^\'" >]+)',page_content)
    #print(urls)
    urls=linkConstruction(root_url, urls)
    url_dict,url_queue=update_struct(url_dict, urls, url_queue)
    url_dict[root_url]=1
    #print(urls)
    deleted=list()
    while len(url_queue)>0:
        current_url=url_queue[0]
        print(counter,current_url)
        try:
            page_content=str(urllib.request.urlopen(current_url).read())
        except Exception:
            del url_queue[0]
            continue
        urls = re.findall('href=[\'"]?([^\'" >]+)',page_content)
        urls=linkConstruction(current_url, urls)
        url_dict,url_queue=update_struct(url_dict, urls, url_queue)
        url_dict[current_url]=1
        deleted.append(url_queue[0])
        del url_queue[0]
        counter+=1      
        if counter==100: #Counter changes here
            break
    end_time=time.time()*1000
    print("Time",int(end_time)-int(start_time),"ms")
    print("Dict size",len(url_dict))
    print("Queue size",len(url_queue))
    print("Deleted",len(deleted),deleted)
        
crawler()
#print(str(urllib.request.urlopen("http://www.youtube.com/www.youtube.com/upload").read()))
