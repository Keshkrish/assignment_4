import pandas as pd
import os
import re
import numpy as np
'''
    Helper function to convert the dtype of all the required columns to float
'''
def extract_and_convert_to_float(value):
    numeric_part = re.search(r'[\d.]+', str(value)) #This step searches for a continuous sequence of digits and '.' which is then converted to float
    #The above step is needed because some of the measurements are followed by units or other letters. For eg: 72s etc.
    if numeric_part:
        return float(numeric_part.group()) #returns the numeric part
    else:
        return None #If there is no numeric part, it returns None
all_fields=['MonthlyAverageRH','MonthlySeaLevelPressure','MonthlyStationPressure','MonthlyDewpointTemperature','MonthlyMeanTemperature','AWND'] #These are the only fields which are averages of their daily fields counterparts.

#In the next step we check if there are 12 non zero entries for each field, corresponding to 12 months. We discard the fields which do not have 12 non null entries.
selected_fields=set(all_fields)#The fields that dont have 12 non null entries are removed from this set
final_df=pd.DataFrame() #Dataframe which stores the extracted monthly averages
#print(selected_fields)
for file in sorted(os.listdir('Data')):
    if not file.startswith('.'):
        df=pd.read_csv(os.path.join('Data',file))
        for field in all_fields:
            if df[field].count()!=12:
                selected_fields.discard(field)
selected_fields=list(selected_fields)
for file in sorted(os.listdir('Data')):
    
    if not file.startswith('.'): #To ignore files which are not the data files
        
        df=pd.read_csv(os.path.join('Data',file))
        for field in selected_fields:
            df[field]=df[field].apply(extract_and_convert_to_float)# Convert the dtype of required field to float
                
        df=df[['DATE','STATION']+selected_fields]
        df.dropna(inplace=True) #drop rows which do not contain the monthly aggregate info
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['month'] = df['DATE'].dt.month #create a column called month.
        df['index'] = list(zip(df['month'], df['STATION'])) #The tuple (month,STATION) is used as a key to map the average calculated from daily data and average aggregated from monthly data when computing r2 score
        df.set_index(['index'], inplace=True)
        df.drop(columns=['DATE','month','STATION'], inplace=True) 
        #print(df)
        final_df=pd.concat([final_df,df],ignore_index=False)

final_df.to_csv('extracted_monthly_averages.csv',index=True)
selected_fields=np.array(selected_fields,dtype=object) #converting to np array to save
np.save('list_of_fields.npy',selected_fields)
