import requests
from bs4 import BeautifulSoup
import random
import sys
import json
import pandas as pd 
import openpyxl
import re
import time
import threading
import bs4
import sys
import easygui as g

UserAgents = [ 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7", 
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10", 
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)", 
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)", 
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre", 
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0", 
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
]
#
headers = {
        'user-agent':random.choice(UserAgents),
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests':'1'
    }

#得到汽车之家所有的品牌
def getAllcarbrand():
    brand = []   # {'??': 'https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-0-3-0-0-0-0-0-0-1.html', ...}
    url = 'https://car.autohome.com.cn/#pvareaid=3311273'#初始页面
    
    
    response = requests.get(url,headers=headers)#通过get请求得到网页数据内容
    response.encoding = "gbk"#转码，不然会乱码
    soup = BeautifulSoup(response.text,'lxml')
    content = 'ABCDFGHIJKLMNOPQRSTWXYZ'#23个拼音首写字母品牌
    for i in range(23):
        letter_list = soup.find(attrs={'id':'brand'+content[i]}).find_all('a')#逐渐定位到这个地方，找出所有的超链接
        for a in letter_list:
            #print(a)
            if(a['href']!='#!'):
                brand.append(a['href'])#把内容保存下来
    return brand

#得到一个品牌所有车的名字、指导价
def getOnebrandcarprice(url,name,price):
    #url = 'https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-0-15-0-0-0-0-0-0-1.html'
    
    response = requests.get(url,headers=headers)
    response.encoding = "gbk"
    soup = BeautifulSoup(response.text,'lxml')
    main_title = soup.find(attrs={'id':'brandtab-1'}).find_all(attrs={'class':'main-title'})
    lever_price = soup.find(attrs={'id':'brandtab-1'}).find_all(attrs={'class':'main-lever'})
    for i in main_title:
        for j in i.find_all(attrs={'class':'font-bold'}):
            name.append(j.string)
    for i in lever_price:
        for j in i.find_all(attrs={'class':'font-arial'}):
            price.append(j.string)
    
    return name,price

def getOne(url,level,score):
    #url = 'https://car.autohome.com.cn/price/list-0-0-0-0-0-0-0-0-120-0-0-0-0-0-0-1.html'
    #score1 = []
    #level = []
    response = requests.get(url,headers=headers)
    response.encoding = "gbk"
    soup = BeautifulSoup(response.text,'lxml')
    car_level = soup.find(attrs={'id':'brandtab-1'}).find_all(attrs={'class':'lever-ul'})
    for i in car_level:
        for j in i.find_all(attrs={'class':'info-gray'}):
                level.append(j.string)
                break
    car_score = soup.find(attrs={'id':'brandtab-1'}).find_all(attrs={'class':'score-cont'})
    for i in car_score:
        for j in i.find_all('span'):
            if isinstance(j.string,bs4.element.NavigableString):
                score.append(j.string)      
    return level,score
        
        

def getAllcarprice():
    name = []
    price = []
    level = []
    score = []
    brands=getAllcarbrand()
    for i in brands:
        url = 'https://car.autohome.com.cn'+i
        name,price = getOnebrandcarprice(url,name,price)
        level,score = getOne(url,level,score)
##下面的pd都是为了把数据合并，更好的导出
    one = pd.DataFrame(level,name,columns=['结构'])
    two = pd.DataFrame(score,name,columns=['评分（满分：5）'])
    three = pd.DataFrame(price,name,columns=['指导价'])
    all = pd.concat([one,two,three],axis=1)
    all.to_excel("D:\\pacar.xlsx",sheet_name="sheet1")#把处理后的数据保存到excel

##简单的gui见面
def gui():
    if g.ccbox("亲，你要不要爬取汽车之家呢",title="汽车之家",choices=("要","不要")):
        g.msgbox("亲，请等待大概两分钟！！！,点击ok后开始爬取",title="汽车之家")
        getAllcarprice()
        g.msgbox("爬取完毕，请去本地D盘找到pacar.xlsx打开,查看数据",title="汽车之家")
    else:
        sys.exit(0)


if __name__ == "__main__":
    
    gui()
    