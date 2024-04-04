import os
import yaml
import subprocess
import random
from bs4 import BeautifulSoup
import pandas as pd
cwd=os.getcwd()#Get the current working directory

'''
    Function to read a yaml file
'''
def read_yaml(file_path):
    with open(file_path,'r') as yaml_file:
        try:
            parameters=yaml.safe_load(yaml_file)
            return parameters
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")


'''
    Function to select a a given number of files from a given year
'''
def select_files(year, num_files):
    
    with open(year,'r') as page: #read the fetched html page as a string
        text=page.read()
    soup = BeautifulSoup(text, 'html.parser')
    all_csv = [link.get('href') for link in soup.find_all('a', href=True) if link['href'].endswith('.csv')] #use BeautifulSoup to obtain a list of the names of all the csv files in the page
    page.close()
    sampled_csv=[]
    all_csv=all_csv[::-1] #reversing the list because it was observed that files towards the end had less null values for monthly fields
    for csv in all_csv:
        url=base_url+year+'/'+csv
        df=pd.read_csv(url)
        if df['MonthlyMeanTemperature'].count()==12: #If we do random sampling, more often we get files which has null values for all monthly fields. This requirement ensures that we have atleast one monthly field without null values to work with 
            sampled_csv.append(csv)
        if len(sampled_csv)==num_files:
            break
    if len(sampled_csv)==0: #if no files satisfy the requirement
        print('No csv files has monthly aggregates!!!')
    else:
        if len(sampled_csv)<num_files: #if the files satisfying the requirement is less than the required number of files
            print('csv files with monthly aggregates is less than the required number of files. The program will continue to run with the available number of files.')
    
        with open('selected_random_files','w') as file: #Store the selected file links in a text file so that the csv files can be fetched using wget
            for csv in sampled_csv:
                file.write(base_url+year+'/'+csv+'\n')
        file.close()

params=read_yaml('params.yaml') #read parameters
year,n_locs=str(params['year']),int(params['n_locs'])
base_url='https://www.ncei.noaa.gov/data/local-climatological-data/access/'

subprocess.run(['wget',base_url+year,'-O',year]) #fetch the page
select_files(year,n_locs) #select files
if os.path.exists('Data'): #delete any previous data if exists
    for file in os.listdir('Data'):
        os.remove(os.path.join('Data',file))

subprocess.run(['wget','--input-file=selected_random_files','-P','Data']) #fetch the selected data
os.remove('selected_random_files') #remove unwanted files
os.remove(year)
