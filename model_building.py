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
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import statsmodels.api as sm
import pickle

df = pd.read_csv('glassdoor_jobs.csv')
df = df[df.country.str.contains(r'Abu Dhabi|Dubai')]

revenue = [5.0, 6.7, 54.2, 326.5, 393.0, 1., 1., 1., 1., 1, 1., 5.6, 23.7, 5., 1., 23.1, 33.6, 1., 1., 1., 13200.0, 243.4, 20000, 5.2, 246.9, 243.4, 5.4, 1., 5.0, 243.4]
df['revenue'] = revenue

size = [1, 1, 2, 3, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 3, 4, 4, 3, 3, 2, 3, 3, 1, 1, 2, 4]
df['size'] = size

df.loc[19, 'type_of_ownership'] = 'Company - Private'
df.loc[48, 'type_of_ownership'] = 'Company - Private'
df.loc[23, 'type_of_ownership'] = 'Company - Private'
df.loc[24, 'type_of_ownership'] = 'Company - Private'
df.loc[27, 'type_of_ownership'] = 'Company - Private'
df.loc[28, 'type_of_ownership'] = 'Company - Private'
df.loc[31, 'type_of_ownership'] = 'Company - Private'
df.loc[35, 'type_of_ownership'] = 'Company - Private'

# choose relevant columns
df_model = df[['rating', 'country', 'size', 'revenue', 'type_of_ownership', 'job_fam', 'avg_salary',\
                'experience_level', 'older_than_30_days', 'stats_yn', 'ml_yn', 'python_yn']]

    
# df_model['size'] = df_model['size'].apply(lambda x: 'Less than 1000 Emloyees' if x=='1 to 50 Employees' or x=='51 to 200 Employees' \
#                                          or x=='501 to 1000 Employees' else 'More than 10000 Employees' \
#                        if x=='5001 to 10000 Employees' or x=='10000+ Employees' else 'Unnkown' if x=='Unknown' or x=='-1' else x)

df_model['type_of_ownership'] = df_model['type_of_ownership'].apply(lambda x: 'Unknown' if x=='-1' or x=='Unknown' or x=='College / University' else x)

# df_model['country'] = df_model['country'].apply(lambda x: 'Other GCC cities' if x=='BH' or x=='KW' or x=='OM' or x=='SA' or x=='remote' or x=='Sharjah' else x)

# get one hot encoded variables
df_dum = pd.get_dummies(df_model)

# create splits
var_names = list(df_dum.drop(columns=['avg_salary', 'type_of_ownership_Company - Public', 'python_yn'], axis=1).columns)
X = np.asarray(df_dum.drop(columns=['avg_salary', 'type_of_ownership_Company - Public', 'python_yn'], axis=1))
y = df_dum['avg_salary'].values

# var_names = list(df_model.drop('avg_salary', axis=1).columns)
# X = np.asarray(df_model.drop('avg_salary', axis=1))
# y = df_model['avg_salary'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=44)

# multiple LR
# r2 0.819
X_sm = sm.add_constant(X)
model = sm.OLS(y, X, X_sm)
res = model.fit()
print(res.summary(xname=var_names))
# print(res.score())

# sklearn LR
# best error -12817.47
lm = LinearRegression()
reg = lm.fit(X_train, y_train)
np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=2)) # too small dataset

# lasso regression
# best alpha 55.6 with error -13259.92 # UAE
# best alpha 88.3 with error -54746.42 # GCC
# best alpha 643 with error -5634.23 # UAE
# best alpha 1999.0  with error -7485. # UAE (with revenue)
lm_l = Lasso(alpha=1999.0, tol=0.01)
lm_l_res = lm_l.fit(X_train, y_train)
print(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=2)))

alpha = []
error = []
for i in range(1, 3000):
    alpha.append(i/1)
    lml = Lasso(alpha=(i/1), tol=0.01)
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error', cv=2)))
plt.plot(alpha, error)

err_tuple = tuple(zip(alpha, error))
df_err = pd.DataFrame(err_tuple, columns=['alpha', 'error'])
df_err[df_err.error==max(df_err.error)] 


# random forest
# best error -11117.28            UAE
# with GS best error is -9215.17  UAE
# best error -20197.45            GCC
# with GS best error is -19662.4    GCC
rf = RandomForestRegressor(criterion='absolute_error', max_depth=6, max_features='log2', n_estimators=20)
rf.fit(X_train, y_train)
print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error')))

# grid search RF
parameters = {'n_estimators':range(10,300, 10), 'criterion':('mse', 'mae'), \
              'max_features':('auto', 'sqrt', 'log2'), 'max_depth':[3,6, 9]}
gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)
print(gs.best_score_)
print(gs.best_estimator_)

# Gradient boosting
gbr = GradientBoostingRegressor(loss='absolute_error', max_depth=6, max_features='log2',\
                           n_estimators=50, random_state=0)
    
gbr.fit(X_train, y_train)
# grid search GB
parameters = {'n_estimators':range(10,300, 10),  \
              'max_features':('auto', 'log2'), 'max_depth':[3,6, 9], 'subsample':[0.9, 1.]}
gs_gbr = GridSearchCV(gbr, parameters, scoring='neg_mean_absolute_error', cv=3)
gs_gbr.fit(X_train, y_train)
print(gs_gbr.best_score_)
print(gs_gbr.best_estimator_)


# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = rf.predict(X_test)
tpred_gbr = gbr.predict(X_test)

