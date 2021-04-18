
'''
What we want to do with this next step is to tell the program to go to the url cited before,
and find all the HTML tags with the shape <a>, which contain the links that will point to the excel files in which the information 
to be retrieved will be available

For the actions mentioned above we write a function create_df which will  get the corresponding links on the page
'''

def create_df(url = r'http://www.anh.gov.co/estadisticas-del-sector/sistemas-integrados-operaciones/estad%C3%ADsticas-producci%C3%B3n'):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup, SoupStrainer
    #Making the request to get the contents of the html page
    anh_html= requests.get(url).content
    #Parsing it into html
    anh_html = anh_html.decode('utf-8')
    soup = BeautifulSoup(anh_html,'html.parser')
    
    tags_a =[]
    urls_href =[]

    #Appending the information we find inside <a> tags
    for link in soup.find_all('a', href=True):
        tags_a.append(link.text)
        urls_href.append(link['href'])

    #Saving the results of the above on a data frame
    All_Links = pd.DataFrame()   
    All_Links['tags']= tags_a
    
    All_Links['url'] =urls_href


    #Filtering only the results that are of our interest which are the ones cointaining the word "Crudo"
    All_Links=All_Links[All_Links['tags'].astype(str).str.lower().str.contains('Crudo',case=False)==True]
    All_Links['Full_link'] = r'http://www.anh.gov.co'+ All_Links['url']

    #Additionally it will be helpful to associate the year that should be in the name of the file with each link

    def detect_year(string):
        string= string.encode('ascii','ignore')    
        m=[int(s) for s in string.split() if s.isdigit()]
        if len(m)==0:
            return 0
        else:
            return m[0]
    
    #Applying the function

    All_Links['years'] = All_Links.apply(lambda x: detect_year(x.tags),axis =1)
    del  All_Links['tags']
    del  All_Links['url']


    return All_Links.reset_index(drop=True)


