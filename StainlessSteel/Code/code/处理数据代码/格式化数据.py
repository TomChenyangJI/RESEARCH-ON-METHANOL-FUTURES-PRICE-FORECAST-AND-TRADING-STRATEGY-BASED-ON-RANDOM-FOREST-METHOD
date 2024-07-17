import xlrd
import xlwt
from xlrd.xldate import xldate_as_datetime
from 可调用函数模块2 import get_files


# 处理开工率
# path = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸产能.xlsx'

result = get_files('~/Desktop/论文研究/甲醇/天然气')

for path in result:
    i_book = xlrd.open_workbook(path)
    col = 1
    sheet = i_book.sheet_by_index(0)
    row = sheet.nrows
    key1 = sheet.cell_value(0, 0)
    val1 = sheet.cell_value(0, col)
    val_dict = {}
    for i in range(1, row):
        key = sheet.cell_value(i, 0)
        try:
            key = xldate_as_datetime(key, '').strftime('%Y%m%d')
        except TypeError:
            key = key[0:4] + key[5:7] + key[8:]
        val_dict[key] = sheet.cell_value(i, 1)
    print(val_dict)

    o_book = xlwt.Workbook('')
    o_sheet = o_book.add_sheet('sheet01')
    o_sheet.write(0, 0, key1)
    o_sheet.write(0, 1, val1)
    i = 0
    for key in val_dict.keys():
        i += 1
        o_sheet.write(i, 0, str(key))
        o_sheet.write(i, 1, float(val_dict[key]))
    o_book.save(path.replace('.xlsx', '.xls'))

# path = '~/Desktop/论文研究/甲醇/冰醋酸/冰醋酸国标低端现货价格.xls'
# i_book = xlrd.open_workbook(path)
# col = 1
# sheet = i_book.sheet_by_index(0)
# row = sheet.nrows
# key1 = sheet.cell_value(0, 0)
# val1 = sheet.cell_value(0, col)
# val_dict = {}
# for i in range(1, row):
#     key = sheet.cell_value(i, 0)
#     try:
#         key = xldate_as_datetime(key, '').strftime('%Y%m%d')
#     except TypeError:
#         key = key[0:4] + key[5:7] + key[8:]
#     val_dict[key] = sheet.cell_value(i, 1)
# print(val_dict)
#
# o_book = xlwt.Workbook('')
# o_sheet = o_book.add_sheet('sheet01')
# o_sheet.write(0, 0, key1)
# o_sheet.write(0, 1, val1)
# i = 0
# for key in val_dict.keys():
#     i += 1
#     o_sheet.write(i, 0, str(key))
#     o_sheet.write(i, 1, float(val_dict[key]))
# o_book.save(path.replace('.xlsx', '.xls'))
