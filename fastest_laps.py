# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:59:56 2020

@author: Lenovo
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

    fw=open('fastest_laps_table.txt','w',encoding='utf8') # output file
    winner_file = open('winner_table.txt','w',encoding='utf8')

    writer=csv.writer(fw,lineterminator='\n')   
    Dhl_winner_writer=csv.writer(winner_file,lineterminator='\n')   

                                 #create a csv writer for this file
    fastest_laps_link = url + '/' + str(year) + '/fastest-laps.html'

    for i in range(5): # try 5 times

            #send a request to access the url
        response=requests.get(fastest_laps_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        
        if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
            break # we got the file, break the loop
        else:
            time.sleep(2) # wait 2 secs
             
    html=response.text   # read in the text from the file
        
    soup = BeautifulSoup(html,features ='html5lib') # parse the html 
        
    table = soup.find('table',{'class':'resultsarchive-table'} )
    body = table.find('tbody')
    table_rows = body.find_all('tr')
     
    # DHL FASTEST LAPS ARE BEING RECORDED SINCE 2007
    
    for tr in table_rows:

        grand_prix , driver , constructor_name , lap_time = 'NA', 'NA', 'NA', 'NA'
        
        grand_prix_chunk = tr.find('td',{'class':'width30 dark'})
        grand_prix = grand_prix_chunk.text.strip()
          
        driver_chunk = tr.find('td',{'class':'width25'})
        driver = driver_chunk.find('span',{'class':'hide-for-mobile'})
        driver_name = driver.text.strip()
 
        constructor_chunk = tr.find('td',{'class':'width25 semi-bold uppercase'})
        constructor_name = constructor_chunk.text.strip()
            
        lap_time_chunk = tr.find('td',{'class':'dark bold'})
        lap_time = lap_time_chunk.text.strip()
            
        writer.writerow([grand_prix , driver_name , constructor_name , lap_time]) # write to file 
        
        
    fastest_lap_chunk = soup.find('div', {'class':'resultsarchive-dhl-winner group'})

    fast_list = fastest_lap_chunk.text.strip().split()
    
    winner_name = fast_list[1] + " " + fast_list[2]
    winner_team = fast_list[3].replace('(',"").replace(')',"")
    fastest = fast_list[4]
    
    Dhl_winner_writer.writerow([winner_name, winner_team, fastest])
    
    winner_file.close()
    fw.close()

run(2019)

fastest_lap_winner_2019 = pd.read_csv('winner_table.txt', names = ['DHL_Winner','CONSTRUCTOR','FASTEST_LAPS'], sep = ',')
fastest_lap_winner_2019.to_csv (r'C:\Users\Lenovo\Desktop\\F1_2019\fastest_lap_2019_winner.csv', index = False, header=True)

