from bs4 import BeautifulSoup
import json
import time
import boto3
import asyncio
from requests_html import AsyncHTMLSession


my_stocks={'GC=F':'Gold','BTC-USD':'Bitcoin USD'}#,'CL=F':'Crude Oil','TSLA':'Tesla','AMZN':'Amazon'}

stocks_urls=[]

#stock_data=[]

#Scraping the data from Yahoo finance using Beautiful Soup and asyncio to speed up the process

async def GetData(s,stock_url):
    summary={}
    #To combine all data for stock:
    full_info={}

    base_url=f'https://finance.yahoo.com/quote/{stock_url}'
    res= await s.get(base_url)
    soup=BeautifulSoup(res.text,'lxml')
    percent_change=soup.find_all('fin-streamer',class_='Fw(500) Pstart(8px) Fz(24px)')

    names=soup.find_all(['div','table','td','span'],class_='C($primaryColor) W(51%)')
    nums=soup.find_all(['div','table','td'],class_="Ta(end) Fw(600) Lh(14px)")
    
    for item,num in zip(names,nums):
    
        summary[item.get_text()]=num.get_text()
    #print(summary)
    stock={
        'name':my_stocks[stock_url],
        'price':soup.find('fin-streamer',class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text,
        'change':soup.find('fin-streamer',class_='Fw(500) Pstart(8px) Fz(24px)').text,
        'percent_change':percent_change[1].text
    }
    full_info={**stock,**summary}
    #print(stock,summary)
    #print(full_info)
    return full_info


#Getting data for all the stocks then gathering it in results

async def stocks_data(my_stocks):

    s=AsyncHTMLSession()
    tasks=(GetData(s,stock_url) for stock_url in my_stocks)
    return await asyncio.gather(*tasks)


#results=asyncio.run(stocks_data(my_stocks))
#print(results)

#Converting the json into the suitable format for ingestion by Kinesis Data Streams

def records_prep(results):
    
    blobs_list=[]
    for list_info in results:

        items_dict={'Data':json.dumps(list_info).encode('utf-8'),'PartitionKey': '1'}
        blobs_list.append(items_dict)

    return blobs_list

print('working')
if __name__ == '__main__' :
    while True:
        try:
            results=asyncio.run(stocks_data(my_stocks))
            results_blob=records_prep(results)
            print(results_blob)
            print('\n')
            time.sleep(30)
        except:
            print('Error')
    #Putting the data in Kinesis for ingestion

#        client = boto3.client('kinesis',region_name='us-east-1')
#
#        response = client.put_records(
#            Records=results_blob  ,
#            StreamName='yahoofinanceDS',
#            StreamARN='arn:aws:kinesis:us-east-1:254244063442:stream/yahoofinanceDS'
#        )