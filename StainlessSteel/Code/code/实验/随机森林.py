import pandas as pd
import numpy as np

# 导入数据
dataset = pd.read_csv("~/Desktop/论文研究/甲醇/基本面+技术指标.xls")

# 输出数据预览
# print(dataset.head())

# 准备训练数据
# 自变量：汽油税、人均收入、告诉公路、人口所占比例
# 因变量：汽油消耗量
X = dataset.iloc[:, 0:4].values
y = dataset.iloc[:, 4].values

# 将数据分为训练集和测试集
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 特征缩放，通常没有必要
# 因为数据单位，自变量数值范围差距巨大，不缩放也没问题
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# 训练随机森林解决回归问题
from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators=200, random_state=0)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)

# 评估回归性能
from sklearn import metrics

print("Mean Absolute Error: ", metrics.mean_absolute_error(y_test, y_pred))
print("Mean Squared Error: ", metrics.mean_squared_error(y_test, y_pred))
print("Root Mean Squared Error:", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

