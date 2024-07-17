from sklearn.model_selection import RandomizedSearchCV
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error

pd.set_option('max_colwidth', 100)
# temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据归一化.xls')
temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据.xls')
# temp_data = pd.read_excel('./汇总后的数据.xls')
# temp_data = pd.read_excel('../../文件/新的汇总后的数据（添加基建数据）.xls')

record_time = time.ctime(time.time())

temp_data = temp_data.drop('日期', axis=1)
from sklearn.model_selection import train_test_split
y = temp_data['期货价格']
X = temp_data.drop('期货价格', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

param_dist = {
'n_estimators':range(80,200,4),
        'max_depth':range(2,15,1),
        'learning_rate':np.linspace(0.01,2,20),
        'subsample':np.linspace(0.7,0.9,20),
        'colsample_bytree':np.linspace(0.5,0.98,10),
        'min_child_weight':range(1,9,1)
}



file_path = './log_RandomSearchResult.txt'
file_obj = open(file_path, 'a')

rf = RandomForestRegressor()
n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num =10)]
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
max_depth = [4, 5, 8, 10]
max_features = ['auto', 'sqrt']
bootstrap = [True, False]
random_params_group = {'n_estimators':n_estimators,
                       'min_samples_split':min_samples_split,
                       'min_samples_leaf':min_samples_leaf,
                       'max_depth':max_depth,
                       'max_features':max_features,
                       'bootstrap':bootstrap}
random_model = RandomizedSearchCV(rf, param_distributions=random_params_group, n_iter=100,
                                  scoring='neg_mean_squared_error', verbose=2, n_jobs=-1,cv=3, random_state=0)
random_model.fit(X_train, y_train)
file_obj.write(str(record_time) + "\n" + str(random_model.best_params_) + '\n')
file_obj.close()