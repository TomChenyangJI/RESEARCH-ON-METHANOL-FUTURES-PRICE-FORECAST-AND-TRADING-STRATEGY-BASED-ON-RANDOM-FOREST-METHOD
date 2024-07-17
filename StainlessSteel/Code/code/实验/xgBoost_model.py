from xgboost import XGBRegressor as XGBR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.linear_model import LinearRegression as LinearR
from sklearn.datasets import load_boston
from sklearn.model_selection import KFold, cross_val_score as CVS, train_test_split as TTS
from sklearn.metrics import mean_squared_error as MSE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time
import datetime
import time


data = load_boston()

pd.set_option('max_colwidth', 100)
temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据.xls')
# temp_data = pd.read_excel('./汇总后的数据.xls')
# temp_data = pd.read_excel('../../文件/新的汇总后的数据（添加基建数据）.xls')


temp_data = temp_data.drop('日期', axis=1)
# temp_data = temp_data.drop('进出口焦煤', axis=1)
from sklearn.model_selection import train_test_split
y = temp_data['期货价格']
X = temp_data.drop('期货价格', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
features = list(X_train.columns)

reg = XGBR(n_estimators=100).fit(X_train, y_train)
reg.predict(X_test)
score = reg.score(X_test, y_test)
print('score is : ', score)
mse = MSE(y_test, reg.predict(X_test))
print('mse is : ', mse)
importances = reg.feature_importances_
print('importances are : ', importances)

# 交叉验证
reg = XGBR(n_estimators=100)
cv_mean = CVS(reg, X_train, y_train, cv=5).mean()
cv_mean_scoring = CVS(X_train, y_train, cv=5, scoring='neg_mean_squared_error').mean()

# 来查看一下sklearn中所有的模型评估指标
import sklearn
sorted(sklearn.metrics.SCORERS.keys())

# 开启参数silent：在数据巨大，预料到算法运行会非常缓慢的时候可以用这个参数来监控模型的训练进度
reg = XGBR(n_estimators=10, silent=False)
silent_mean = CVS(reg, X_train, y_train, scoring='neg_mean_squared_error').mean()

cv = 5
axisx = range(10, 1010, 50)
rs = []
var = []
ge = []
for i in axisx:
    reg = XGBR(n_estimators=i, random_state=420)
    cvresult = CVS(reg, X_train, y_train, cv=cv)
    rs.append(cvresult.mean())#记录1-偏差
    var.append(cvresult.var())#记录方差
    ge.append((1 - cvresult.mean())**2 + cvresult.var())#计算泛化误差的可控部分


print(axisx[rs.index(max(rs))], max(rs), var[rs.index(max(rs))])
print(axisx[var.index(min(var))],rs[var.index(min(var))],min(var))
print(axisx[ge.index(min(ge))], rs[ge.index(min(ge))], var[ge.index(min(ge))],min(ge))
plt.figure(figsize=(20, 5))
plt.plot(axisx, rs, c='black', label='XGB')
plt.plot(axisx, rs+var, c='red', linestyle='-.')
plt.plot(axisx, rs-var, c='red', linestyle='-.')
plt.legend()
plt.show()

# 看看泛化误差的可控部分如何
plt.figure(figsize=(20, 5))
plt.plot(axisx, ge, c='gray', linestyle='-.')
plt.show()

# 9.检测模型效果
# 就是计算时间

