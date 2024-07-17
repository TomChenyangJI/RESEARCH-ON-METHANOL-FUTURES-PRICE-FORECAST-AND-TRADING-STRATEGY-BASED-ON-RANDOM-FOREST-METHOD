import time
import datetime
import xlwt
from 可调用函数模块 import getData
from 可调用函数模块2 import get_next_day, day_match_month_or_week

def check_date(checking_date, data_dict):
    keys = data_dict.keys()
    if checking_date in keys:
        print('True')
    else:
        print('False')


# 冰醋酸 甲醇 天然气
# sore  jia  gas

# 产能    出口量     进口量     库存      消费量     毛利
# production   ex         im       inve      consu    profit

# 冰醋酸
# 月
sore_production = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸产能.xls'  # 这个数据其实是不用的
# 月
sore_ex = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸出口量.xls'
# 月
sore_im = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸进口量.xls'
# 周
sore_inve = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸库存天数.xls'
# 月
sore_consu = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸消费量.xls'
# 日
sore_profit = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸毛利.xls'
#日
sore_spot = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸国标低端现货价格.xls'

# 甲醇
# 月
jia_production = '~/Desktop/论文研究/甲醇/甲醇/钢联数据_甲醇：产量：中国（月）_2021-6-6_1622962155745.xls'
# 月
jia_ex = '~/Desktop/论文研究/甲醇/甲醇/钢联数据_甲醇：出口数量合计：中国—全球（月）_2021-6-6_1622962503120.xls'
# 月
jia_im = '~/Desktop/论文研究/甲醇/甲醇/钢联数据_甲醇：进口数量合计：全球—中国（月）_2021-6-6_1622962531907.xls'
# 周
jia_inve = '~/Desktop/论文研究/甲醇/甲醇/钢联数据_甲醇：社会库存：中国（周）_2021-6-6_1622962257187.xls'
# 日
jia_profit = '~/Desktop/论文研究/甲醇/甲醇/甲醇_天然气制甲醇制甲醇毛利润.xls'
# 日
jia_spot =  '~/Desktop/论文研究/甲醇/甲醇/甲醇现货价格生意社.xlsx'

# 天然气
# 周
gas_inve = '~/Desktop/论文研究/甲醇/天然气/钢联数据_EIA：液化石油气_液化天然气：库存（周）_2021-6-6_1622964301577.xls'
# 月
gas_production = '~/Desktop/论文研究/甲醇/天然气/天然气产量.xls'
# 月
gas_ex = '~/Desktop/论文研究/甲醇/天然气/天然气出口量.xls'  # 这个数据是不需要的
# 月
gas_im = '~/Desktop/论文研究/甲醇/天然气/天然气进口量.xls'
# 日
gas_spot = '~/Desktop/论文研究/甲醇/天然气/天然气现货价格生意社.xlsx'


# ----------------获取数据------------------------


# 冰醋酸
sore_production_data = getData(sore_production, 1)
sore_ex_data = getData(sore_ex, 1)
sore_im_data = getData(sore_im, 1)
sore_inve_data = getData(sore_inve, 1)
sore_consu_data = getData(sore_consu, 1)
sore_profit_data = getData(sore_profit, 1)
sore_spot_data = getData(sore_spot, 1)
# print(len(list(sore_spot_data.keys())))

# 甲醇
jia_production_data = getData(jia_production, 1)
jia_ex_data = getData(jia_ex, 1)
jia_im_data = getData(jia_im, 1)
jia_inve_data = getData(jia_inve, 1)
jia_profit_data = getData(jia_profit, 1)
jia_spot_data = getData(jia_spot, 1)

# 天然气
gas_inve_data = getData(gas_inve, 1)
gas_production_data = getData(gas_production, 1)
gas_ex_data = getData(gas_ex, 1)
gas_im_data = getData(gas_im, 1)
gas_spot_data = getData(gas_spot, 1)

# 期货价格
future_data = getData('~/Desktop/论文研究/甲醇/甲醇期货价格.xls', 1)

# ---------------------进行数据的匹配---------------------
month_count = 31
week_count = 30
# 1.首先看一下哪些数据需要匹配，然后进行匹配
# 冰醋酸 出口量 进口量 库存（周） 消费量
sore_ex_match = day_match_month_or_week(future_data, sore_ex_data, month_count)
# print(sore_ex_match)
sore_im_match = day_match_month_or_week(future_data, sore_im_data, month_count)
sore_inve_match = day_match_month_or_week(future_data, sore_inve_data, week_count)
sore_consu_match = day_match_month_or_week(future_data, sore_consu_data, month_count)

