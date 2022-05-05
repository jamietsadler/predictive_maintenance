# -*- coding: utf-8 -*-
"""NASA Predictive Maintenance.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PkbpHlM4SAuLdOjtEIhmo-GmLokbeFu0

# NASA Turbofan Predictive Maintenance

This notebook aims to predict the remaining useful life (RUL) of engines using operational & sensor reading data, provided by NASA via Kaggle. 

It will start by exploring the data using statistics and visualisations, before moving onto modelling the data. The aim o the Kaggle conmpetition is simply to predict if an engine has failed or not (i.e. RUL is 0). However, there are numerous ways in which this can be achieved. A range of models have been employed in this analysis.

The data will be modelled in 2 main ways:

**1. Regression:**

This will aim to predict a continuous value for RUL. Models will be assessed on their ability to closely match the RUL of engines.

**2. Classification:**

For this, the data will have to be classified using the RUL feature. if the RUL is above 0, then the engines are still active (data labelled 0), otherwise, the engine has failed (data labelled 1). Due to the large disparity in class size, accuracy metrics are initially expected to be poor.

## Improvement Points

* Perform wider range of EDA to further understand data.
* Make engine no. a categoricalk feature in models.
* Test wider range of scalers.
* Test Lambda and Ridge Regression models to try and utilise feature coefficient minimisation.
* Tune hyperparemters on Random Forest model.
* Time series feature engineering (Rolling values, fourier series transformations).
* Try to even class sizes for classification (upsampling, SMOTE etc).
* Classify engine as 'Failed' or not based on results of regression models.

### Load Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, confusion_matrix, precision_score, accuracy_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV

"""### Load Data"""

train_df = pd.read_csv('train_data.csv')
assess_df = pd.read_csv('test_data.csv')

"""## EDA"""

train_df.head()

train_df.shape

train_df['engine_no'].nunique()

train_df[train_df.RUL == 0]['RUL'].count()

train_df.isna().sum()

"""Sensors 22-27 have no data so drop"""

train_df.drop(['sensor_22', 'sensor_23', 'sensor_24', 'sensor_25', 'sensor_26', 'sensor_27'], inplace = True, axis = 1)

"""Check columns of data to assess"""

assess_df.head()

"""Generate correlations"""

corrs = train_df.corr()

"""Look at Distributions"""

for col in train_df.columns:
  sns.displot(train_df[col])
  plt.show()

corrs

plt.figure(figsize = (20, 10))
sns.heatmap(corrs)
plt.title('Feature Correlation')
plt.show()

train_df.groupby('RUL').mean().sort_values('RUL', ascending = False)

rul_grouped = train_df.groupby('RUL').mean().sort_values('RUL', ascending = False)

for col in rul_grouped.columns:
  train_df.groupby('RUL').mean().sort_values('RUL', ascending = False)[col].plot(title = 'Mean Value in Lifecycle for ' + col)
  plt.show()

"""Would be good to see how readings change across lifecycle depending on engine """

sample = train_df[(train_df.engine_no == 3) | (train_df.engine_no == 9) | (train_df.engine_no == 23)]

plt.figure(figsize = (20, 10))
sns.lineplot(x = 'RUL', y = 'sensor_21', data = sample, hue = 'engine_no')
plt.title('Sensor values for Subset of Engines')
plt.show()

plt.figure(figsize = (20, 10))
sns.lineplot(x = 'RUL', y = 'sensor_11', data = sample, hue = 'engine_no')
plt.title('Sensor values for Subset of Engines')
plt.show()

plt.figure(figsize = (20,10))
sns.lineplot(x = 'RUL', y = 'op_setting_3', data = sample, hue = 'engine_no')
plt.title('Operational setting values for Subset of Engines')
plt.show()