lm_mae = np.round(mean_absolute_error(y_test, tpred_lm), 2)
lm_r2 = np.round(r2_score(y_test, tpred_lm), 2)
lms_mae = np.round(mean_absolute_error(y_test, tpred_lml), 2)
lms_r2 = np.round(r2_score(y_test, tpred_lml), 2)
rf_mae = np.round(mean_absolute_error(y_test, tpred_rf), 2)
rf_r2 = np.round(r2_score(y_test, tpred_rf), 2)
gbr_mae = np.round(mean_absolute_error(y_test, tpred_gbr), 2)
gbr_r2 = np.round(r2_score(y_test, tpred_gbr), 2)
print('LR: MAE {}, R2 {}'.format(lm_mae,lm_r2))
print('Lasso: MAE {}, R2 {}'.format(lms_mae,lms_r2))
print('RF: MAE {}, R2 {}'.format(rf_mae,rf_r2))
print('GBR: MAE {}, R2 {}'.format(gbr_mae,gbr_r2))

# test an ensemple of rf and lasso regression
print(mean_absolute_error(y_test, (tpred_lml+tpred_rf)/2))

plt.figure(figsize=(10,10))
plt.scatter(y_test, tpred_rf, c='crimson', s=50)
p1 = max(max(tpred_rf), max(y_test))
p2 = min(min(tpred_rf), min(y_test))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=15)
plt.ylabel('Predictions', fontsize=15)
plt.axis('equal')
plt.title('Random Forest, MAE: {}, R2: {}'.format(rf_mae, rf_r2), fontdict={'size':25})
# Adding text on the plot.
plt.show()


plt.figure(figsize=(10,10))
plt.scatter(y_test, tpred_gbr, c='crimson', s=50)
p1 = max(max(tpred_gbr), max(y_test))
p2 = min(min(tpred_gbr), min(y_test))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=15)
plt.ylabel('Predictions', fontsize=15)
plt.axis('equal')
plt.title('Gradient boosting, MAE: {}, R2: {}'.format(gbr_mae, gbr_r2), fontdict={'size':25})
plt.show()

plt.figure(figsize=(10,10))
plt.scatter(y_test, tpred_lml, c='crimson', s=50)
p1 = max(max(tpred_lml), max(y_test))
p2 = min(min(tpred_lml), min(y_test))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=15)
plt.ylabel('Predictions', fontsize=15)
plt.axis('equal')
plt.title('Lasso regression, MAE: {}, R2: {}'.format(lms_mae, lms_r2) , fontdict={'size':25})
plt.show()


# gs.best_estimator_.predict(X_test[0, :].reshape(1, -1))

importances = [a for (a,b) in sorted(zip(gs.best_estimator_.feature_importances_, var_names))]
features = [b for (a,b) in sorted(zip(gs.best_estimator_.feature_importances_, var_names))]
plt.barh(features, importances)
top_features = features[-14:]

# try estimator with the most important features
# create splits
var_names = list(df_dum[top_features])
X = np.asarray(df_dum[top_features])
y = df_dum['avg_salary'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=43)

rf = RandomForestRegressor(criterion='mae', max_depth=6, max_features='log2',
                      n_estimators=10)
print(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error')))

# grid search 10 features 4573, 0.11
parameters = {'n_estimators':range(10,150, 10), \
              'max_features':('auto', 'log2'), 'max_depth':[3,6, 9]}
    
gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)
print(gs.best_score_)
print(gs.best_estimator_)

# for 12 features
rf_12 = RandomForestRegressor(criterion='mae')
gs_12 = GridSearchCV(rf_12, parameters, scoring='neg_mean_absolute_error', cv=3)
gs_12.fit(X_train, y_train)
print(gs_12.best_score_)
print(gs_12.best_estimator_)

# for 8 features 4606, 0.14
rf_8 = RandomForestRegressor(criterion='mae')
gs_8 = GridSearchCV(rf_8, parameters, scoring='neg_mean_absolute_error', cv=3)
gs_8.fit(X_train, y_train)
print(gs_8.best_score_)
print(gs_8.best_estimator_)

# for 11 features 4726, 0.12
rf_11 = RandomForestRegressor(criterion='mae')
gs_11 = GridSearchCV(rf_11, parameters, scoring='neg_mean_absolute_error', cv=3)
gs_11.fit(X_train, y_train)
print(gs_11.best_score_)
print(gs_11.best_estimator_)

# for 14 features
rf_14 = RandomForestRegressor(criterion='mae')
gs_14 = GridSearchCV(rf_14, parameters, scoring='neg_mean_absolute_error', cv=3)
gs_14.fit(X_train, y_train)
print(gs_14.best_score_)
print(gs_14.best_estimator_)

# test
tpred_rf = gs.best_estimator_.predict(X_test)
rf_mae = np.round(mean_absolute_error(y_test, tpred_rf), 2)
r2 = np.round(r2_score(y_test, tpred_rf), 2)

plt.figure(figsize=(10,10))
plt.scatter(y_test, tpred_rf, c='crimson', s=50)
p1 = max(max(tpred_rf), max(y_test))
p2 = min(min(tpred_rf), min(y_test))
plt.plot([p1, p2], [p1, p2], 'b-')
plt.xlabel('True Values', fontsize=15)
plt.ylabel('Predictions', fontsize=15)
plt.axis('equal')
plt.title('Random Forest, MAE: {}, R2: {}'.format(rf_mae, r2), fontdict={'size':25})
plt.show()



# pickle the model
pkl = {'model': gbr}
pickle.dump(pkl, open('model_file' + '.p', 'wb'))

# ['rating',
#  'size',
#  'revenue',
#  'older_than_30_days',
#  'stats_yn',
#  'ml_yn',
#  'country_Abu Dhabi',
#  'country_Dubai',
#  'type_of_ownership_Company - Private',
#  'type_of_ownership_Unknown',
#  'job_fam_da',
#  'job_fam_ds',
#  'job_fam_ml',
#  'job_fam_other',
#  'experience_level_other',
#  'experience_level_senior']
