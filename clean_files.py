'''
In here were gonna define a set of functions that are going to able us to clean the excel files we need

'''

def trim_df(df):
    #We drop all the columns completely empty
    df.dropna(axis=1,how='all',inplace=True)
    
 
    #Add a column to get the count of non-na
    df['non_nans'] = df.count(axis=1)
    
    #Save the maximum non na
    maximum = df.non_nans.max()
    
    
    #Filtering rows with more than 4 non nas, we only get the relevant information

    df=df[df.non_nans>4]
    
    #Drop the column we calculated before
    df.drop(['non_nans'], inplace=True, axis=1)
    
    #Setting new name columns
    df.columns = df.iloc[0]
    
    #Reset index
    df.reset_index(drop=True,inplace=True)
    
    #Eliminate first column which is now the header
    df.drop([0], inplace=True)
    
    #Resetting the index again
    df.reset_index(drop=True,inplace=True)
    
    #Return the new dataframe
    return df, maximum

'''
To have a better manipulation of the data were gonna change its column types accorindgly to the data they contain. The
 function change_types will do the following:

1) Try to set the column type to float, and if it can not do it, it means that column contain a category variable
2)Set all column names to upper case
3) Normalise accents within the columns with text data
4)Replace the column name "Empresa" to "Operadora" in case it exists

'''

def change_types(trimmed_df):
    import numpy as np
    #Step 1)
    for col in trimmed_df.columns:
        
        trimmed_df.dropna(inplace=True)
        
        try:
            trimmed_df = trimmed_df.astype({col:'float64'})
        except ValueError:
            
            trimmed_df[col] = trimmed_df[col].str.upper()
            
            continue
    #Step #2
    trimmed_df.columns = [x.upper() for x in trimmed_df.columns]
    #Step #3
    cols = trimmed_df.select_dtypes(include=[np.object]).columns
    trimmed_df[cols] = trimmed_df[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))
    #Step #4
    if 'EMPRESA' in list(trimmed_df.columns):
        trimmed_df.rename(columns={'EMPRESA': 'OPERADORA'}, inplace=True)

    return trimmed_df

'''
The following function will accept a dataframe and convert it from wide to a long format
sdcf DFSVrw 
'''
def long_df(trimmed_df,year):
    import pandas as pd
    #First we separate the text and numeric data
    
    num_cols=trimmed_df.select_dtypes(include=['float64']).columns
    string_cols = trimmed_df.select_dtypes(include=['object']).columns
    
    #Generate the list of dates to have
    i=0
    fechas=list(pd.date_range(start=fr'01/01/{year}', periods=len(num_cols), 
                              freq='M').strftime('%m/%d/%Y'))
    #Renombramos los meses por la fecha correspondiente de fin de mes
    for col in num_cols:
        trimmed_df.rename(columns={col: f"{fechas[i]}"},inplace=True)
        i=i+1
        
    #We use pd.melt to get the long format of the data
    molten_df = pd.melt(trimmed_df, id_vars=string_cols,
                        var_name='Fecha',value_name="Produccion")
    molten_df.dropna(inplace=True)
    
    return molten_df