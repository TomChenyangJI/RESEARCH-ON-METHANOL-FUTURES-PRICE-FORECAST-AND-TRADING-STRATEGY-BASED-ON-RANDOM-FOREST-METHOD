from sklearn import datasets # 其实就是生成的一些数据集
wine = datasets.load_wine()
X = wine.data  # 一共有13个特征

y = wine.target # 这个y是类
target_names = wine.target_names

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_p = pca.fit(X).transform(X)
# print(X.shape)
# print(X_p.shape)
# print(pca.explained_variance_ratio_)

# 提取主成分，进行线性回归，使用回归模型来预测测试集  这是第一个对照试验


