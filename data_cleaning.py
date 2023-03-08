#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:39:04 2023

@author: svetlanamaslenkova
"""
import pickle5 as pickle
from collections import Counter
import re

curr_path = '/Users/svetlanamaslenkova/Documents/DS_project/'
data_scraped_path = curr_path + 'data_scraped/'

# open & and retrieve rows with salary info
with open(data_scraped_path + 'gcc_jobs_df.pkl', 'rb') as handle:
    jobs_df = pickle.load(handle)
print(jobs_df.shape)
jobs_with_salary_df = jobs_df[~((jobs_df.salary_estimate=='-1')|(jobs_df.salary_estimate==-1))\
                              |~((jobs_df.salary_description=='-1')|(jobs_df.salary_description==-1))]
print('n of rows with salary: ', jobs_with_salary_df.shape[0])

jobs_to_delete= ['carpenter foreman', 'retail operation executive', 'lead generation specialist', 'digital marketing specialist']
jobs_with_salary_df = jobs_with_salary_df[~(jobs_with_salary_df['job_title'].str.lower().str.contains(('|').join(jobs_to_delete)))]

## clean and organize salary info
# convert types into str
jobs_with_salary_df.salary_estimate = jobs_with_salary_df.salary_estimate.astype(str) 
jobs_with_salary_df.salary_description = jobs_with_salary_df.salary_description.astype(str) 
# create columns with time period salary info
jobs_with_salary_df['hourly'] = jobs_with_salary_df['salary_estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
jobs_with_salary_df['annually'] = jobs_with_salary_df['salary_description'].apply(lambda x: 1 if any(map(x.lower().__contains__, ['per annum', 'usd'])) else 0)
# add for Cobblestone job
jobs_with_salary_df.loc[412, 'annually'] = 1

# merge two salary columns
jobs_with_salary_df['salary'] = [a if b=='-1' else b for a,b in zip(jobs_with_salary_df.salary_estimate.values, jobs_with_salary_df.salary_description.values)]
# remove unnecessary text info from salary column
jobs_with_salary_df['salary'] = jobs_with_salary_df['salary'].apply(lambda x: x.split('(')[0])
# create a column with the currency info 
jobs_with_salary_df['currency'] = jobs_with_salary_df['salary'].apply(lambda x: 'usd' if 'usd' in x.lower() or '$' in x.lower() else 'aed' if 'aed' in x.lower()\
                                              else 'bhd' if 'bhd' in x.lower() else 'qar' if 'qar' in x.lower() \
                                              else 'sar' if 'sar' in x.lower() else 'omr' if 'omr' in x.lower() \
                                              else 'kd' if 'kd' in x.lower()else -1)


# get salary column cleaned from text
# remove text from the salary column and replace 'K' with zeroes
salary = jobs_with_salary_df['salary'].apply(lambda x: x.lower().replace('k', '000'))
salary = salary.apply(lambda x: re.sub('[a-zA-Z$]', '', x))
# salary = salary.apply(lambda x: re.sub(' - 0%', '', x))

# create columns for min and max salary
min_salary = salary.apply(lambda x: x.replace('–', '-').split('-')[0])
max_salary = salary.apply(lambda x: x.replace('–', '-').split('-')[1] if \
                len(x.replace('–', '-').split('-'))>1 else x.replace('–', '-').split('-')[0])
# clean the columns from spaces and unnecesary symbols
jobs_with_salary_df['min_salary'] = min_salary.apply(lambda x: x.replace(',', '').replace(' ', ''))
jobs_with_salary_df['max_salary'] = max_salary.apply(lambda x: x.replace(',', '').replace(' ', ''))


# convert column types
jobs_with_salary_df['min_salary'] = jobs_with_salary_df['min_salary'].astype(float)
jobs_with_salary_df['max_salary'] = jobs_with_salary_df['max_salary'].astype(float)

# convert currency to AED
currenccies_dict = {'usd' : 3.67,
               'bhd' : 9.76,
               'qar' : 1.01,
               'sar' : 0.98,
               'omr' : 9.57,
               'kd' : 12,
               'aed':1.0}

jobs_with_salary_df['min_salary'] = jobs_with_salary_df.apply(lambda x: x['min_salary'] * currenccies_dict[x['currency']], axis=1)
jobs_with_salary_df['max_salary'] = jobs_with_salary_df.apply(lambda x: x['max_salary'] * currenccies_dict[x['currency']], axis=1)
# add the average salary column
jobs_with_salary_df['avg_salary'] = (jobs_with_salary_df.min_salary + jobs_with_salary_df.max_salary) / 2

# convert salary into monthly salary
jobs_with_salary_df['min_salary'] = jobs_with_salary_df.apply(lambda x: x.min_salary * 160 if x.hourly==1 else x.min_salary/12 if x.annually==1 else x.min_salary, axis=1)
jobs_with_salary_df['max_salary'] = jobs_with_salary_df.apply(lambda x: x.max_salary * 160 if x.hourly==1 else x.max_salary/12 if x.annually==1 else x.max_salary, axis=1)
jobs_with_salary_df['avg_salary'] = jobs_with_salary_df.apply(lambda x: x.avg_salary * 160 if x.hourly==1 else x.avg_salary/12 if x.annually==1 else x.avg_salary, axis=1)

# remove new line character and rating from company name
jobs_with_salary_df['company_name'] = jobs_with_salary_df['company_name'].apply(lambda x: x.split('\n')[0] if len(x.split('\n'))>1 else x)

# add column indicating if a job was posted more than 30 days ago
jobs_with_salary_df['older_than_30_days'] = jobs_with_salary_df['job_age'].apply(lambda x: 1 if '30' in x.lower() else 0)

# add job family column
jobs_with_salary_df['job_fam'] = jobs_with_salary_df.job_title.apply(lambda x: 'ds' if 'data scien' in x.lower() \
                                              else 'da' if 'analy' in x.lower() \
                                                  else 'ml' if 'machine learning' in x.lower()\
                                                      # else 'research' if 'research' in x.lower()\
                                                      else 'other')
# add company age column
jobs_with_salary_df['founded'] = jobs_with_salary_df['founded'].astype(int)
jobs_with_salary_df['company_age'] = jobs_with_salary_df.founded.apply(lambda x: x if x<0 else 2023 - x)
    
## add required skills columns
# python
jobs_with_salary_df['python_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
# r
jobs_with_salary_df['r_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'r-studio' in x.lower() or 'r studio' in x.lower() else 0)
# spark
jobs_with_salary_df['spark_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
# aws
jobs_with_salary_df['aws_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
# pytorch
jobs_with_salary_df['pytorch_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'pytorch' in x.lower() or 'torch' in x.lower() else 0)
# tf
jobs_with_salary_df['tf_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'tensorflow' in x.lower() else 0)
# ml
jobs_with_salary_df['ml_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'machine learning' in x.lower() else 0)
# power bi OR tableau
jobs_with_salary_df['pbi_tableau_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'power bi' in x.lower() or 'tableau' in x.lower() else 0)
# statistics
jobs_with_salary_df['stats_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'statisti' in x.lower() else 0)
# sql
jobs_with_salary_df['sql_yn'] = jobs_with_salary_df['job_description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

jobs_with_salary_df.sum()
# keep the following skills: stats_yn, ml_yn, sql_yn, python_yn

# see the frequency of words n descriptions
result_text = ''
for text in list(jobs_with_salary_df.job_description.values):
    result_text = result_text + ' ' + text.replace('\n', ' ')
freq = Counter(result_text.split()).most_common(60)
words = re.findall(r'\w+', result_text)
two_words = [' '.join(ws) for ws in zip(words, words[1:])]
wordscount = {w:f for w, f in Counter(two_words).most_common() if f > 1}

jobs_with_salary_df['experience_level'] = jobs_with_salary_df['job_title'].apply(lambda x: 'junior' if 'junior' in x.lower() or 'jr.' in x.lower() or 'entry' in x.lower() \
                                           else 'senior' if 'senior' in x.lower() or 'sr.' in x.lower() or 'expert' in x.lower() \
                                               or 'lead' in x.lower()  or 'principal' in x.lower() else 'other')

    
# # add job simplified column
jobs_with_salary_df['job_simp'] = jobs_with_salary_df['job_title'].apply(lambda x: \
            'analyst' if 'analyst' in x.lower() else 'data engineer' if 'data engineer' in x.lower() else 'data scientist' if 'data scientist' in x.lower()\
                else 'director' if 'director' in x.lower() else 'manager' if 'manager' in x.lower() else 'machine learning engineer' if \
                    'machine learning engineer' in x.lower() else 'researcher' if 'research' in x.lower() else 'other')
jobs_with_salary_df['job_simp'].value_counts()
jobs_with_salary_df['job_fam'].value_counts()

    

import geonamescache
gc = geonamescache.GeonamesCache()

def get_country(city, gc):
    if city.lower()=='remote':
        return 'remote'
    country_code = gc.search_cities(city, case_sensitive=False)[0]['countrycode']
    if country_code=='AE':
        return city
    return country_code
    
jobs_with_salary_df['country'] = jobs_with_salary_df['location'].apply(lambda x: get_country(x, gc))


# # rearrange the columns
# jobs_with_salary_df = jobs_with_salary_df[['job_title',
#  'salary_estimate',
#  'job_description',
#  'rating',
#  'company_name',
#  'location',
#  'job_age',
#  'size',
#  'founded',
#  'type_of_ownership',
#  'industry',
#  'sector',
#  'revenue',
#  'competitors',
#  'date_scrapped',
#  'job_fam',
#  'salary_description',
#  'hourly',
#  'annually',
#  'salary',
#  'currency',
#  'min_salary',
#  'max_salary',
#  'avg_salary',
#  'company_age',
#  'python_yn',
#  'r_yn',
#  'spark_yn',
#  'aws_yn',
#  'pytorch_yn',
#  'tf_yn',
#  'ml_yn',
#  'pbi_tableau_yn',
#  'stats_yn',
#   'sql_yn',
#  'experience_level'
# ]]

jobs_with_salary_df.to_csv('glassdoor_jobs.csv', index=False)