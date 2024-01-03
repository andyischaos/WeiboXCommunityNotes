

#%% load packages
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib
import pandas as pd
import regex as re
import time
#%% scrape all the webpages
# discern the type of document
## test
testurl = "https://www.politifact.com/factchecks/list/"
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'
HEADERS = {'User-agent':user_agent}
req = urllib.request.Request(testurl, headers = HEADERS) # visit disguised as browser
pagehtml = urllib.request.urlopen(req).read() # read the website
pagesoup = soup(pagehtml)


# Finding all the list items by class 'o-listicle__item'
list_items = pagesoup.find_all('li', class_='o-listicle__item')

# List to hold all extracted data
extracted_data = []

# Iterating over each list item to extract the required information
for item in list_items:
    # Extracting the author, content, body, quote wrap, quote, and link
    claimer = item.find('div', class_='m-statement__author').get_text(strip=True) if item.find('div', class_='m-statement__author') else None
    quote_wrap = item.find('div', class_='m-statement__quote-wrap').get_text(strip=True) if item.find('div', class_='m-statement__quote-wrap') else None
    link = item.find('a')['href'] if item.find('a') else None
    rating = item.find('div', class_='c-image')
    # Find the 'img' tag within the 'div' with the class 'm-statement__quote-wrap'
    img_src = item.find('div', class_='m-statement__meter').find('img')['src']
    author = item.find('footer', class_='m-statement__footer').get_text(strip=True) if item.find('footer', class_='m-statement__footer') else None
    # Appending the extracted data to the list
    extracted_data.append({
        'claimer': author,
        'content': quote_wrap,
        'link': link,
        'rating':img_src,
        'author-date':author
    })

# Output the extracted data
print(extracted_data)

#%% real code
# Functions
def save_data(dataframe, filename):
    dataframe.to_csv(filename, index=False)

def get_soup(page_number):
    testurl = "https://www.politifact.com/factchecks/list/?page={}".format(str(page_number))
    req = urllib.request.Request(testurl, headers = HEADERS) # visit disguised as browser
    pagehtml = urllib.request.urlopen(req).read() # read the website
    pagesoup = soup(pagehtml)
    return pagesoup    
def process_page(pagesoup):
    list_items = pagesoup.find_all('li', class_='o-listicle__item')
    
    for item in list_items:
        # Extract necessary data from each list item
        name_content = item.find(class_='m-statement__name').get_text()
        desc_content = item.find('div',class_='m-statement__desc').get_text()
        href_content = item.find('div',class_='m-statement__meta').find('a')['href']
        quote_wrap = item.find('div', class_='m-statement__quote-wrap').text.strip()
        link = item.find('div', class_='m-statement__quote').find('a')['href']
        
        # Find the image under the div with class 'm-statement__meter'
        img_element = item.find('div', class_='m-statement__meter').find('img', src=True)
        img_src = img_element['src'].split('/')[-1].split('.jpg')[0] if img_element else ''
        authordate = item.find('footer', class_='m-statement__footer').get_text(strip=True) if item.find('footer', class_='m-statement__footer') else None
        # Append the extracted data to the list
        extracted_data.append({
            'claimer': name_content,
            'when&where': desc_content,
            'claimer_url':href_content,
            'content': quote_wrap,
            'link': link,
            'rating': img_src,
            'author-date': authordate.split('•')[0] if authordate else '',
            'date':authordate.split('•')[1] if authordate else '',
            # This seems to be a duplicate of the 'claimer' field
        })
        
# List to hold all extracted data
extracted_data = []
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'
HEADERS = {'User-agent':user_agent}


page_number = 1
while True:
    pagesoup = get_soup(page_number)
    if pagesoup is None: 
        break
    process_page(pagesoup)
    page_number += 1
    time.sleep(1)
    
if extracted_data:
    df = pd.DataFrame(extracted_data)
    save_data(df, 'politifact_raw.csv')


