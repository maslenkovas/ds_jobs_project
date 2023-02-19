#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 11:51:26 2023

@author: svetlanamaslenkova
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import statsmodels.api as sm

df = pd.read_csv('data_eda.csv')

# choose relevant columns
df_model = df[['rating', 'location', 'size', 'type_of_ownership', 'revenue', 'job_fam', 'avg_salary',\
                'experience_level', 'older_than_30_days']]
    
# get one hot encoded variables
df_dum = pd.get_dummies(df_model)

df_dum['size_Unknown'] = df_dum['size_Unknown'] + df_dum['size_-1']
df_dum['type_of_ownership_Unknown'] = df_dum['type_of_ownership_Unknown'] + df_dum['type_of_ownership_-1']
df_dum['revenue_Unknown / Non-Applicable'] = df_dum['revenue_Unknown / Non-Applicable'] + df_dum['revenue_-1']
df_dum = df_dum.drop(columns=['size_-1', 'type_of_ownership_-1', 'revenue_-1'])

# create splits
var_names = list(df_dum.drop('avg_salary', axis=1).columns)
X = np.asarray(df_dum.drop('avg_salary', axis=1))
y = df_dum['avg_salary'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# multiple LR
X_sm = sm.add_constant(X)
model = sm.OLS(y, X, X_sm)
res = model.fit()
print(res.summary(xname=var_names))
print(res.score())

# sklearn LR
# best error -12817.47
lm = LinearRegression()
reg = lm.fit(X_train, y_train)
np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=2)) # too small dataset

# lasso regression
# best alpha 55.6 with error -13259.92
lm_l = Lasso(alpha=55.6, tol=0.01)
lm_l_res = lm_l.fit(X_train, y_train)
print(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=2)))

alpha = []
error = []
for i in range(50, 700):
    alpha.append(i/10)
    lml = Lasso(alpha=(i/10), tol=0.01)
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error', cv=2)))
plt.plot(alpha, error)

err_tuple = tuple(zip(alpha, error))
df_err = pd.DataFrame(err_tuple, columns=['alpha', 'error'])
df_err[df_err.error==max(df_err.error)] 


# random forest
# best error -11117.28
# with GS best error is -9215.17
rf = RandomForestRegressor()
print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error')))

# grid search
parameters = {'n_estimators':range(10,300, 10), 'criterion':('mse', 'mae'), \
              'max_features':('auto', 'sqrt', 'log2')}
gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=2)
gs.fit(X_train, y_train)
print(gs.best_score_)
print(gs.best_estimator_)

# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

print('LR: ', mean_absolute_error(y_test, tpred_lm))
print('Lasso: ', mean_absolute_error(y_test, tpred_lml))
print('RF: ', mean_absolute_error(y_test, tpred_rf))

# test an ensemple of rf and lasso regression
print(mean_absolute_error(y_test, (tpred_lml+tpred_rf)/2))








