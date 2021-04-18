
def check(entry, engine ):
    
    import sqlalchemy
    import pandas as pd

    #First we query which links we have already processed into our database
    query = '''SELECT * 
                FROM scraped_data '''
    #We store the data in past_results

    past_results = pd.read_sql(sql=query,con= engine)
    #After that we merge the tables to detect new ones
    merged_results = pd.merge(entry, past_results, how='left', on=['Full_link'])
    
    #We finally return the dataframe where we dont find a match after the merge
    merged_results = merged_results[merged_results['years_y'].isna()]

    return merged_results.rename(columns={'years_x':'years'})[['Full_link','years']]

