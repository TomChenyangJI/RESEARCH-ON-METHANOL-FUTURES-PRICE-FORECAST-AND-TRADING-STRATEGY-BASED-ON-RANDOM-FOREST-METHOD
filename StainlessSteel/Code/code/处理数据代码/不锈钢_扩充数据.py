from 可调用函数模块 import month_generation, getData, makeDir
import os
import xlwt
import xlrd
from 可调用函数模块2 import get_dir, get_files

base_path = '~/Desktop/论文研究/不锈钢/数据/格式化数据'

# dir_li = os.listdir(base_path)

# def get_dir(base_path):
#     dir_li = os.listdir(base_path)
#     result = []
#     for ele in dir_li:
#         if (os.path.isfile(base_path + '/' + ele)):
#             pass
#         else:
#             result.append(base_path + '/' + ele)
#     return result

dir_li = get_dir(base_path)
dir_li.remove('~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据')


def output_data(data, path):
    """

    :param data: 字典类型的数据
    :param path: 数据要保存的绝对地址
    :return: None
    """
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet01')
    sheet.write(0, 0, '日期')
    sheet.write(0, 1, '值')
    i = 0
    for key in list(data.keys()):
        i += 1
        sheet.write(i, 0, key)
        sheet.write(i, 1, data[key])
    book.save(path)

def convert_data(path):
    """
    此函数是将文件夹path中的Excel文件中的月数据转换为日数据，并且保存到扩充数据文件夹目录（save_path）下
    :param path: 文件夹绝对路径
    :return: None
    """
    im_file_li = get_files(path)
    for file in im_file_li:
        # print(file)
        data = getData(file, 1)
        for key in list(data.keys()):
            val = data[key]
            data.pop(key)
            try:
                data[str(int(key))] = val.strip()
            except:
                data[str(int(key))] = val
        data = month_generation(data, 30)
        inner_dir = path.split('/')[-1]
        # print(path)
        # print(inner_dir)
        filename = file.split('/')[-1]
        save_path = '~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/' + inner_dir
        makeDir(save_path)
        save_name = save_path + '/' + filename
        save_name = save_name.replace('xlsx', 'xls')
        output_data(data, save_name)




# 进出口   的数据要进行扩充
im_path = '~/Desktop/论文研究/不锈钢/数据/格式化数据/进出口'
convert_data(im_path)
# 开工率
rate_path = '~/Desktop/论文研究/不锈钢/数据/格式化数据/开工率'
convert_data(rate_path)
# 现货价格 房地产
real_estate = '~/Desktop/论文研究/不锈钢/数据/格式化数据/现货价格/钢联数据_百城价格指数：样本均价：中国（月）_2021-6-5_1622894115897.xls'
data = getData(real_estate, 1)
for key in list(data.keys()):
    val = data[key]
    data.pop(key)
    try:
        data[str(int(key))] = val.strip()
    except:
        data[str(int(key))] = val
data = month_generation(data, 30)
inner_dir = real_estate.split('/')[-1]
# print(path)
# print(inner_dir)
filename = real_estate.split('/')[-1]
save_path = '~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/' + inner_dir
makeDir(save_path)
save_name = save_path + '/' + filename
save_name = save_name.replace('xlsx', 'xls')
output_data(data, save_name)
# 库存
inventory_path = '~/Desktop/论文研究/不锈钢/数据/格式化数据/库存'
convert_data(inventory_path)
# 毛利 镍 季
grossprofit_nie = '~/Desktop/论文研究/不锈钢/数据/格式化数据/毛利/钢联数据_镍：营业净收入：全球：淡水河谷（季）_2021-6-5_1622901906311.xls'
data = getData(grossprofit_nie, 1)
for key in list(data.keys()):
    val = data[key]
    data.pop(key)
    try:
        data[str(int(key))] = val.strip()
    except:
        data[str(int(key))] = val
data = month_generation(data, 30)
inner_dir = grossprofit_nie.split('/')[-1]
# print(path)
# print(inner_dir)
filename = grossprofit_nie.split('/')[-1]
save_path = '~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/' + inner_dir
makeDir(save_path)
save_name = save_path + '/' + filename
save_name = save_name.replace('xlsx', 'xls')
output_data(data, save_name)





