import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt



pd.set_option('max_colwidth', 100)
temp_data = pd.read_excel('~/desktop/论文研究/甲醇/汇总后的数据/汇总后的数据.xls')
record_time = time.ctime(time.time())
date_col = temp_data['日期']
temp_data = temp_data.drop('日期', axis=1)
from sklearn.model_selection import train_test_split
y = temp_data['期货价格']
X = temp_data.drop('期货价格', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
features = list(X_train.columns)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error


bootstrap_ = True
max_depth_=12
max_features_='sqrt'
min_samples_leaf_= 1
min_samples_split_=2
n_estimators_=900


rf1 = RandomForestRegressor(bootstrap=True,
                            max_depth=10,
                            max_features='sqrt',
                            min_samples_leaf= 1,
                            min_samples_split=2,
                            n_estimators=900)

head = list(X_train.columns)
rf1.fit(X_train, y_train)
y_predict1 = rf1.predict(X)

y_predict1 = y_predict1.tolist()
date_col = date_col.tolist()
X = np.array(X).tolist()
y = y.tolist()
import xlwt
book = xlwt.Workbook()
sheet = book.add_sheet('sheet01')

for i in range(len(X)):
    tmp = [date_col[i],y_predict1[i]]
    for col in range(len(tmp)):
        sheet.write(i, col, tmp[col])
book.save('~/Desktop/论文研究/甲醇/交易策略数据/期货价格预测值.xls')

import 合并大智慧期货数据和价格预测值