import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('max_colwidth', 100)
temp_data = pd.read_csv('temp_data.csv')

print(temp_data.shape)

# print(temp_data.head())

# print(temp_data.info())
# print(temp_data.describe())
# print(temp_data.head())
# 处理日期数据
temp_data['dates'] = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) for year, month, day in zip(temp_data['year'], temp_data['month'], temp_data['day'])]
temp_data['dates'] = pd.to_datetime(temp_data['dates'])
# print(temp_data.head())
# fig = plt.figure(figsize=(8, 4))
# plt.plot(temp_data['dates'], temp_data['temp'], c = 'red', label='temp')
# plt.plot(temp_data['dates'], temp_data['average'], c = 'blue', label='average')
# plt.legend(loc = 'best')
# plt.show()
# plt.close(fig)

# # 随着时间其他特征的变化
# fig = plt.figure(figsize=(8, 15))
# ax1 = plt.subplot(311)
# ax1.plot(temp_data['dates'], temp_data['ws_1'], c = 'red')
# ax1.set_xlabel('')
# ax1.set_ylabel('Wind Speed')
# ax1.set_title('Yesterday\'s wind speed')
# # 降水
# ax2 = plt.subplot(312)
# ax2.plot(temp_data['dates'], temp_data['prcp_1'], c='blue')
# ax2.set_xlabel('')
# ax2.set_ylabel('Precipitation')
# ax2.set_title('Yesterday\'s Precipitation')
# # 积雪
# ax3 = plt.subplot(313)
# ax3.plot(temp_data['dates'], temp_data['snwd_1'], 'ro')
# ax3.set_xlabel('Date')
# ax3.set_ylabel('Snow Depth')
# ax3.set_title("Yesterday's Snow Depth")
# plt.show()
# plt.close(fig)

# 加入昨天和前天的气温作为新的特征
temp_data['1day_ago_temp'] = temp_data['temp'].shift(1)
temp_data['2days_ago_temp'] = temp_data['temp'].shift(2)
# print(temp_data.head())
temp_data = temp_data.dropna()

# 创建季节特征
seasons = []
for month in temp_data['month']:
    if month in [3, 4, 5]:
        seasons.append('Spring')
    elif month in [6, 7, 8]:
        seasons.append('Summer')
    elif month in [9, 10, 11]:
        seasons.append('Autumn')
    elif month in [12, 1, 2]:
        seasons.append('Winter')
temp_data['season'] = seasons
# print(temp_data.head())

# 数据预处理
temp_data = temp_data.drop(['dates'], axis = 1) # 1说明的是将列drop掉，0的话就把行dorp掉
# print(temp_data.shape)

# one-hot
temp_data = pd.get_dummies(temp_data)
# print(temp_data.head())

# 划分训练集和测试集
from sklearn.model_selection import train_test_split
y = temp_data['temp']
X = temp_data.drop('temp', axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
# print(X_train.shape)
# print(y_train.shape)
# print(X_test.shape)
# print(y_test.shape)
# 所有数据准备完毕
# 存储一下目前的列名
features = list(X_train.columns)
# print(features)

# 我们先用默认参数训练
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
rf0 = RandomForestRegressor(random_state=0)
rf0.fit(X_train, y_train)
y_predict0 = rf0.predict(X_test)
error0 = mean_absolute_error(y_test, y_predict0)
# print("error 0", error0)

errors = []
errors.append(error0)

# 看一下特征重要性
importances = list(rf0.feature_importances_)
# print(importances)
# column和重要度组合起来
feature_importances = [(feature, round(importance, 4)) for feature, importance in zip(features, importances)]
# print(feature_importances)

# 排序
feature_importances = sorted(feature_importances, key = lambda x : x[1], reverse=True)
# print(feature_importances)

# print(rf0.get_params())

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

# 设置搜索参数
param_grid = {
    # 'bootstrap':[True], # 是否对样本集急性有放回抽样来构建树
    'max_depth':[5, 10], # 决策树最大深度
    # 'max_features':['auto'], # 构建决策树最优模型时考虑的最大特征数，默认是'auto'，表示最大特征数是N的平方根
    'min_samples_leaf':[3, 4, 5], # 叶子结点最小样本数
    'min_samples_split':[5, 7, 9], # 内部结点再划分所需最小样本数
    'n_estimators':[50, 200, 600] # 弱学习器的个数，可以扩大一下
}

grid_search_rf = GridSearchCV(estimator=RandomForestRegressor(random_state=0),
                              param_grid=param_grid, scoring='neg_mean_squared_error',
                              cv=5) # cv是交叉验证，为5的话就是将训练数据分为5分，选用其中的4分作为训练数据，将另外的一份作为测试数据
print(grid_search_rf.fit(X_train, y_train))
# 模型存储
print(grid_search_rf.best_params_)

rf1 = RandomForestRegressor(bootstrap=True,
                            max_depth=10,
                            max_features='auto',
                            min_samples_leaf= 5,
                            min_samples_split=5,
                            n_estimators=600)
rf1.fit(X_train, y_train)
y_predict1 = rf1.predict(X_test)
error1 = mean_absolute_error(y_test, y_predict1)
print("调参后，平均绝对误差为：",error1)

result = pd.DataFrame(y_test)
result['y_predict0'] = y_predict0
result['y_predict1'] = y_predict1
print(result.head(10))