"""## Regression

This problem can be represented as a regression one because the 'RUL" can be modelled as a continuous variable, whereby the engine fails when the predicted value is close to 0. Different regression models require different assumptions, therefore each model will have different sets of feature engineering.

The following regression models will not directly aim to predict whether the engine has failed or not, as their intended purpose is to obtain a close match in the relationship between the features and the target variable.

### Linear Regression
"""

from sklearn.linear_model import LinearRegression

"""Start by creating a basuc Linear Regression Model using all features and basic feature engineering (expected to score badly because of high multi-colinearity between features and large number of features).

Engine number is categorical variable, due to high number of categories it will not be used for now.
"""

train_df.head()

X, y = train_df.iloc[:, 1:-1], train_df.iloc[:, -1]

"""split into training and testing"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

"""scale data"""

sc = StandardScaler()

X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

lm_model = LinearRegression() # instantiate

lm_model.fit(X_train_scaled, y_train) # fit data

y_hat = lm_model.predict(X_test_scaled) # predict

"""Assess predictions"""

rmse = np.sqrt(mean_squared_error(y_test, y_hat))
mae = mean_absolute_error(y_test, y_hat)
r2 = r2_score(y_test, y_hat)
print('rmse: ', rmse, '  mae: ', mae, '  r2: ', r2)

"""As expcted scores are low, due to little feature engineering/selection.

#### PCA

In order to reduce mulitcolinearity between variables, whilst maintaining the highest level of variance in the dataset, pca can be used.
"""

from sklearn.decomposition import PCA

pca = PCA(n_components=10)

X, y = train_df.iloc[:, 1:-1], train_df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

pca_df_train = pca.fit_transform(X_train_scaled)

pca_df_test = pca.transform(X_test_scaled)

pca.explained_variance_

plt.bar(range(len(pca.explained_variance_)), pca.explained_variance_)
plt.title('PCA Explained Variance')
plt.xticks(range(0, 5))
plt.xlabel('PCA Feature')
plt.ylabel('Explained Variance')
plt.show()

"""Try new Linear Regression Model using PCA dataset"""

lm_model_pca = LinearRegression()

lm_model_pca.fit(pca_df_train, y_train) # fit to pca data

y_hat = lm_model_pca.predict(pca_df_test) # Make predictions

rmse = np.sqrt(mean_squared_error(y_test, y_hat))
mae = mean_absolute_error(y_test, y_hat)
r2 = r2_score(y_test, y_hat)
print('rmse: ', rmse, '  mae: ', mae, '  r2: ', r2)

"""### Random Forest"""

from sklearn.ensemble import RandomForestRegressor

X, y = train_df.iloc[:, 1:-1], train_df.iloc[:, -1]

"""split into train and test"""

X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

rf_regressor = RandomForestRegressor(
    n_estimators = 100,
    max_depth = 7,
    max_samples = 0.3, # only use 30% of samples each tree to combat multicolinearity & overfitting
    n_jobs = -1,
    
)

rf_regressor.fit(X_train_scaled, y_train)

y_hat = rf_regressor.predict(X_test_scaled) # predict

rmse = np.sqrt(mean_squared_error(y_test, y_hat))
mae = mean_absolute_error(y_test, y_hat)
r2 = r2_score(y_test, y_hat)
print('rmse: ', rmse, '  mae: ', mae, '  r2: ', r2)

"""### XGBoost

Gradient boosting ensemble method
"""

import xgboost as xgb

X, y = train_df.iloc[:, 1:-1], train_df.iloc[:, -1]

X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

"""Make initial pass at xgb model with no hyperparameter tuning"""

xgb_model = xgb.XGBRegressor(n_jobs = -1) # Instantiate regressor

xgb_model.fit(X_train_scaled, y_train)

xgb_preds = xgb_model.predict(X_test_scaled) # make predictions

rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
mae = mean_absolute_error(y_test,xgb_preds)
r2 = r2_score(y_test, xgb_preds)
print('rmse: ', rmse, '  mae: ', mae, '  r2: ', r2)

