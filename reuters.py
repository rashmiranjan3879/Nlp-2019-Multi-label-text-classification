# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd
from scrapy.exceptions import CloseSpider

class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    start_urls = ['https://in.reuters.com/assets/searchArticleLoadMoreJson?blob=volcano&bigOrSmall=big&articleWithBlog=true&sortBy=&dateRange=&numResultsToShow=10&pn=2&callback=addMoreNewsResults']
    curr_page=2
    count=0
    def parse(self,response):
        self.curr_page=self.curr_page+1
        data=response.text.split()
        newssites=[]
        for i in range (0,len(data)):
            if(data[i]=='href:'):
                newssites.append(data[i+1][1:-2])
        #print(newssites)
        for news in newssites:
            next_news='https://in.reuters.com/'+news
            yield scrapy.Request(next_news, callback=self.parsetext)

        next_page='https://in.reuters.com/assets/searchArticleLoadMoreJson?blob=volcano&bigOrSmall=big&articleWithBlog=true&sortBy=&dateRange=&numResultsToShow=10&pn='+str(self.curr_page)+'&callback=addMoreNewsResults'	
        yield scrapy.Request(next_page, callback=self.parse)
        	
    def parsetext(self, response):
        # if(self.validornot(response)==False):
        #     return
        # print(self.count)    
        self.count=self.count+1
        if(self.count>1000):
        	raise CloseSpider('1000 page limit reached')    
        page = response.url.split("/")[-1]
        filename = 'reutersvolcano-%s' % page
        with open(filename, 'w') as f:
            title=response.css('h1.ArticleHeader_headline::text').get()
            title=''.join(title)
            date=response.css('div.ArticleHeader_date::text').get()
            date=''.join(date)
            data=response.css('p::text').getall()
            data=' '.join(data)
            total_data=[title,date,data]
            total_data='\n'.join(total_data)
            f.write(total_data)
        self.log('Saved file %s' % filename)
        
