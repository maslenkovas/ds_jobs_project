import pandas as pd
import glassdoor_scraper as gs

path = "/Users/svetlanamaslenkova/Documents/DS_project/chromedriver_mac64/chromedriver"

df = gs.get_jobs('data scientist', 'United Arab Emirates', 5, True, path, 15)

print(df)