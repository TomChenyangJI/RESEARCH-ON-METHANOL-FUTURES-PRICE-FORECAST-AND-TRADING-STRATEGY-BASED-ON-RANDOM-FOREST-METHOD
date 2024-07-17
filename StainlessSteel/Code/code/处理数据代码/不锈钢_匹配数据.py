from 可调用函数模块 import *
import time
import datetime


# 技术指标 日数据


# 不锈钢 铁矿石 镍 房地产
# 获取 期货价格 日数据
future_path = {
    '不锈钢': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/期货价格/不锈钢-大智慧_收盘价.xls', 2],
    '铁矿石': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/期货价格/铁矿石期货-大智慧_收盘价.xls', 2],
    '镍': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/期货价格/镍-大智慧_收盘价.xls', 2],
    '房地产': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/期货价格/不锈钢-大智慧_收盘价.xls', 2]
}


# 获取 现货价格 日数据
spot_path = {
    '不锈钢': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/现货价格/不锈钢热轧卷板多城市现货价格.xls', 2],
    '铁矿石': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/现货价格/钢联数据_铁矿：国产：均价：中国（日）_2021-6-5_1622894537888.xls', 2],
    '镍': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/现货价格/镍.xlsx', 2],
    '房地产': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/现货价格/钢联数据_百城价格指数：样本均价：中国（月）_2021-6-5_1622894115897.xls', 2]
}

# 获取 开工率 月数据好像 周 半月数据
rate_path = {
    '不锈钢': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/开工率/不锈钢产量.xls', 2],
    '铁矿石': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/开工率/钢联数据_铁矿：产量：中国（月）_2021-6-5_1622896487420.xls', 2],
    '镍': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/开工率/电解镍.xls', 2],
    '房地产': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/开工率/钢联数据_房地产开发企业：房屋：施工面积：中国（月）_2021-6-5_1622892749718.xls', 2]
}

# 获取 毛利 日数据
profit_path = {
    '不锈钢': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/毛利/不锈钢毛利.xlsx', 2],
    '铁矿石': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/毛利/铁矿石_唐山地区钢坯利润.xls', 2],
    '镍': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/毛利/钢联数据_镍：营业净收入：全球：淡水河谷（季）_2021-6-5_1622901906311.xls', 2],
    '房地产': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/毛利/不锈钢毛利.xlsx', 2]
}

# 获取 进出口 月数据
im_ex_path = {
    '不锈钢进口': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/进出口/不锈钢进口量.xlsx', 2],
    '不锈钢出口': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/进出口/不锈钢出口量.xlsx', 2],
    '铁矿石进口': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/进出口/铁矿石_铁矿：进口数量合计：全球—中国（月）.xls', 2],
    '铁矿石出口': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/进出口/铁矿石_铁矿：出口数量合计：中国—全球（月）.xls', 2],
    '镍进口': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/进出口/电解镍进口量.xlsx', 2],
    '镍出口': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/进出口/电解镍出口量.xlsx', 2]
}

# 获取 库存 周
inventory_path = {
    '不锈钢': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/库存/不锈钢主要钢厂库存.xls', 2],
    '铁矿石': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/库存/卓_铁矿石_中国45个港口库存量.xls', 2],
    '镍': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/扩充数据/库存/镍.xls', 2],
    '房地产': ['~/Desktop/论文研究/不锈钢/数据/格式化数据/库存/房地产存量多地.xls', 2]
}

# 接下里是获取数据
# 不锈钢 铁矿石 镍 房地产
# steel ore nie estate

# 获取 期货价格 日
steel_future = getData(future_path['不锈钢'][0],1)
ore_future = getData(future_path['铁矿石'][0],1)
nie_future = getData(future_path['镍'][0],1)

# 获取 现货价格 日 房地产是月
steel_spot = getData(spot_path['不锈钢'][0],1)
ore_spot = getData(spot_path['铁矿石'][0],1)
nie_spot = getData(spot_path['镍'][0],1)
estate_spot = getData(spot_path['房地产'][0],1)

# 获取 开工率 月
steel_rate = getData(rate_path['不锈钢'][0], 1)
ore_rate = getData(rate_path['铁矿石'][0], 1)
nie_rate = getData(rate_path['镍'][0], 1)
estate_rate = getData(rate_path['房地产'][0], 1)

# 获取 毛利 日 镍是季
steel_profit = getData(profit_path['不锈钢'][0], 1)
ore_profit = getData(profit_path['铁矿石'][0], 1)
nie_profit = getData(profit_path['镍'][0], 1)

# 获取 进出口 月
steel_im = getData(im_ex_path['不锈钢进口'][0], 1)
steel_ex = getData(im_ex_path['不锈钢出口'][0], 1)
ore_im = getData(im_ex_path['铁矿石进口'][0], 1)
ore_ex = getData(im_ex_path['铁矿石出口'][0], 1)
nie_im = getData(im_ex_path['镍进口'][0], 1)
nie_ex = getData(im_ex_path['镍出口'][0], 1)

# 获取 库存 月 铁矿石是周
steel_inve = getData(inventory_path['不锈钢'][0], 1)
ore_inve = getData(inventory_path['铁矿石'][0], 1)
nie_inve = getData(inventory_path['镍'][0], 1)
estate_inve = getData(inventory_path['房地产'][0], 1)


def getPrevDay(date):
    delta = datetime.timedelta(-1)
    struct_date = time.strptime(date, '%Y%m%d')
    datetime_obj = datetime.datetime(struct_date.tm_year, struct_date.tm_mon, struct_date.tm_mday)
    datetime_obj = datetime_obj + delta
    return str(datetime_obj.strftime('%Y%m%d'))


# 首先要字典数据是
def day_match_month(day_data, month_data):
    pass


# 接下来是错开匹配数据 // 错开匹配数据的时候要考虑到时间的问题，如果是日和周数据进行匹配的话，只能是利用前一周的数据
# 所有数据以不锈钢的期货价格为基准
# 不锈钢 铁矿石 镍 房地产
# steel ore nie estate

# 获取 期货价格 日

# 获取 现货价格 日 房地产是月

# 获取 开工率 月

# 获取 毛利 日 镍是季

# 获取 进出口 月

# 获取 库存 月 铁矿石是周

