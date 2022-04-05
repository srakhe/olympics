#!/usr/bin/env python
# coding: utf-8

# In[28]:


from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


# In[43]:


class OlympicsDateScrapper:
    
    def __init__(self, url):
        self.title="Olympic_Games_Date"
        self.fetch_data(url)
    
    def fetch_data(self,url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        self.save_data(webpage)
    
    def save_data(self,webpage):
        filename=self.title+'.html'
        with open(filename, 'wb') as file:
            file.write(webpage)
        self.generate_column_headers_and_create_dataframe();
    
    def generate_column_headers_and_create_dataframe(self):
        filename=self.title+'.html'
        file = open(filename)
        soup = BeautifulSoup(file.read())
        olympic_date_table= soup.findAll("table",{"class": "wikitable"})
        column_headers=[]
        self.olympic_date_table_columns=olympic_date_table[0].findAll("tr")
        olympic_table_column_headers=self.olympic_date_table_columns[0]
        for row in olympic_table_column_headers:
            column_headers.append(row.text.strip())
        
        column_headers=[column for column in column_headers if len(column) >1]
        start_columns=column_headers[0:3]
        end_columns=column_headers[6:8]
        column_headers=start_columns+ end_columns
        
        self.olympic_date_table = pd.DataFrame(columns=column_headers)  
        self.scrape()
    
       
        
    def scrape(self):
        k=0
        for row in self.olympic_date_table_columns[1:]:
            individual_row_data = row.find_all("td")
            field_value= [field.text.split('\n')[0] for field in individual_row_data] 
            field_value=field_value[1:]
            start_column_values=field_value[0:3]
            end_column_values=field_value[-3:][0:2]
            row_values=[]
            row_values=start_column_values + end_column_values
            if(len(row_values)!=5):
                continue
            self.olympic_date_table.loc[k]=row_values
            k=k+1
        
                
        self.data_cleaning()
        
    def data_cleaning(self):
        self.olympic_date_table['City']=[city[0] for city in self.olympic_date_table['City'].str.split('[')]
        self.olympic_date_table['Opening ceremony']=[city[0] for city in self.olympic_date_table['Opening ceremony'].str.split('[')]
        self.olympic_date_table['Closing ceremony']=[city[0] for city in self.olympic_date_table['Closing ceremony'].str.split('[')]
        self.olympic_date_table=self.olympic_date_table[self.olympic_date_table['City']!="MelbourneStockholm"]
        self.olympic_date_table = self.olympic_date_table[self.olympic_date_table['City']!="TokyoHelsinki"] 
        self.olympic_date_table = self.olympic_date_table[self.olympic_date_table['City']!="London"]
        self.olympic_date_table = self.olympic_date_table[self.olympic_date_table['City']!="SapporoGarmisch-Partenkirchen"]
        self.olympic_date_table['Opening ceremony'].replace('', np.nan, inplace=True)
        self.olympic_date_table['Closing ceremony'].replace('', np.nan, inplace=True)
        self.olympic_date_table.dropna(subset=['Opening ceremony','Closing ceremony'], inplace=True)
        self.olympic_date_table['City']=[city+' Olympics' for city in self.olympic_date_table['City']]
        
        print(self.olympic_date_table)    

        
        self.save_dataframe_to_csv()
        
    def save_dataframe_to_csv(self):
        filename=self.title+'.csv'
        self.olympic_date_table.to_csv(filename)
     
    def get_Olympic_Date_DataFrame(self):
        return self.olympic_date_table
        


# In[44]:


if __name__ == "__main__":
    oly_date_scr = OlympicsDateScrapper(url="https://en.wikipedia.org/wiki/List_of_Olympic_Games_host_cities")

