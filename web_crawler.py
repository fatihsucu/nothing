import urllib2
from bs4 import BeautifulSoup
import re

input_url = ""


def checkout_links(input_url):
    urls = []
    html_page = urllib2.urlopen(input_url).read()
    soup = BeautifulSoup(html_page)
    for line in soup.findAll('a'):
        references = line.get('href')
        if references.startswith('http://'):
            add_straight(urls ,references)
        else:
            new_link = input_url + references
            add_straight(urls, new_link)
    return urls


def add_straight(list_, item):
    if any(item) in list_:
        return False
    else:
        list_.append(item)
    return list_

def spide_all_website(input_url):
    urls = checkout_links(input_url)

    for link in urls:
        try:
            urls =  urls + checkout_links(link)
        except:
            urls.remove(link)
            continue
    return urls

def get_text_content(url):
    html_page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html_page)
    for line in soup.findAll("p"):        
        text = line.get_text().encode('utf8')
        #print dir(re)
        pat = re.findall("[A-Za-z]+", text.decode('utf8'))
        print pat
        
            



get_text_content("http://www.sabah.com.tr")