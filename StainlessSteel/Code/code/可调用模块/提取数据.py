"""
            螺纹钢                    焦炭                       焦煤                          铁矿石
期货价格     现货价格                   现货价格                     现货价格                    现货价格
            期货价格                   期货价格                     期货价格                    期货价格
            开工率                     开工率                       开工率                     开工率
            毛利                      毛利                          毛利                      毛利
            进出口                    进出口                                                进出口
                                     库存                          库存                      库存
"""

from 可调用函数模块 import *

# 命名的规范
# 现货 spot
# 库存 inventory
# 进出口 im_ex
# 开工率 op_rate
# 毛利profit
# 期货价格 future_price
# 品种名 steel螺纹钢 coal焦炭 ore铁矿石 coking焦煤

# 获取 期货价格 日数据
future_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/期货数据/铁矿石期货-大智慧.xlsx', 4],
    '焦煤': ['~/Desktop/ 小论文/数据/期货数据/焦煤期货-大智慧.xlsx', 4],
    '焦炭': ['~/Desktop/ 小论文/数据/期货数据/焦炭期货-大智慧.xlsx', 4],
    '螺纹钢': ['~/Desktop/ 小论文/数据/期货数据/螺纹钢期货-大智慧.xlsx', 4]
}

# 技术指标 日数据

# 获取 现货价格 日数据
spot_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_铁矿石_澳.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_炼焦煤.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_焦炭.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_螺纹钢.xls', 2]
}

# 获取 开工率 月数据好像 周 半月数据
rate_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_铁矿石_国产矿山开工率.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_焦煤_山西大同煤矿开工率.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_焦炭_焦炭中国周度开工率.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_螺纹钢_建筑钢材产线开工率.xls', 2]
}

# 获取 毛利 日数据
profit_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_铁矿石_唐山地区钢坯利润.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_焦煤_炼焦煤毛利.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_焦炭_山西焦炭毛利.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_螺纹钢_螺纹钢毛利.xls', 2]
}

# 获取 进出口 月数据
im_ex_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_铁矿石_铁矿：进口数量合计：全球—中国（月）.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_焦煤_进口炼焦煤：港口库存合计（周）.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_焦炭_焦炭：进口数量合计：省市：中国（月）.xls', 2],
# 这个数据是直接不要了的我记得
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_螺纹钢_螺纹钢：出口数量：中国（月）.xls', 2]
}

# 获取 库存 周
inventory_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_卓_铁矿石_澳矿库存情况.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_焦煤_炼焦煤：110家钢铁企业：库存：中国（周）.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_焦炭_焦炭：110家钢铁企业：库存（周）.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_螺纹钢_螺纹钢：建筑钢材钢铁企业：库存：中国（周）.xls', 2]
}

# 字典中品种的顺序是：铁矿石 焦煤 焦炭 螺纹钢


# 是否需要将期货数据的日期格式修改为'20210524'

# 来想一下接下来的一步工作是什么
# 提取错开的月数据或者是周数据，然后将它们补充为日数据，然后进行所有数据的匹配
#
# 看一下哪些数据是不要的
# 焦炭的进出口 螺纹钢的库存不要

# 周数据 和 月数据

# 库存 --------------------------------------------------------
# 1.周数据
#焦炭
amount = 30
inve_coal = month_generation(getData(inventory_path['焦炭'][0], inventory_path['焦炭'][1]), amount)
#铁矿石
inve_ore = month_generation(getData(inventory_path['铁矿石'][0], inventory_path['铁矿石'][1]), amount)
#焦煤
inve_coking = month_generation(getData(inventory_path['焦煤'][0], inventory_path['焦煤'][1]), amount)


# 开工率 --------------------------------------------------------
# 2.月数据
# 开工率
# 铁矿石
rate_ore = month_generation(getData(rate_path['铁矿石'][0], rate_path['铁矿石'][1]), amount)
# 焦煤
rate_coking = month_generation(getData(rate_path['焦煤'][0], rate_path['焦煤'][1]), amount)
# 焦炭
rate_coal = month_generation(getData(rate_path['焦炭'][0], rate_path['焦炭'][1]), amount)
# 螺纹钢
rate_steel = month_generation(getData(rate_path['螺纹钢'][0], rate_path['螺纹钢'][1]), amount)


# 进出口 --------------------------------------------------------
# 月数据
# 铁矿石
im_ex_ore = month_generation(getData(im_ex_path['铁矿石'][0], im_ex_path['铁矿石'][1]), amount)
# 焦煤
im_ex_coking = month_generation(getData(im_ex_path['焦煤'][0], im_ex_path['焦煤'][1]), amount)
# 焦炭
im_ex_coal = month_generation(getData(im_ex_path['焦炭'][0], im_ex_path['焦炭'][1]), amount)
# 螺纹钢
im_ex_steel = month_generation(getData(im_ex_path['螺纹钢'][0], im_ex_path['螺纹钢'][1]), amount)

# 毛利 --------------------------------------------------------
# 铁矿石
profit_ore = month_generation(getData(profit_path['铁矿石'][0], profit_path['铁矿石'][1]), amount)
# 焦煤
profit_coking = month_generation(getData(profit_path['焦煤'][0], profit_path['焦煤'][1]), amount)
# 焦炭
profit_coal = month_generation(getData(profit_path['焦炭'][0], profit_path['焦炭'][1]), amount)
# 螺纹钢
profit_steel = month_generation(getData(profit_path['螺纹钢'][0], profit_path['螺纹钢'][1]), amount)

