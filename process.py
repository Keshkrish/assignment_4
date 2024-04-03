import pandas as pd
import os
import re
import numpy as np
'''
    Helper function to convert the dtype of all the required columns to float
'''
def extract_and_convert_to_float(value):
    numeric_part = re.search(r'[\d.]+', str(value))#This step searches for a continuous sequence of digits and '.' which is then converted to float
    #The above step is needed because some of the measurements are followed by units or other letters. For eg: 72s etc.
    if numeric_part:
        return float(numeric_part.group())#returns the numeric part
    else:
        return None#If there is no numeric part, it returns None

final_df=pd.DataFrame() #Dataframe that stores the computed monthly averages
list_of_fields=list(np.load('list_of_fields.npy',allow_pickle=True))#The list of fields obtained from prepare step
map_fields={'MonthlyAverageRH':'DailyAverageRelativeHumidity','MonthlySeaLevelPressure':'DailyAverageSeaLevelPressure','MonthlyStationPressure':'DailyAverageStationPressure','MonthlyDewpointTemperature':'DailyAverageDewPointTemperature','MonthlyMeanTemperature':'DailyAverageDryBulbTemperature'}
#Above is a dictionary which maps the monthly aggregate fields to its corresponding daily fields

selected_fields=[]

for field in list_of_fields:
    selected_fields.append(map_fields[field])#Stores the coresponding daily fields for the list of fields obtained from prepare step


for file in sorted(os.listdir('Data')):
    if not file.startswith('.'):#To ignore files which are not the data files
        df=pd.read_csv(os.path.join('Data',file))
        df['DATE']=pd.to_datetime(df['DATE'])
        for field in selected_fields:
            df[field]=df[field].apply(extract_and_convert_to_float)#Convert the dtype of required field to float
        df['index']=list(zip(df['DATE'].dt.month,df['STATION']))
        monthly_avg = df.groupby(df['index'])[selected_fields].mean()#Agrregate by (month,location) and calculate averages
        #print(monthly_avg)
        final_df=pd.concat([final_df,monthly_avg],ignore_index=False)
        
#final_df['index'] = list(zip(final_df['DATE'], final_df['STATION']))
#final_df.drop(columns=['DATE','STATION'],inplace=True)
df.set_index(['index'], inplace=True)
#print(final_df)
final_df.to_csv('computed_monthly_averages.csv',index=True)#save the calculated averages
