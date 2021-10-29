"""
Scraper Template 
@author Ed Chadwick 2021

Important disclaimer:
    This is not a perfect crawler, just a template I keep so I don't have to reinvent it every time I need one.
    
    Also, please don't use this for illegal shit. Thanks.
"""
import requests, csv, re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
pageList = []
excludeList=['@'] #populate this with keywords found in URLs you don't want to check 
start = input('Enter Starting url: ') #the starting page to branch from - currently only supports index pages
if 'http' not in start:
    start = 'https://' + start
domain = urlparse(start).netloc
print('domain is '+domain)
pageList.append(start)
for page in pageList:
    linkList = []
    print("Searching "+page)
    try:
        response = requests.get(page)
    except:
        print("Failed to connect to "+page)
    if(response.status_code == 200):
        #get all links on the page
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            allLinks = soup.findAll('a', href=True)
            for l in allLinks:
                linkList.append(l['href'])
        except:
            print('Parsing failed on '+page)
            
        """
        Add more BeautifulSoup queries here to grab different things from the page.
        """
            
        #This section finds all the links on the page that are descendents of the starting page and adds them to the list if they aren't already there.
        for t in linkList:
            """
            Add checks here to look for links of a certain kind to store if that's what you're looking for.
            """
            #this part curates the links so the crawler navigates sensibly. Works OK, but still improve it 
            #print("checking: "+t)
            if(len(t)>0):
                #get rid of variable arguments.
                t = t.split('?')[0]
                #if (t[0] == '/'): 
                    #t = page + t
                if ((re.match('[a-z]',t[0])) and ('http' not in t))or(t[0] == '/'):
                    t = 'https://'+domain + "/" + t
                #add appropriate links to the pagelist to be checked if they aren't there already
                if (domain in t) and (t not in pageList) and not(any(bad in t for bad in (excludeList))):
                    pageList.append(t)
                    #print('adding '+t)
    else:
        print("Page "+page+" returned error "+str(response.status_code))
        
        
#chuck everything into a csv file
with open(domain.split('.')[0]+'_URLs.csv', mode = 'w') as csvFile:
    csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvWriter.writerow(['Page URL'])
    for entry in pageList:
        csvWriter.writerow([entry])

print(len(pageList))
print(pageList)