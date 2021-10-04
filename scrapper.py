from bs4 import BeautifulSoup
import requests, urllib.parse, lxml

class ScrapNews():

    def __init__(self):
      pass
    def scrape(self,query):
        all_news={'title': [],'date': []}
        li_url="https://www.google.com/search?q="+query+"&tbm=nws&sxsrf=AOaemvJ3xg4cdnrpZwy6USE5NEAN4oDFNw:1632813407467&source=lnt&tbs=sbd:1&sa=X&ved=2ahUKEwjuqIv5j6HzAhWyS_EDHS0zAr8QpwV6BAgBECk&biw=1853&bih=981&dpr=1"
        page=requests.get(li_url, timeout=20)
        soup=BeautifulSoup(page.text,'lxml')
        
        Titles=soup.find_all('h3')
        for title in Titles:
            if (title.text is not None):
                all_news["title"].append(title.text)

        Dates=soup.find_all('span')
        for date in Dates[8:-6]:
            if ("ago" in date.text):
                all_news["date"].append(date.text)


        return all_news
