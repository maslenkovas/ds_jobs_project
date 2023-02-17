import pandas as pd
import glassdoor_scraper as gs
import pickle5 as pickle 

path = "/Users/svetlanamaslenkova/Documents/DS_project/chromedriver_mac64/chromedriver"

# # webscraping Data Analyst Jobs
# df = gs.get_jobs('data analyst', 'United Arab Emirates', 330, True, path, 15)

# # saving the dataframe
# with open('/Users/svetlanamaslenkova/Documents/DS_project/da_jobs_scraped.pkl', 'wb') as handle:
#     pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

# # webscraping Data Scientist Jobs
# df = gs.get_jobs('data analyst', 'United Arab Emirates', 55, True, path, 15)

# # saving the dataframe
# with open('/Users/svetlanamaslenkova/Documents/DS_project/ds_jobs_scraped.pkl', 'wb') as handle:
#     pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

# # webscraping Machine Learning Jobs
# df = gs.get_jobs('machine learning', 'United Arab Emirates', 200, True, path, 15)
# # # saving the dataframe
# with open('/Users/svetlanamaslenkova/Documents/DS_project/ml_jobs_scraped.pkl', 'wb') as handle:
#     pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)