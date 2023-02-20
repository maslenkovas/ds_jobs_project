#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:15:33 2023

@author: svetlanamaslenkova
"""

import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle


app = Flask(__name__)

# load the model
def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

# prediction function
def ValuePredictor(to_predict_list):
 	to_predict = np.array(to_predict_list).reshape(1, 25)
 	loaded_model = load_models()
 	result = loaded_model.predict(to_predict)
 	return result[0]

def preproccess(response):
    # response = {'rating': '-1', 'older_than_30_days': '0', 'location': 'Abu-Dhabi', 'size': '1-50 Employees', \
    #             'type_of_ownership': 'College/University', 'revenue': '$25 to $100', 'job_fam': 'DS', 'experience': 'Junior'}
    rating = response['rating']
    older_than_30_days = response['older_than_30_days']
    location_abu_dhabi = 1 if response['location'] == 'Abu-Dhabi' else 0
    location_dubai = 1 if response['location'] == 'Dubai' else 0
    location_shajah = 1 if response['location'] == 'Sharjah' else 0
    size_1to50 = 1 if response['size'] == '1-50 Employees' else 0
    size_51to200 = 1 if response['size'] == '51-200 Employees' else 0
    size_201to500 = 1 if response['size'] == '201-500 Employees' else 0
    size_501to1000 = 1 if response['size'] == '501-1000 Employees' else 0
    size_1000to10000 = 1 if response['size'] == '1000-10000 Employees' else 0
    size_idk = 1 if response['size'] == "I don't know" else 0
    type_of_ownership_college = 1 if response['type_of_ownership'] == "College/University" else 0
    type_of_ownership_private = 1 if response['type_of_ownership'] == "Private" else 0
    type_of_ownership_public = 1 if response['type_of_ownership'] == "Public" else 0
    type_of_ownership_idk = 1 if response['type_of_ownership'] == "I don't know" else 0
    revenue25_100 = 1 if response['revenue'] == "$25 to $100" else 0
    revenue100_500 = 1 if response['revenue'] == "$100 to $500" else 0
    revenue_idk = 1 if response['revenue'] == "I don't know" else 0
    job_fam_ds = 1 if response['job_fam'] == "DS" else 0
    job_fam_da = 1 if response['job_fam'] == "DA" else 0
    job_fam_ml = 1 if response['job_fam'] == "ML" else 0
    job_fam_other = 1 if response['job_fam'] == "Other" else 0
    experiemnce_junior = 1 if response['experience'] == "Junior" else 0
    experiemnce_senior = 1 if response['experience'] == "Senior" else 0
    experiemnce_middle = 1 if response['experience'] == "Middle" else 0
    
    
    to_predict_list = [rating, older_than_30_days, location_abu_dhabi, location_dubai, location_shajah, size_1to50, size_201to500, \
                       size_1000to10000, size_501to1000, size_51to200, size_idk, type_of_ownership_college, type_of_ownership_private, \
                           type_of_ownership_public, type_of_ownership_idk, revenue100_500, revenue25_100, revenue_idk, job_fam_da, job_fam_ds,\
                               job_fam_ml, job_fam_other, experiemnce_junior, experiemnce_middle, experiemnce_senior]
    
    to_predict_list = list(map(int, to_predict_list))
    
    return to_predict_list


@app.route("/")
def Home():
    return render_template("index.html")

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        response = request.form.to_dict()
        to_predict_list = preproccess(response)
        result = np.round(int(ValuePredictor(to_predict_list)/1000))	
        result_message = "The expected salary is around {}k AED per month".format(result)
        	
        return render_template("result.html", prediction = result_message)



# ['rating',
#  'older_than_30_days',
#  'location_Abu Dhabi',
#  'location_Dubai',
#  'location_Sharjah',
#  'size_1 to 50 Employees',
#  'size_201 to 500 Employees',
#  'size_5001 to 10000 Employees',
#  'size_501 to 1000 Employees',
#  'size_51 to 200 Employees',
#  'size_Unknown',
#  'type_of_ownership_College / University',
#  'type_of_ownership_Company - Private',
#  'type_of_ownership_Company - Public',
#  'type_of_ownership_Unknown',
#  'revenue_$100 to $500 million (USD)',
#  'revenue_$25 to $100 million (USD)',
#  'revenue_Unknown / Non-Applicable',
#  'job_fam_da',
#  'job_fam_ds',
#  'job_fam_ml',
#  'job_fam_other',
#  'experience_level_junior',
#  'experience_level_na',
#  'experience_level_senior']