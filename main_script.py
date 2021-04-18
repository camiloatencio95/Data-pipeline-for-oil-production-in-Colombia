from get_files import create_df
from check_db import check
import sqlalchemy
import clean_files
import sys
import pandas as pd

#First we start by checking what excel files do we get
excel_files = create_df()

#Second we create an engine to compare our obtanied 'excel files' to the ones already written into the dataframe

motor =sqlalchemy.create_engine('mysql+pymysql://root:camilo@localhost:3306/oil_analysis')

#We obtain a data frame with only excel files that have not yet been written into our database

new_excel_files=check(entry=excel_files , engine =motor)

#If there are not new files we can terminate our script here 
#if len(new_excel_files) == 0:
    #sys.exit()

#Other wise we continue
#We create a dictionary in which we will keep the new dataframes.



dataframes={}

for i in new_excel_files.index:
    df = pd.read_excel(new_excel_files.at[i,'Full_link'])
    df = clean_files.trim_df(df)[0]
    df= clean_files.change_types(df)
    df=  clean_files.long_df(df, new_excel_files.at[i,'years'])
    dataframes[str(new_excel_files.at[i,'years'])]=df

#Finally we concatenate all the dataframes 
try:
    final_df=pd.concat(dataframes.values(), ignore_index=True)
except ValueError:
    final_df=pd.DataFrame()

del final_df['CUENCA']

#We rename the new columns of the dataframe so that it matches the columns in the table

final_df.rename(columns={"OPERADORA":"COMPANY",\
                            "Fecha":"DDATE",\
                            "Produccion":"PDOIL" }, inplace= True)   

final_df.to_sql(name = "oil_production", con =motor, if_exists="append", method = "multi", schema = 'oil_analysis', index=False,chunksize=500)
#final_df.to_excel('mdna.xlsx')
print(1)
new_excel_files.to_sql(name='scraped_data', con=motor, if_exists="append",index= False, method = "multi",schema = 'oil_analysis')