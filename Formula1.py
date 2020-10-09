# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 12:56:11 2020

@author: Ashutosh Shinde
"""

# Formula 1 Web Scraping

from bs4 import BeautifulSoup
import re
import time
import requests
import csv
import pandas as pd

def run(year):
    
    url = 'https://www.formula1.com/en/results.html'

    fw=open('f11_table.txt','w',encoding='utf8') # output file

    writer=csv.writer(fw,lineterminator='\n')                                    #create a csv writer for this file
    
    races_result_link = url + '/' + str(year) + '/races.html'

    #print(races_result_link)

    for i in range(5): # try 5 times

            #send a request to access the url
        response=requests.get(races_result_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        
        if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
            break # we got the file, break the loop
        else:time.sleep(2) # wait 2 secs
             
    html=response.text# read in the text from the file
        
    soup = BeautifulSoup(html,features ='html5lib') # parse the html 
        
    table = soup.find('table',{'class':'resultsarchive-table'} )
    body = table.find('tbody')
    table_rows = body.find_all('tr')
 
    for tr in table_rows:

        grand_prix , date , winner , constructor , laps = 'NA', 'NA', 'NA', 'NA', 'NA'
            
        grand_prix_chunk=tr.find('a',{'href':re.compile('/en/results.html/'+ str(year) + '/races')})
        grand_prix = grand_prix_chunk.text.strip()
            
       
        date_chunk = tr.find('td',{'class':'dark hide-for-mobile'})
        date = date_chunk.text.strip()
        
        winner_chunk = tr.find('span',{'class':'hide-for-mobile'})
        winner = winner_chunk.text.strip()
            
        constructor_chunk = tr.find('td',{'class':'semi-bold uppercase'})
        constructor = constructor_chunk.text
            
        laps_chunk = tr.find('td',{'class':'bold hide-for-mobile'})
        laps = laps_chunk.text.strip()
            
        writer.writerow([grand_prix , date , winner , constructor , laps]) # write to file 
     

            
    fw.close()

run(2019)

races_2019 = pd.read_csv('f11_table.txt', names = ['GRAND PRIX','GP_DATE','WINNER','CONSTRUCTOR','LAPS'], sep = ',')
print(races_2019)
races_2019.to_csv (r'C:\Users\Lenovo\Desktop\races_2019.csv', index = False, header=True)


