# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 19:28:28 2021

@author: tauhid
"""

from bs4 import BeautifulSoup 
import requests
import pandas as pd
import numpy as np
import random
import time

headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
          'Accept': '*/*','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8','Connection': 'keep-alive',
          'Content-Length':'34','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Host': 'main.sci.gov.in','Referer': 'https://main.sci.gov.in/case-status'}

act=[]
diaryno=[]
caseno=[]
listedon=[]
status=[]
disp=[]
category=[]
petitioner=[]
respondent=[]
petadvocate=[]
resadvocate=[]
usection=[]


def get_data():   
    start_yr,end_yr=2001,2021
    s=requests.session()
    starttime=time.time()
    print(time.ctime())
    for year in range(start_yr,end_yr+1):
      payload={}
      payload['d_yr']=year
      for i in range(1,100+1):
        payload['d_no']=i
        payload['ansCaptcha']=random.randint(1111,9999)
        try:
          response=s.post('https://main.sci.gov.in/php/case_status/case_status_process.php',data=payload,headers=headers)
          soup=BeautifulSoup(response.text,'html.parser')
        except:
            print('Request Timeout Requesting Again')
            continue
        tab = soup.find('div' , class_='panel-collapse collapse in')
        if tab is None:
          tabdata=soup.find_all('td')
        else:
          tabdata=tab.find_all('td')
        tabledata=[]
        for td in tabdata:
          tabledata.append(td.text.strip())
        for i in range(0,len(tabledata),2):
          info=tabledata[i]
          if ('Act' in info):
            if tabledata[i+1] == '':
              act.append(np.nan)
            else:
              act.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Case No' in info):
            if tabledata[i+1] == '':
              caseno.append(np.nan)
            else:
              caseno.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Category' in info):
            if tabledata[i+1] == '':
              category.append(np.nan)
            else:
              category.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Diary' in info):
            if tabledata[i+1] == '':
              diaryno.append(np.nan)
            else:
              diaryno.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Pet.' in info):
            if tabledata[i+1] == '':
              petadvocate.append(np.nan)
            else:
              petadvocate.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Petitioner' in info):
            if tabledata[i+1] == '':
              petitioner.append(np.nan)
            else:
              petitioner.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Present' in info):
            if tabledata[i+1] == '':
              listedon.append(np.nan)
            else:
              listedon.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Resp.' in info):
            if tabledata[i+1] == '':
              resadvocate.append(np.nan)
            else:
              resadvocate.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Respondent' in info):
            if tabledata[i+1] == '':
              respondent.append(np.nan)
            else:
              respondent.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Status/Stage' in info):
            if tabledata[i+1] == '':
              status.append(np.nan)
            else:
              status.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('Disp.' in info):
            if tabledata[i+1] == '':
              disp.append(np.nan)
            else:
              disp.append(tabledata[i+1].replace('\xa0','').strip())
          elif ('U/Section' in info):
            if tabledata[i+1] == '':
              usection.append(np.nan)
            else:usection.append(tabledata[i+1].replace('\xa0','').strip())
      print(f"Fetching done of year {payload['d_yr']}")    
      payload['d_yr']=payload['d_yr']+1
    print('Time required for execution:',time.time()-starttime)


def create_csv(filename='Test'):
    df = {'Diary No':diaryno,'Case No':caseno,'Present/Last Listed On':listedon,
          'Status/Stage':status,'Disp.Type':disp,'Category':category,'Act':act,
          'Petitioner(s)':petitioner,'Respondent(s)':respondent,
          'Pet. Advocate(s)':petadvocate,'Resp. Advocate(s)':resadvocate,'U/Section':usection}
    dataset = pd.DataFrame.from_dict(data = df,orient='index')
    dataset=dataset.transpose()
    dataset.to_csv(filename +'.csv', index=False, encoding='utf-8')
    print(f"CSV file created named {filename}.csv")
get_data()
create_csv('test1')
