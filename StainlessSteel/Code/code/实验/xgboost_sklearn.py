import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor


other_params = {
    'eta': 0.3,
    'n_estimators': 500,
    'gamma': 0,
    'max_depth': 6,
    'min_child_weight': 1,
    'colsmaple_bytree': 1,
    'colsample_bylevel': 1,
    'subsample': 1,
    'reg_lambda': 1,
    'reg_alpha': 0,
    'seed': 33
}
import time

pd.set_option('max_colwidth', 100)
temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据.xls')
# temp_data = pd.read_excel('./汇总后的数据.xls')
# temp_data = pd.read_excel('../../文件/新的汇总后的数据（添加基建数据）.xls')

record_time = time.ctime(time.time())


temp_data = temp_data.drop('日期', axis=1)
# temp_data = temp_data.drop('进出口焦煤', axis=1)
from sklearn.model_selection import train_test_split
y = temp_data['期货价格']
X = temp_data.drop('期货价格', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
features = list(X_train.columns)


cv_params = {'n_estimators': np.linspace(100, 1000, 10, dtype=int)}
regress_model = xgb.XGBRegressor(**other_params)
gs = GridSearchCV(regress_model, cv_params, verbose=2, refit=True, cv=5, n_jobs=-1)
gs.fit(X_test, y_test)
print('the best parameters: ', gs.best_params_)
print('the best score :', gs.best_score_)