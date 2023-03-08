import pandas as pd
import glassdoor_scraper as gs
import pickle5 as pickle 

driver_path = "/Users/svetlanamaslenkova/Documents/DS_project/chromedriver_mac64/chromedriver"
save_to_path = '/Users/svetlanamaslenkova/Documents/DS_project/data_scraped/GCC_region/'


for location in ['Bahrain', 'Kuwait', 'Oman', 'Qatar', 'Saudi Arabia', 'United Arab Emirates']:
# for location in ['Oman', 'Saudi Arabia', 'United Arab Emirates']:
# for location in ['Bahrain']: 
    # webscraping Data Scientist Jobs
    df = gs.get_jobs('data scientist', location, 500, True, driver_path, 10)
    # saving df
    file_name = location.lower() + '_ds_jobs_scraped.pkl'
    with open(save_to_path + file_name, 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    # webscraping Data Analyst Jobs
    df = gs.get_jobs('data analyst', location, 500, True, driver_path, 10)
    # saving df
    file_name = location.lower() + '_da_jobs_scraped.pkl'
    with open(save_to_path + file_name, 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    # webscraping Machine Learning engineer Jobs
    df = gs.get_jobs('machine learning', location, 500, True, driver_path, 10)
    # saving df
    file_name = location.lower() + '_ml_jobs_scraped.pkl'
    with open(save_to_path + file_name, 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)