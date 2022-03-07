#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib.request
import pandas as pd
page_url = "https://en.wikipedia.org/wiki/Cost_of_the_Olympic_Games"
urllib.request.urlretrieve(page_url, "Cost_of_the_Olympic_Games.html")


# In[2]:


from bs4 import BeautifulSoup
page = open("Cost_of_the_Olympic_Games.html")
soup = BeautifulSoup(page.read())


# In[4]:


olympic_cost_table= soup.findAll("table",{"class": "wikitable"})
olympic_cost_table_columns=olympic_cost_table[0].findAll("th")
olympic_cost_table_columns
column_headers=[]
for col in olympic_cost_table_columns:
    column_headers.append(col.text.split('\n')[0])

olympic_table = pd.DataFrame(columns=column_headers)


# In[5]:


olympic_cost_table_values=olympic_cost_table[0].findAll("tr")
k=0
for row in olympic_cost_table_values[1:]:
    individual_row_data = row.find_all("td")
    field_value= [field.text.split('\n')[0] for field in individual_row_data]   
    olympic_table.loc[k]=field_value
    k=k+1


# In[6]:


olympic_table


# In[9]:


olympic_table.to_csv("Cost_of_Olympic_Games.csv")

