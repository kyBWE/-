
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import random

for page in range(1,56):
    print('page:',format(page))
    offset=(page-1)*20
    url = 'https://hurun.net/zh-CN/Rank/HsRankDetailsList?num=ODBYW2BI&search=&offset={}&limit=20'.format(offset)
    headers={
        'referer':'https://hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich',
        'accept':'application/json, text/javascript, */*; q=0.01',
        'accept-encoding':'gzip, deflate, br, zstd',
        'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type':'application/json',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
        }
    time.sleep(random.uniform(1,3))
    r=requests.get(url=url,headers=headers)
    json_data=r.json()
    
    Rank=[]  #排名
    FullName_CN=[]  #中文姓名
    FullName_EN=[]  #英文姓名
    Wealth=[]  #财富值
    Sex=[]  #性别
    Age=[]  #年龄
    BirthPlace=[]  #出生地
    Birthday=[]  #生日
    Education=[]  #学历
    
    ComName_CN=[]  #公司中文名称
    ComName_EN=[]  #公司英文名称
    ComPlace=[]  #公司所在地
    ComIndustry=[]  #行业

    item_list=json_data['rows']
    for item in item_list:
        Rank.append(item['hs_Rank_Rich_Ranking'])
        FullName_CN.append(item['hs_Character'][0]['hs_Character_Fullname_Cn'])
        FullName_EN.append(item['hs_Character'][0]['hs_Character_Fullname_En'])        
        Wealth.append(item['hs_Rank_Rich_Wealth'])
        Sex.append(item['hs_Character'][0]['hs_Character_Gender'])
        Age.append(item['hs_Character'][0]['hs_Character_Age'])
        BirthPlace.append(item['hs_Character'][0]['hs_Character_BirthPlace_Cn'])
        Birthday.append(item['hs_Character'][0]['hs_Character_Birthday'])
        Education.append(item['hs_Character'][0]['hs_Character_Education_Cn'])
        ComName_CN.append(item['hs_Rank_Rich_ComName_Cn'])
        ComName_EN.append(item['hs_Rank_Rich_ComName_En'])
        ComPlace.append(item['hs_Rank_Rich_ComHeadquarters_Cn'])
        ComIndustry.append(item['hs_Rank_Rich_Industry_Cn'])
        
    df=pd.DataFrame(
    {
        '排名':Rank,
        '姓名（中文）':FullName_CN,
        '姓名（英文）':FullName_EN,       
        '财富值':[f"{w}亿" for w in Wealth],
        '性别':['男' if s=='先生' else '女' for s in Sex],
        '年龄':Age,
        '出生地':BirthPlace,
        '生日':Birthday,
        '学历':Education,
        '企业名称（中文）':ComName_CN,
        '企业名称（英文）':ComName_EN,
        '企业所在地':ComPlace,
        '行业':ComIndustry
        }
    )
    if page==1:
        header=True
    else:
        header=False
    df.to_csv('2024胡润百富榜.csv',mode='a+',index=False,header=header,encoding='utf_8_sig')