# 甲醇 产量 出口量 进口量 库存（周）
jia_production_match = day_match_month_or_week(future_data, jia_production_data, month_count)
jia_ex_match = day_match_month_or_week(future_data, jia_ex_data, month_count)
jia_im_match = day_match_month_or_week(future_data, jia_im_data, month_count)
jia_inve_match = day_match_month_or_week(future_data, jia_inve_data, week_count)

# 天然气 产量 出口量 进口量 库存（周）
gas_production_match = day_match_month_or_week(future_data, gas_production_data, month_count)
# gas_ex_match = day_match_month_or_week(future_data, gas_ex_data, month_count)  # 这里是数据出现错误的原因，因为 天然气出口 数据是不使用的
gas_im_match = day_match_month_or_week(future_data, gas_im_data, month_count)
gas_inve_match = day_match_month_or_week(future_data, gas_inve_data, week_count)

# 2.接着看一下哪些数据是不需要匹配的，然后列举出来
# 冰醋酸 现货价格 毛利
# sore_spot_data  sore_profit_data
sore_spot_match = day_match_month_or_week(sore_spot_data, sore_spot_data, 1)
sore_profit_match = day_match_month_or_week(sore_profit_data, sore_profit_data, 1)

# 甲醇 现货价格 毛利
# jia_spot_data   jia_profit_data
jia_spot_match = day_match_month_or_week(jia_spot_data, jia_spot_data, 1)
jia_profit_match = day_match_month_or_week(jia_profit_data, jia_profit_data, 1)


# 天然气 现货价格
# gas_spot_data
gas_spot_match = day_match_month_or_week(gas_spot_data, gas_spot_data, 1)

# 将1和2的数据进行匹配

head = ['期货价格', '冰醋酸出口量']
match_data = sore_ex_match
# print(match_data)

def list_data_match(list_data2, name):
    """
    将两个字典数据进行匹配，其中第二个字典的val是一个2元列表
    :param name: 需要添加的数据的名称
    :param list_data2: 第二个字典，其key是日期，val是一个2元列表
    :return: 一个字典，其key为日期，val是一个列表
    """
    global head, match_data
    list_data1 = match_data
    head.append(name)
    result = {}
    key_li1 = list(list_data1.keys())
    key_li2 = list(list_data2.keys())
    for key in key_li1:
        if key in key_li2:
            tem_li = list_data1[key]
            result[key] = tem_li + [list_data2[key][1]]
    match_data = result
    print(name, len(list(match_data.keys())))

list_data_match(sore_im_match, '冰醋酸进口')
list_data_match(sore_inve_match, '冰醋酸库存')
list_data_match(sore_consu_match, '冰醋酸消费量')
list_data_match(jia_production_match, '甲醇产量')
list_data_match(jia_ex_match, '甲醇出口')
list_data_match(jia_im_match, '甲醇进口')
list_data_match(jia_inve_match, '甲醇库存')
list_data_match(gas_production_match, '天然气产量')
# list_data_match(gas_ex_match, '天然气出口')
list_data_match(gas_im_match, '天然气进口')
list_data_match(gas_inve_match, '天然气库存')
list_data_match(sore_spot_match, '冰醋酸现货价格')
list_data_match(sore_profit_match, '冰醋酸毛利')
list_data_match(jia_spot_match, '甲醇现货价格')
list_data_match(jia_profit_match, '甲醇毛利')
list_data_match(gas_spot_match, '天然气现货价格')
# check_date('20160314', match_data)

# print(len(list(match_data.keys())))



# 这里代码的设计是有点问题的
# 尤其是匹配数据那里是有点问题的，要检查一下

# 上游的供应 下游的需求
# 天然气 甲醇 冰醋酸
# 天然气 产量 进口 库存 现货价格
# 冰醋酸 消费量 库存 进口 出口

# 将数据输出到指定的Excel文件
book = xlwt.Workbook()
sheet = book.add_sheet('sheet01')
# 写标题
sheet.write(0, 0, '日期')
i = 0
for title in head:
    i += 1
    sheet.write(0, i, title)

# 写内容
i = 0
for key in match_data.keys():
    i += 1
    j = 0
    sheet.write(i, j, key)
    # val
    val_li = match_data[key]
    for val in val_li:
        j += 1
        sheet.write(i, j, val_li[j - 1])

# 保存文件
book.save('~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据.xls')

# 检测一下数据的质量
