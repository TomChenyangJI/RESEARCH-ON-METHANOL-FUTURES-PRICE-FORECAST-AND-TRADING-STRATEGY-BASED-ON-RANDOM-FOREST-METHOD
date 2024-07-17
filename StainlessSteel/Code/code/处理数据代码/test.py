import os
import shutil
import sys

dir_list = os.listdir('~/Desktop/论文研究/不锈钢/数据/格式化数据')
print(dir_list)
for i in dir_list:
    print(os.path.isfile('~/Desktop/论文研究/不锈钢/数据/格式化数据/' + i))
