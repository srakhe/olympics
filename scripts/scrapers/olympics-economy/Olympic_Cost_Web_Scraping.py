from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup

class CostOfOlympicScraper:
    
    def __init__(self, url):
        self.title="data/Cost_of_the_Olympic_Games"
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
        olympic_medal_table= soup.findAll("table",{"class": "igsv-table no-datatables"})
        olympic_medal_table[1]
        column_headers=[]
        self.olympic_cost_table_columns=olympic_medal_table[1].findAll("tr")
        olympic_table_column_headers=self.olympic_cost_table_columns[1]
        for row in olympic_table_column_headers:
            column_headers.append(row.text)
    
        #Create extra columns which needs to be extracted from web scraping
        column_headers.append('Year')  
        column_headers.append('Type')
        column_headers.append('City')
        column_headers.append('Country')
     
        self.olympic_table = pd.DataFrame(columns=column_headers)  
        self.scrape()
        
    def scrape(self):
        olympic_cost_table_column_demo=self.olympic_cost_table_columns[2:]
        k=0
        for row in olympic_cost_table_column_demo:
            individual_row_data = row.find_all("td")
            field_value= [field.text.split('\n')[0] for field in individual_row_data]   
            
            #Assigning NA values .TO be filled by feature extraction
            field_value.append('NA')
            field_value.append('NA')
            field_value.append('NA')
            field_value.append('NA')
            self.olympic_table.loc[k]=field_value
            k=k+1
            
        self.extract_features()
        
    def extract_features(self):
        k=0       
        for row in self.olympic_table.iterrows():
            olympic_info=row[1][0].split(',')

            # Handling edge cases
            if(len(olympic_info)<3):
                self.olympic_table['Country'].loc[k]=olympic_info[1]
                self.olympic_table['City'].loc[k]=olympic_info[0].split(' ')[3]
                self.olympic_table['Year'].loc[k]=olympic_info[0].split(' ')[0]
                self.olympic_table['Type'].loc[k]=olympic_info[0].split(' ')[1]
            else:    
                self.olympic_table['City'].loc[k]=olympic_info[1]
                self.olympic_table['Country'].loc[k]=olympic_info[2]
                olympic_year_and_type=olympic_info[0]
                olympic_year_and_type=olympic_year_and_type.split(' ')
                self.olympic_table['Year'].loc[k]=olympic_year_and_type[0]
                self.olympic_table['Type'].loc[k]=olympic_year_and_type[1]
            k=k+1
        
        self.save_dataframe_to_csv()
        
    def save_dataframe_to_csv(self):
        filename=self.title+ '.csv'
        self.olympic_table.to_csv(filename)
    

if __name__ == "__main__":
    cost_of_oly_scr = CostOfOlympicScraper(url="https://moneynation.com/olympics-money-facts/")