# 期货 --------------------------------------------------------
# 铁矿石
future_ore = getFutureData(future_path['铁矿石'][0], future_path['铁矿石'][1])
# 焦煤
future_coking = getFutureData(future_path['焦煤'][0], future_path['焦煤'][1])
# 焦炭
future_coal = getFutureData(future_path['焦炭'][0], future_path['焦炭'][1])
# 螺纹钢
future_steel = getFutureData(future_path['螺纹钢'][0], future_path['螺纹钢'][1])

# 现货 --------------------------------------------------------
# 铁矿石
spot_ore = getData(spot_path['铁矿石'][0], spot_path['铁矿石'][1])
# 焦煤
spot_coking = getData(spot_path['焦煤'][0], spot_path['焦煤'][1])
# 焦炭
spot_coal = getData(spot_path['焦炭'][0], spot_path['焦炭'][1])
# 螺纹钢
spot_steel = getData(spot_path['螺纹钢'][0], spot_path['螺纹钢'][1])


# 技术指标的数据还没有获得


# 这个时候就获取到了所有的数据了
# 接下来就要整合所有的数据了

def matchData(data, name):
    """
    将字典data中的数据添加到字典中original_dict
    :param original_dict: 是一个字典，key是日期，格式为'20210524'，val是列表，格式为列表[, , , ...]，列表中的元素是一个特征值
    :param data: 是一个特征数据集，其格式为字典，该字典的key为日期，格式为'20210524'，val是值
    :param name: 要添加的特征值的名称
    :return: 将新特征添加到original_dict之后返回
    """
    global head  # head: 用来记录目前original_dict中的val列表中数据对应的特征名称
    global original_dict # original_dict: 是一个字典，key是日期，格式为'20210524'，val是列表，格式为列表[, , , ...]，列表中的元素是一个特征值 # {'20210524':[, , , ...]}
    data_keys = list(data.keys())
    head.append(name)
    for key in list(original_dict.keys()):
        if key in data_keys:
            original_dict[key].append(data[key])
        else:
            original_dict.pop(key)

def create_original_dict(future_data):
    original_dict = {}
    for key in list(future_data.keys()):
        val = [future_data[key]]
        original_dict[key] = val
    return original_dict




head = []
original_dict = create_original_dict(future_steel)
head.append('期货螺纹钢')

# 期货
matchData(future_ore, '期货铁矿石')
matchData(future_coal, '期货焦炭')
# matchData(future_steel, '期货螺纹钢')
# 现货
matchData(spot_ore, '现货铁矿石')
matchData(spot_coal, '现货焦炭')
matchData(spot_steel, '现货螺纹钢')
# 库存
matchData(inve_ore, '库存铁矿石')
matchData(inve_coal, '库存焦炭')
# matchData(inve_steel, '库存螺纹钢') 这个数据是不相关的，所以就没有这个数据
# 毛利
matchData(profit_ore, '毛利铁矿石')
matchData(profit_coal, '毛利焦炭')
matchData(profit_steel, '毛利螺纹钢')
# 开工率
matchData(rate_ore, '开工率铁矿石')
matchData(rate_coal, '开工率焦炭')
matchData(rate_steel, '开工率螺纹钢')
# 进出口
matchData(im_ex_ore, '进出口铁矿石')
# matchData(im_ex_coal, '进出口焦炭') # 这个数据是不要的，因为不相关
matchData(im_ex_steel, '进出口螺纹钢')

# 处理基建方向的数据
real_estate_path = '~/Desktop/ 小论文/补充下载/基建投资同比增长率.xlsx'
real_estate = getData(real_estate_path, 1)
for key in list(real_estate.keys()):
    val = real_estate[key]
    real_estate.pop(key)
    real_estate[str(int(key))] = val

real_estate = real_estate

real_estate = month_generation(real_estate, amount)

matchData(real_estate, '基建')

# print(original_dict)
# print(head)
# print(len(list(original_dict.keys())))


# matchData(future_coking, '期货焦煤')
# matchData(spot_coking, '现货焦煤')
# matchData(inve_coking, '库存焦煤')
# matchData(profit_coking, '毛利焦煤')
# matchData(rate_coking, '开工率焦煤')
# matchData(im_ex_coking, '进出口焦煤')


# 将匹配后的所有数据进行写入文件
import xlwt

book = xlwt.Workbook()
sheet = book.add_sheet('sheet01')
sheet.write(0, 0, '日期')
for i in range(len(head)):
    sheet.write(0, i + 1, head[i])

row = 1
for key in list(original_dict.keys()):
    sheet.write(row, 0, key)
    col = 1
    val_li = original_dict[key]
    for val in val_li:
        sheet.write(row, col, val_li[col - 1])
        col += 1
    row += 1


book.save('../文件/新的汇总后的数据（添加基建数据）.xls')
""""""



'''

result = getFutureData(future_path['螺纹钢'][0], future_path['螺纹钢'][1])
print(result)

import xlwt
book = xlwt.Workbook('')
sheet = book.add_sheet('sheet01')
sheet.write(0, 0, '日期')
sheet.write(0, 1, '期货价格')
i = 0
for key in list(result.keys()):
    i += 1
    sheet.write(i, 0, key)
    sheet.write(i, 1, result[key])
book.save('../文件/日期格式规范化期货价格.xls')
'''