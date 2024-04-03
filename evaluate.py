import pandas as pd
from sklearn.metrics import r2_score

computed_averages=pd.read_csv('computed_monthly_averages.csv',index_col=0) #Read the output of process
extracted_averages=pd.read_csv('extracted_monthly_averages.csv',index_col=0) #Read the output of prepare


computed_averages=computed_averages.sort_index() #Sorting is done to ensure that each row in computed_averages and extracted_averages correspond to the same month and location
extracted_averages=extracted_averages.sort_index()

computed_averages_values=computed_averages.iloc[:,:].values.flatten() #extract the values and flatten, to compute a single r2 score
extracted_averages_values=extracted_averages.iloc[:,:].values.flatten()

#print(computed_averages_values)
#print(extracted_averages_values)
r2=r2_score(computed_averages_values,extracted_averages_values) #Compute r2 score

print('R2 Score is:'+str(r2))
if r2>0.9:
    print('Consistent (C)')
