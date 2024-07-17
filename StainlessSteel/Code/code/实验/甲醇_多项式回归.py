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
# temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/基本面+技术指标.xls')

temp_data = temp_data.drop('日期', axis=1)

y = temp_data['期货价格']
X = temp_data.drop('期货价格', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
features = list(X_train.columns)

poly = PolynomialFeatures(degree=2).fit(X_train, y_train)
# print(poly.get_feature_names(X_train.columns))

X_ = poly.transform(X_train)
reg = LinearRegression().fit(X_, y_train)
coef = reg.coef_



result = [*zip(poly.get_feature_names(X_train.columns), reg.coef_)]
result.sort(key=lambda x : x[1], reverse=True)
# print(result)
print(result)
#
# print(reg.score(X_, y_train))

coeff = reg.coef_
r = reg.intercept_
X_test_ = poly.transform(X_test)
y_test_predict = []

for x_test in X_test_:
    j = 0
    # (i * k for i, k in list(zip(x_test, reg.coef_)))
    tmp = list(i * k for i, k in list(zip(x_test, reg.coef_)))
    for ele in tmp:
        j += ele
    j += reg.intercept_
    y_test_predict.append(j)

# print(y_test_predict)
# print('coef is :')
# print([round(i, 4) for i in reg.coef_])
# print('------------')

res = mean_absolute_error(y_test, y_test_predict)
# print('mean_absolute_error: ', res)
res = mean_absolute_percentage_error(y_test, y_test_predict)
mse = mean_squared_error(y_test, y_test_predict)
# print('mse is ', mse )
# print('mean_absolute_percentage_error: ', res)
# print('intercept: ', reg.intercept_)
#
#
#
# print('-----------------------------')

# t = [*zip(y_test, y_test_predict)]
# print(t)

# with open('predict_of_polynomial_technical.txt', 'w') as obj:
#     for ele in t:
#         obj.write(str(ele[0]) + ',' + str(ele[1]) + '\n')


# intercept: -4201.5684533592685
# mean_absolute_error: 24.636178050645672
# mean_absolute_percentage_error: 0.010659782431043954

# print(result)



