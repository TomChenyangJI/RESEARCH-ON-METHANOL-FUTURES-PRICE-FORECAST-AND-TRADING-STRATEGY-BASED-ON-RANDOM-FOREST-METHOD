import re

# pattern = 'the score of the module is.\d\.\d*'
# with open('xgboost_experimental_result2.txt', 'r') as fileobj:
#     context = fileobj.read()
#
# # result = re.search(pattern, context)
# result = re.findall(pattern, context)
# result = [i for i in result]
# tmp_li = []
# for record in result:
#     tmp = re.search('\d\.\d*', record)[0]
#     tmp_li.append(tmp)
#
# tmp_li.sort()
#
# print(tmp_li)

# result.sort()
# print(result)


t = [('kdj', 0.0003234503), ('rsi', 0.00042269067), ('冰醋酸现货价格', 0.0005453551), ('冰醋酸出口量', 0.00056970323), ('冰醋酸毛利', 0.0005708925), ('psy', 0.0007138715), ('macd_dea', 0.00077983807), ('天然气现货价格', 0.0008795343), ('甲醇进口', 0.0010339947), ('甲醇出口', 0.0012257621), ('冰醋酸库存', 0.001439474), ('冰醋酸消费量', 0.0020589319), ('冰醋酸进口', 0.0021710692), ('甲醇库存', 0.0039346544), ('wr', 0.0043166624), ('obv', 0.011752625), ('甲醇产量', 0.023386965), ('天然气库存', 0.025715703), ('天然气进口', 0.04246966), ('天然气产量', 0.06323533), ('甲醇现货价格', 0.2359689), ('甲醇毛利', 0.57648486)]

tmp = 0
print(len(t))
for i in t[17:]:
    print(i[0])
    tmp += i[1]
print(tmp)