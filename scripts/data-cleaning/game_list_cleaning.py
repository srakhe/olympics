#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np


# In[4]:


class GamesListCleaning:
    def __init__(self,filePath,type_of_game):
        self.olympics_games=pd.read_csv(filePath)
        self.type_of_game=type_of_game
        self.pre_process_data()
        
    def pre_process_data(self):
        k=0
        start_date=[]
        end_date=[]
        start_month=[]
        for row in  self.olympics_games.iterrows():
            timeline=row[1][-1].split('–')
            if(len(timeline)>=2):
                start_date.append(timeline[0].strip())
                end_date.append(timeline[1].strip())
                start_month.append(timeline[1].split(' ')[-1].strip())
            elif (len(timeline)<2):
                start_date.append('NA')
                end_date.append('NA')
                start_month.append('NA')
            k=k+1  
        
        self.olympics_games['Type']=self.type_of_game
        self.olympics_games['start_date']=start_date
        self.olympics_games['end_date']=end_date
        self.olympics_games['start_month']=start_month
        self.post_process_data()
       
    
    def post_process_data(self):
            start_date=[]
            for row in self.olympics_games.iterrows():
                if( (len(row[1]['start_date'])<=2) and (row[1]['start_date']!='NA') ):
                    start_date.append(row[1]['start_date']+ ' ' + row[1]['start_month'])
                else:
                    start_date.append(row[1]['start_date'])
             
            self.olympics_games['start_date']=start_date
            self.olympics_games.drop(columns=['start_month'],inplace=True)
            
            self.save_to_csv()
      
    def save_to_csv(self):
        filename='cleaned_'+ self.type_of_game +'.csv'
    
    def get_olympic_dataframe(self):
        return self.olympics_games
        


# In[5]:


if __name__ == "__main__":
    summer_olympics = GamesListCleaning(filePath="../scrapers/olympic/data/games/summer.csv",type_of_game="Summer").get_olympic_dataframe()
    winter_olympics = GamesListCleaning(filePath="../scrapers/olympic/data/games/winter.csv",type_of_game="Winter").get_olympic_dataframe()
    games_list=pd.concat([summer_olympics,winter_olympics],ignore_index=True)
    games_list.to_csv('games.csv')

