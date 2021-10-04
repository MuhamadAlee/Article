from nltk.tokenize import sent_tokenize
from GoogleNews import GoogleNews
from scrapper import ScrapNews
from googlesearch import search
from newspaper import Article
from bs4 import BeautifulSoup
import ParaPhrase as phraser
import Summerizer as summ
from datetime import datetime
import HeadlineGeneration
import uploading
import requests, lxml
import random
import string
import heapq
import time
import nltk
import re
import os
import warnings
warnings.filterwarnings("ignore")


class ArtGen:

    def __init__(self):
        #using modules
        self.pp=phraser.Phrase()
        self.sm=summ.Summery()
        self.googlenews = GoogleNews()
        self.scrap=ScrapNews()
        self.tg=HeadlineGeneration.Title_Generation()
        

    def sent_splitter(self,txt):
        sentences=txt.split('.')
        return sentences

    def news(self,query):
        all_news = {'title': [], 'link': [],'headline': [], 'date': []}
        self.googlenews.search(query)
        results=self.googlenews.results(sort=True)
        all_times=[]
        for news in results:
            all_times.append(news["date"])
        least_index=self.time_comparison(all_times)
        news=results[least_index]
        all_news['title'].append(news["title"])
        all_news['link'].append(news["link"])
        all_news['headline'].append(news["desc"])
        all_news['date'].append(news["date"])
            
        return all_news

    def time_comparison(self,times):
        timestamps=['sec','min','hour','day','week','month']
        flag=False
        last=""
        ind=-1
        for ts in timestamps:
            for index,date in enumerate(times):
                if (ts in date) or (ts+'s' in date):
                    val=int(date.split(' ')[0])
                    if (last=="") or (last>val):
                        flag=True
                        ind=index
                        last=val
            if (flag):
                break
        return ind

    def url_removal(self,text):
        text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)
        return text 

    def remove_emoji(self,string):
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    def reconcatenate(self,txt_list):
        paragraph=""
        for sentence in txt_list:
            paragraph+=sentence+". "
        return paragraph

    def news_extraction(self,last,query):
        INTRO=""
        BODY=""
        CON=""
        intro=""
        body=""
        con=""
        # all_news =self.news("cryptocurrency")
        all_news=self.scrap.scrape(query)
        if(len(all_news['date'])==0):
            print("Sorry article will be generated after 15 minutes")
            return "",intro,body,con
        times=all_news['date']
        # print(times)
        ind=self.time_comparison(times)
        query=all_news['title'][ind]
        
        print("News is generated against: \n"+"*"*50+query+"*"*50)
        URLs=search(query,  num_results=10, lang="en")
        
        iteration_flag=True
        if query in last:
            print("Sorry latest Article is already generated")
            return query,intro,body,con
        
        for url in URLs:
            try:
                if(iteration_flag):
                    article = Article(url, language="en")
                    article.download()
                    article.parse()
                    article.nlp()

                    text=article.text
                    text=text.replace('?','.')
                    text=text.replace('"','')
                    text=self.url_removal(text)
                    text=self.remove_emoji(text)
                    sentences=self.sent_splitter(text)
                    intro_count=(len(sentences)//4)
                    body_count=(len(sentences)//2)
                    concolusion_count=(len(sentences)//4)


                    txt=self.reconcatenate(sentences[0:intro_count])
                    INTRO=txt
                    
                    txt=self.reconcatenate(sentences[intro_count:(intro_count+body_count)])
                    BODY=txt
                    
                    txt=self.reconcatenate(sentences[(intro_count+body_count):])
                    CON=txt
                    
                    
                    into_sent=self.sent_splitter(INTRO)
                    body_sent=self.sent_splitter(BODY)
                    con_sent=self.sent_splitter(CON)

                    into_sent=into_sent[:-1]
                    body_sent=body_sent[:-1]
                    con_sent=con_sent[:-1]
                    
                    introduction=""
                    middle=""
                    end=""

                    for sent in into_sent:
                        out=self.pp.rephrase(sent,1)
                        introduction+=out

                    for sent in body_sent:
                        out=self.pp.rephrase(sent,1)
                        middle+=out

                    for sent in con_sent:
                        out=self.pp.rephrase(sent,1)
                        end+=out

                    introduction=self.sm.summerize(introduction,50)
                    middle=self.sm.summerize(middle,60)
                    end=self.sm.summerize(end,60)
                    
                    if len(introduction.split())>60:
                        tokens=introduction.split()
                        introduction=' '.join(tokens[:60]) 

                    if len(middle.split())>120:
                        tokens=middle.split()
                        middle=' '.join(tokens[:120]) 
                    
                    if len(end.split())>60:
                        tokens=end.split()
                        end=' '.join(tokens[:60]) 

                    into_sent=self.sent_splitter(introduction)
                    body_sent=self.sent_splitter(middle)
                    con_sent=self.sent_splitter(end)

                    into_sent=into_sent[:-1]
                    body_sent=body_sent[:-1]
                    con_sent=con_sent[:-1]

                    intro+=self.reconcatenate(into_sent)
                    body+=self.reconcatenate(body_sent)
                    con+=self.reconcatenate(con_sent)

                    if (len(intro.split())>=225) or (len(body.split())>=450)or(len(con.split())>=225):
                        iteration_flag=False

            except:
                continue

        intro=intro.replace('From active to passive.','')
        body=body.replace('From active to passive.','')
        con=con.replace('From active to passive.','')
        return query,intro,body,con


    def main_event(self):
        
            
            query_words=["nft","nft crypto","non fungible token","nft token","nfts crypto","nft news","most expensive nft","nft tips","new nft","nft for sale","nft websites","nft token list","nft crypto price","best nft crypto","top nft","buying nft","top nfts","best nfts","nft list","NFT collector","NFT Collection","NFT Artist","NFT Art","NFT community"]
            last_links={"nft":[],"nft crypto":[],"non fungible token":[],"nft token":[],"nfts crypto":[],"nft news":[],"most expensive nft":[],"nft tips":[],"new nft":[],"nft for sale":[],"nft websites":[],"nft token list":[],"nft crypto price":[],"best nft crypto":[],"top nft":[],"buying nft":[],"top nfts":[],"best nfts":[],"nft list":[],"NFT collector":[],"NFT Collection":[],"NFT Artist":[],"NFT Art":[],"NFT community":[]}
            
            while True:
                for word in query_words:
                    try:
                        last=[word]
                        query,intro,body,con=self.news_extraction(last,word)
                        total_article=intro+body+con
                        article=""
                        if(len(total_article.split())<300):
                            continue
                        if (intro!=""):           
                            head_block=self.tg.generate(intro+body+con)
                            article+=intro+"\n\n\n"
                            article+=self.tg.generate(body)+":\n"+body+"\n\n\n"
                            article+=self.tg.generate(con)+":\n"+con+"\n\n\n"
                            img_block=str(random.randint(0,384))+".jpg"
                            self.up=uploading.Upload()
                            self.up.login()
                            self.up.create_blog(head_block,article,img_block)                


                            if len(last)==10:
                                last.pop(0)
                            last.append(query)
                            print("Article is generated")
                    except Exception as e:
                        print(e)
                        continue    
                
                # script will rerun itself after evry 15 minutes
                print("___________________Waiting for next turn _______________________")
                time.sleep(15*60)  
        

if __name__ == '__main__':
    ag=ArtGen()
    ag.main_event()

