
# Demo exercise for DAI group interview

_Author: Matteo Jucker Riva_    

Dockerized and deployed version

## Links    
[online repo](https://github.com/ciskoh/dai_group_demo)   
[server AWS](http://3.68.190.143:8050/)

## Request   

__Situation__: The client is a reseller of  running shoes (brand “Fast Feed”) and asked you to provide him insights about people that do running as a sport either professional or as a hobby. He would like to know how many people from age 0-20, 21-30, 31-40, 41-50, 51+ are participating in the Zurich Marathon from 2014 – 2018. He is trying to do some research on the  https://datasport.com/de/ but doesn’t know how to get the data.    
__Goal:__   
a. Code a webscraper in Python and parse the data from the Zurich Marathon from the website: https://services.datasport.com/2014/lauf/zuerich/alfab.htm for all athletes from a-z, from the year 2014 – 2018. 

b. Store the data in a database with the following fields:   
*Id is an auto-generated integer (autoincrement)   
*Category: Varchar   
*Rang:  varchar   
*Fullname: varchar   
*Age_year: integer   
*Location: varchar   
*total_time timestamp   
*run_link: varchar   
*Run_year: integer   
    
c.Create a Dashboard in Python Dash with the following criteria:
  i.     Create drop-down filters for the group of ages (0-20, 21-30, etc,) and run_year
  ii.     Provide to the reseller a visualization on the count of athletes per “age group” and run_year (see sample image below) and a datatable with all attributes from point b.
  iii.     Create a callback-function on the filters to update the visualization and the datatable. If both filters are active it is an AND-filter   
   
_Additionally_, if you have some time left: 
Deploy the tool in the cloud, preferably on AWS or Azure (on AWS you get an Ubuntu 20.4 server on the free tier for 1 year)   
 i.     Use a webserver like Apache HTTPD or Nginx (no need for HTTPS certificate)   
ii.     Choose the storage as you prefer   
 

## Description & development notes

__Dependecies and install__   
All code is created with pycharm in python 3.9.    
   
Virtual environment & package management created with Conda.   
See `environment.yml` for list of dependencies
Install all dependencies with the following command:   
    `conda env create -f environment.yml`   

__Dockerized version__ all files related with the dashboard are cointained in the `app`folder. DOCKERFILE contains the instruction to create a docker image for the app using `environment.yml` . 

config.py implements a `Config` class that holds the main settings for the creation of the database

### Workflow:

1. Webscraping using Request and BF4:    
    `app/modules/scrape_runner_data.py` handles all web_scraping and is called during database creation   
   
1. Database creation using sqLite:   
    `app/modules/create_runner_db.py` creates the database file and populates it using `app/modules/scrape_data.py`   
   
1. Dashboard with dash+plotly:    
    `app/dashboard.py`creates he dasboard using Dash & plotly
   
1. Deployment
    Deployed with docker on AWS using The Elastic Container Registry (ECR) & Elastic Container Service (ECS) at the following address : [http://3.68.190.143:8050/](http://3.68.190.143:8050/)

