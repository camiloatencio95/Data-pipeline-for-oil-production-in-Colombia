# Data pipeline for oil production in Colombia
A data pipeline that starts by webscrapping the National Hidrocarbons Agency and then continues to process data using pandas, to finally be stored in a SQL server in an aproppiate shape.

# Problem description
Colombia's National Hydrocarbon Agency (ANH),in a yearly basis publishes the production of all the Oil producing companies in the country with additional features such as Department/State, County/Municipio and the contract under the production was obtained.

This data is basically a times series, however it is presented in a wide format and in several excel files published on their website, making it hard to query this data.

# Solution
A python based pipeline which webscraps ANH's page will read the excel files, shape them properly for a time series and write into a sql databse.
This pipeline should be run once or twice a month to check for new data published, and be written into the database.

# Local Set-up

Install depencies by running on your terminal `pip3 install -r requirements.txt`

You should also change the password and root of your localhost server when creating the sqlalachemy engine in  the "motor" variable in line 13 of main_script.py
`motor =sqlalchemy.create_engine('mysql+pymysql://your_user:your_pswd@localhost:3306/oil_analysis')`


## Components
  In this project you will find 3 different python scripts:\n
   * `main_script.py` Which is the main script and the one that should be run everytime we need to actually update the records on our database.\n
   * `get_files.py` Which will is in charge of the webscrapping proccess to point the program to the source of the published data by the ANH.\n
   * `clean_files.py` Which is the script in charge of builing a dataframe with the right format and perfmorming all the data cleaning tasks. \n
    
## Technologies used in this project

* [Python]
* [Beautiful Soup 4]
* [Pandas]
* [SqlAlchemy]

## To do
* Develop a complementary Dashboard that lets quickly query oil production per producer, state/county or contract
* Deploy in a cloud-based service