"""An ok first pass, with improved performance over previous models.

Now tune hyperparameters
"""

gbm_param_grid = {
    'learning_rate': [0.001, 0.01, 0.1], # learn rate for gradient descent
    'n_estimators': [100, 200, 400], # number of trees
    'subsample': [0.3, 0.5, 0.9], # fraction of samples to use
    'max_depth': [3, 5, 7], # max depth of tree
    'colsample_bytree': [0.5, 0.7, 0.9] # fraction of features to use
}

grid_search = RandomizedSearchCV(
    estimator = xgb_model, 
    param_distributions= gbm_param_grid, 
    scoring = 'neg_mean_squared_error', 
    cv = 4, 
    n_iter=25, # search 25 combinations
    n_jobs = -1)

"""Want to punish outliers so use `neg_mean_squared_error` as scoring"""

grid_search.fit(X_train_scaled, y_train)

grid_search.best_params_

xgb_estimator = grid_search.best_estimator_

xgb_preds = xgb_estimator.predict(X_test_scaled)

rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
mae = mean_absolute_error(y_test,xgb_preds)
r2 = r2_score(y_test, xgb_preds)
print('rmse: ', rmse, '  mae: ', mae, '  r2: ', r2)

"""Slight improvement in metrics achieved after hyperparameter tuning

### Deep Learning (Tensorflow)

Model will be of form multi-layer-perceptron (MLP)

Import libraries from tensorflow
"""

from tensorflow.keras.models import Sequential 
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

"""Define function for building ANN"""

def build_ann_model(learn_rate=0.01, neurons = 32, n_layers = 2):
  model = Sequential()
  model.add(InputLayer(input_shape = (X_train_scaled.shape[1], )))
  for i in range(n_layers):
    model.add(Dense(neurons, activation='relu'))
  model.add(Dense(1))
  my_opt = Adam(learning_rate=learn_rate)
  model.compile(loss='mean_squared_error', metrics=['mae'], optimizer=my_opt)

  return model

earlystop_callback = EarlyStopping(
    monitor='mae', 
    min_delta=0.001, 
    patience=5) # early stopping callback to prevent overfitting

"""Build and fit first model without hyperparameter tuning"""

ann_model = build_ann_model(learn_rate = 0.001, n_layers = 2, neurons = 32)

"""Select & Scale data, use all features for now."""

X, y = train_df.iloc[:, 1:-1], train_df.iloc[:, -1]

X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

ann_model.fit(
    X_train_scaled, 
    y_train,
    epochs = 50, 
    batch_size=200,  
    callbacks = [earlystop_callback], 
    verbose=1, 
    validation_split=0.1
    )

y_hat = ann_model.predict(X_test_scaled)

rmse = np.sqrt(mean_squared_error(y_test, y_hat))
mae = mean_absolute_error(y_test, y_hat)
r2 = r2_score(y_test, y_hat)
print('rmse: ', rmse, '  mae: ', mae, '  r2: ', r2)

"""Now tune hyperparameters"""

def randomised_search(build_fn, X, y):
  param_grid = {
      'batch_size': [50, 75, 100, 150, 200, 400],
      'epochs': [20, 50, 100, 200],
      'learn_rate': [0.001, 0.01, 0.05],
      'neurons': [8, 16, 32, 48, 64],
      'n_layers': [1, 2, 3]
  }
  model = KerasRegressor(build_fn = build_fn)
  grid = RandomizedSearchCV(
    estimator = model,
    param_distributions = param_grid,
    n_jobs = 2,
    n_iter = 25
  )
  grid_result = grid.fit(X, y, verbose = 0)
  
  return grid_result

grid_result = randomised_search(build_ann_model, X_train_scaled, y_train)

print(grid_result.best_params_)
print(grid_result.best_score_)
print(grid_result.scorer_)

"""Build and fit according to result of random grid search"""









