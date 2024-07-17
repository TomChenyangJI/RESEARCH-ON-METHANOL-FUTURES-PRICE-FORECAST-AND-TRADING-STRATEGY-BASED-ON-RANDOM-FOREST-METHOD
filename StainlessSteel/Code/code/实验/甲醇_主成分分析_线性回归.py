# 没有办法使用线性模型来拟合数据，也就是说线性回归模型是不适用的


import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures



pd.set_option('max_colwidth', 100)
temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据.xls')
# temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/甲醇毛利和现货价格.xlsx')

temp_data = temp_data.drop('日期', axis=1)

from sklearn.model_selection import train_test_split
y = temp_data['期货价格']
X = temp_data.drop('期货价格', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
features = list(X_train.columns)

# # 接下来要处理的是线性回归模型
from sklearn.linear_model import LinearRegression

linear = LinearRegression()
linear.fit(X_train, y_train)
# print('testing ... ', list(linear.coef_))
#
# print('score', linear.score(X_test, y_test))
result = linear.predict(X_test)
tmp = linear.coef_.tolist()
tmp = [(i, j) for i, j in list(zip(features, tmp))]
tmp.sort(key=lambda x : x[1])
t = mean_absolute_percentage_error(y_test, result)
print('mean_absolute_percentage_error: ', t)
t = mean_absolute_error(y_test, result)
print('mean_absolute_error: ', t)
print('score:', linear.score(X_test, y_test))
print('intercept', linear.intercept_)

# 直接使用线性回归的方式来处理数据后得出的回归系数是：
# [('冰醋酸库存', -1.484647983207737), ('rsi', -1.474418199538441), ('wr', -1.2123943972994737), ('冰醋酸进口', -0.698359783612685), ('psy', -0.3773423745035731), ('冰醋酸毛利', -0.07339114809053257), ('冰醋酸出口量', -0.059054665862197674), ('甲醇现货价格', -0.01380561960830304), ('天然气现货价格', -0.002294877433187035), ('甲醇进口', -7.168017235185988e-06), ('obv', 1.9208531622585956e-06), ('天然气进口', 3.8033906973014136e-06), ('甲醇产量', 5.3371077430150636e-06), ('天然气库存', 1.6354878102765054e-05), ('甲醇出口', 0.00012967113357385682), ('天然气产量', 0.0014499389392916928), ('甲醇库存', 0.005016895806775771), ('冰醋酸消费量', 0.015181867980304985), ('甲醇毛利', 0.020805102474239293), ('冰醋酸现货价格', 0.05660478068348564), ('kdj', 0.38561251130796376), ('macd_dea', 0.4820889231083818), ('期货价格偏移', 0.9271983056486706)]
# intercept: 173.53399215216587
# mean_absolute_error: 23.92261610386596
# mean_absolute_percentage_error: 0.010308835793504481


from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_error
# print(mean_absolute_percentage_error(result, y_test))



# amount = 15
from sklearn.decomposition import PCA
pca = PCA(n_components=0.95)

X_p = pca.fit(X_train).transform(X_train)
# print(X_train)
# print(X_p)
linear = LinearRegression()
linear.fit(X_p, y_train)
print( ' intercept ',linear.intercept_)
# print(' coef_ {:.7f} '.format(float(linear.coef_)))
coef = linear.coef_
print('coef: ', coef)
print('intercept: ', linear.intercept_)
result = linear.predict(pca.fit(X_test).transform(X_test))
# print("result : ", result)
print("mean_absolute_error: ", mean_absolute_error(y_test, result))
print("mean_absolute_percentage_error: ", mean_absolute_percentage_error(y_test, result))


# intercept: 2373.434935521688
# coef: -2.31692227e-05
# mean_absolute_error: 238.66465269545603
# mean_absolute_percentage_error: 0.10253203889240771



# linear.predict()
# print(pca.explained_variance_ratio_)

# # 现在需要将实验的结果记录到日志文件中 log_PCAExperimentResult.txt
#
# # 接下来要处理的是线性回归模型
from sklearn.linear_model import LinearRegression
# #
model = LinearRegression()
model.fit(X_p, y_train)
a = model.intercept_
coeff = model.coef_
# print(coeff)
# print(np.dot(X_test, pca.get_covariance()))
input_predict = [[i[-1]] for i in np.dot(X_test, pca.get_covariance())]
# print(len(np.dot(X_test, pca.get_covariance())[0]))
# print(input_predict)
# result = model.fit(pca.fit(X_test).transform(X_test), y_test)
result = model.predict(X_p)
# print(list((i - j) for i, j in list(zip(result, y_train))))
# print(zip(result, y_train))
# print(result)
#
# model.fit(X_train, y_train)
# coeff = model.coef_
# intercept = model.intercept_
# #
# pred = model.predict(X_test)
# print(np.mean((pred - y_test) ** 2))
# # result = model.predict(X_test)
# # print(result)
# # print(intercept)
# from sklearn.metrics import mean_squared_error
# # print(mean_squared_error(result, y_test))
#
#
# # convert_dataset = [list(i[:amount]) for i in np.dot(X_test, pca.get_covariance())]
# # result = model.predict(convert_dataset)
# # from sklearn.metrics import mean_absolute_percentage_error
# # print(mean_absolute_percentage_error(result, y_test))
# # print('残差平方和:{:.2f}'.format(np.mean((model.predict(convert_dataset) - y_test) ** 2)))
#
# # # print(convert_dataset)
# # print('score = ', model.score(convert_dataset, y_test))
# #
# # from sklearn.metrics import mean_squared_error
# # from sklearn.metrics import mean_absolute_percentage_error
# # predict = np.dot(convert_dataset, coeff)
# # error = mean_squared_error(predict, y_test)
# # error_precentage = mean_absolute_percentage_error(predict, y_test)
# # # print(error_precentage)
# #
# # # log_file_experiment = open('log_PCAExperimentResult.txt', 'a')
# # # record_time = time.ctime(time.time())
# # # log_file_experiment.write('\n' + str(record_time) + "\n")
# # # log_file_experiment.write(('error = ' + str(error)) + 'error percentage = ' + str(error_precentage) + '\n')
# # # log_file_experiment.close()
