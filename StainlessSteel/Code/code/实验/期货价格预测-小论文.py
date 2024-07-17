import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt



pd.set_option('max_colwidth', 100)
# temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据归一化.xls')
temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/截取数据重要性90%2.xls')
# temp_data = pd.read_excel('~/Desktop/论文研究/甲醇/基本面+技术指标.xls')
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
# print(importances)
# print(len(importances), len(features))

feature_importances = [(feature, round(importance, 4)) for feature, importance in zip(features, importances)]
# print(feature_importances)
feature_importances = sorted(feature_importances, key = lambda x : x[1], reverse=True)


#{'n_estimators': 1400, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'max_depth': 10, 'bootstrap': False}



"""
from sklearn.model_selection import GridSearchCV

param_grid = {
    # 'bootstrap':[True], # 是否对样本集急性有放回抽样来构建树
    'max_depth': [5, 10, 15, 20],  # 决策树最大深度
    # 'max_features':['auto'], # 构建决策树最优模型时考虑的最大特征数，默认是'auto'，表示最大特征数是N的平方根
    'min_samples_leaf': [1, 2, 3, 5, 10, 15],  # 叶子结点最小样本数
    'min_samples_split': [3, 4, 6, 15, 20],  # 内部结点再划分所需最小样本数
    'n_estimators': [1400, 1200, 1600]  # 弱学习器的个数，可以扩大一下
}

grid_search_rf = GridSearchCV(estimator=RandomForestRegressor(random_state=0), n_jobs=-1, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3)

grid_search_rf.fit(X_train, y_train)

print(grid_search_rf.best_params_)
grid_file = open('log_GridSearchReuslt.txt', 'a')
grid_file.write(str(record_time) + '\n\t' + str(grid_search_rf.best_params_))
grid_file.close()


"""
# print(rf0.get_params())

# {'n_estimators': 1400, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'max_depth': 10, 'bootstrap': False}
# print(rf0.estimator_params)

#{'max_depth': 25, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 1300}


# Fri Jul  2 20:12:21 2021
# 	{'max_depth': 12, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 1600}
# Fri Jul  2 20:12:25 2021
# 	{'max_depth': 12, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 1300}
# Fri Jul  2 20:12:30 2021
# 	{'max_depth': 12, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 1400}

bootstrap_ = True
max_depth_=12,
max_features_='sqrt'
min_samples_leaf_= 1
min_samples_split_=2
n_estimators_=700
rf1 = RandomForestRegressor(bootstrap=True,
                            max_depth=12,
                            max_features='sqrt',
                            min_samples_leaf= 1,
                            min_samples_split=2,
                            n_estimators=700)

head = list(X_train.columns)
print('r0 score is ', rf0.score(X_test, y_test))
rf1.fit(X_train, y_train)
print('score is ', rf1.score(X_test, y_test))
y_predict1 = rf1.predict(X_test)
error1 = mean_absolute_error(y_test, y_predict1)
error1_ = mean_absolute_percentage_error(y_test, y_predict1)
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_predict1)
from sklearn.metrics import mean_absolute_error
print('mae is ', mean_absolute_error(y_test, y_predict1))
print('mse is ', mse )
print("调参后，平均绝对误差为：",error1, " percentage = ", error1_)

importances1 = list(rf1.feature_importances_)

feature_importances1 = [(feature, round(importance, 4)) for feature, importance in zip(features, importances1)]
# print(feature_importances)
feature_importances1 = sorted(feature_importances1, key = lambda x : x[1], reverse=True)
print(feature_importances1)

# 将实验的结果记录到日志文件中
log_file_experiment = open('log_ResultOfExperiments.txt', 'a')
log_file_experiment.write('\n' + str(record_time) + "\n")
log_file_experiment.write('default result :\n' + str(feature_importances) + '\n')
log_file_experiment.write('\tmean absolute error : '+ str(error0)+' mean_absolute_percentage_error :' + str(error0_) + '\n')
log_file_experiment.write('after adaption :\n' + str(feature_importances1) + '\n')
log_file_experiment.write(f"\tparameters : bootstrap={bootstrap_} max_depth={max_depth_} max_features={max_features_} "
                          f"min_samples_leaf={min_samples_leaf_} "
                          f"min_samples_split={min_samples_split_} n_estimators={n_estimators_}\n")
log_file_experiment.write('mean squared absolute error : '+ str(error1) +' mean_absolute_percentage_error :' + str(error1_) + '\nscore is ' + str(rf1.score(X_test, y_test)) + '\noriginal score is ' +  str(rf0.score(X_test, y_test)) + '\n')
log_file_experiment.close()
''''''
# print('result', rf1.feature_importances_)
# print(head)
# importance = rf1.feature_importances_
# for i in range(len(head)):
#     print(head[i], importance[i])
# result = pd.DataFrame(y_test)
# result['y_predict0'] = y_predict0
# result['y_predict1'] = y_predict1
# print(result.head(10))




'''
from sklearn.model_selection import RandomizedSearchCV

param_dist = {
'n_estimators':range(80,200,4),
        'max_depth':range(2,15,1),
        'learning_rate':np.linspace(0.01,2,20),
        'subsample':np.linspace(0.7,0.9,20),
        'colsample_bytree':np.linspace(0.5,0.98,10),
        'min_child_weight':range(1,9,1)
}



file_path = './best_params_record.txt'
file_obj = open(file_path, 'a')

rf = RandomForestRegressor()
n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num =10)]
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
max_depth = [5, 8, 10]
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
# print(random_model)
# print(random_model.fit(X_train, y_train))
random_model.fit(X_train, y_train)
# predictions = random_model.predict(X_test)
# err = mean_absolute_error(predictions, y_test)
# print(random_model.best_params_)
# print('err is ', err)
file_obj.write(str(record_time) + "\n" + str(random_model.best_params_) + '\n')
file_obj.close()
""""""

# 预测完成之后要看一下数据的可靠性

'''

print(y_predict1)