"""## Classification

This will involve creating a binary classifiation, whereby the engine has failed ('RUL' == 1) or it hasnt ('RUL' > 0). A new column will be created in the training dataset for this.

Feature engineer classification column
"""

df_train_clf = train_df.copy() # make deep copy of train df

df_train_clf['Failed'] = df_train_clf['RUL'].apply(lambda x: 1 if x == 0 else 0) # binary classifcation according to value of RUL

df_train_clf.drop('RUL', axis = 1, inplace = True) # no longer need RUL

df_train_clf.head()

df_train_clf['Failed'].value_counts()

"""### Logistic Regression

Will first try to predict failure using standard Logistic regression with minimal feature engineering.
"""

from sklearn.linear_model import LogisticRegression

X, y = df_train_clf.iloc[:, 1:-1], df_train_clf.iloc[:, -1] # features and label

"""split into train and test. Need to stratify based on label so that even ratio between classes is achieved."""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, stratify = y) # train and test

X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

lr_model = LogisticRegression(
    solver = 'newton-cg' # better for slightly larger datasets
)

lr_model.fit(X_train_scaled, y_train)

y_hat = lr_model.predict(X_test_scaled)

f1_sc = f1_score(y_test, y_hat)
acc_score = accuracy_score(y_test, y_hat)
recall = recall_score(y_test, y_hat)
print('f1 score: ', f1_sc, '  accuracy score: ', acc_score, '  recall score: ', recall)

"""### XGBoost

will start by using default values for hyperparameters and then prigressing onto tuning to enhance accuracy.
"""

xgb_clf_model = xgb.XGBClassifier(n_jobs = -1)

xgb_clf_model.fit(X_train_scaled, y_train)

y_hat = xgb_clf_model.predict(X_test_scaled)

f1_sc = f1_score(y_test, y_hat)
acc_score = accuracy_score(y_test, y_hat)
recall = recall_score(y_test, y_hat)
print('f1 score: ', f1_sc, '  accuracy score: ', acc_score, '  recall score: ', recall)

"""Now perform hyperparameter tuning"""

gbm_param_grid = {
    'learning_rate': [0.001, 0.01, 0.1], # learn rate for gradient descent
    'n_estimators': [100, 200, 400], # number of trees
    'subsample': [0.3, 0.5, 0.9], # fraction of samples to use
    'max_depth': [3, 5, 7], # max depth of tree
    'colsample_bytree': [0.5, 0.7, 0.9] # fraction of features to use
}

grid_search = RandomizedSearchCV(
    estimator = xgb_clf_model, 
    param_distributions= gbm_param_grid, 
    scoring = 'recall', 
    cv = 4, 
    n_iter=25, # search 25 combinations
    n_jobs = -1)

grid_search.fit(X_train_scaled, y_train)

grid_search.best_params_

xgb_clf_estimator = grid_search.best_estimator_

xgb_preds = xgb_clf_estimator.predict(X_test_scaled)

f1_sc = f1_score(y_test, y_hat)
acc_score = accuracy_score(y_test, y_hat)
recall = recall_score(y_test, y_hat)
print('f1 score: ', f1_sc, '  accuracy score: ', acc_score, '  recall score: ', recall)

"""### Deep Learning (Tensorflow)

Define DL classification build function
"""

def build_ann_clf_model(learn_rate=0.01, neurons = 32, n_layers = 2):
  model = Sequential()
  model.add(InputLayer(input_shape = (X_train_scaled.shape[1], )))
  for i in range(n_layers):
    model.add(Dense(neurons, activation='relu'))
  model.add(Dense(2, activation = 'softmax'))
  my_opt = Adam(learning_rate=learn_rate)
  model.compile(loss='sparse_categorical_crossentropy', metrics=['f1_score'], optimizer=my_opt)

  return model

ann_clf = build_ann_clf_model(
  
)

ann_clf.fit(X_train_scaled, y_train) # fit to data

ann_clf_preds = ann_clf.predict(X_test_scaled)

ann_clf_preds
