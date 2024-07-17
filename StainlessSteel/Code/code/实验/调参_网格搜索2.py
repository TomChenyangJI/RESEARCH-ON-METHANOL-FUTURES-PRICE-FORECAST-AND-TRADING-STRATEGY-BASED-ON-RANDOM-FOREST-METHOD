import pandas as pd
import time
import numpy as np
# import matplotlib.pyplot as plt

pd.set_option('max_colwidth', 100)
# temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/基本面+技术指标.xls')
temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/截取数据重要性90%2.xls')
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


from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
rf0 = RandomForestRegressor(random_state=0)
rf0.fit(X_train, y_train)
y_predict0 = rf0.predict(X_test)
error0 = mean_absolute_error(y_test, y_predict0)
error0_ = mean_absolute_percentage_error(y_test, y_predict0)
print("error0 = ",error0, "error0 percentage = ", error0_)

importances = list(rf0.feature_importances_)

feature_importances = [(feature, round(importance, 4)) for feature, importance in zip(features, importances)]
# print(feature_importances)
feature_importances = sorted(feature_importances, key = lambda x : x[1], reverse=True)


from sklearn.model_selection import GridSearchCV

#{'n_estimators': 1400, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'max_depth': 10, 'bootstrap': False}

param_grid = {
    # 'bootstrap':[True], # 是否对样本集急性有放回抽样来构建树
    'max_depth': [10, 11, 12],  # 决策树最大深度
    'max_features':['auto', 'sqrt'], # 构建决策树最优模型时考虑的最大特征数，默认是'auto'，表示最大特征数是N的平方根
    'min_samples_leaf': [1, 2, 3, 4],  # 叶子结点最小样本数
    'min_samples_split': [2, 3, 4, 5],  # 内部结点再划分所需最小样本数
    'n_estimators': [1000, 1100]  # 弱学习器的个数，可以扩大一下

}

grid_search_rf = GridSearchCV(estimator=RandomForestRegressor(random_state=0), n_jobs=-1, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3)

grid_search_rf.fit(X_train, y_train)

print(grid_search_rf.best_params_)
grid_file = open('log_GridSearchReuslt.txt', 'a')
grid_file.write(str(record_time) + '\n\t' + str(grid_search_rf.best_params_))
grid_file.close()


""""""