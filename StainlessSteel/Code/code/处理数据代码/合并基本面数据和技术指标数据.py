import xlrd
import xlwt


base_features = '~/Desktop/论文研究/甲醇/汇总后的数据/汇总后的数据.xls'
technical_inx = '~/Desktop/论文研究/甲醇/技术指标数据.xls'


# 获取基本面数据
base_obj = xlrd.open_workbook(base_features)
sheet = base_obj.sheet_by_index(0)
row = sheet.nrows
col = sheet.ncols
head1 = []
for i in range(1, col):
    head1.append(sheet.cell_value(0, i))
val_dict = {}
for i in range(1, row):
    key = sheet.cell_value(i, 0)
    val = []
    for col_inx in range(1, col):
        val.append(sheet.cell_value(i, col_inx))
    val_dict[key] = val


# 获取技术指标数据
tech_obj = xlrd.open_workbook(technical_inx)
sheet = tech_obj.sheet_by_index(0)
row = sheet.nrows
col = sheet.ncols
head2 = []
for i in range(2, col):
    head2.append(sheet.cell_value(0, i))
val_dict2 = {}
for i in range(1, row):
    key = sheet.cell_value(i, 0)
    val = []
    for col_inx in range(2, col):
        val.append(sheet.cell_value(i, col_inx))
    val_dict2[key] = val

# 匹配基本面数据和技术指标数据
# val_dict val_dict2

val_dict_key_li = list(val_dict.keys())
val_dict2_key_li = list(val_dict2.keys())
final_dict = {}
for key in val_dict_key_li:
    if key in val_dict2_key_li:
        val_li1 = val_dict[key]
        val_li2 = val_dict2[key]
        val_li = val_li1 + val_li2
        final_dict[key] = val_li
# print(len(final_dict['20200210']))
# print(len(list(final_dict.keys())))
# print(head1 + head2)

# 合并基本面数据和技术指标后的数据
book = xlwt.Workbook()
sheet = book.add_sheet('sheet01')
sheet.write(0, 0, '日期')
# 写标题
head = head1 + head2
col_inx = 0
for title in head:
    col_inx += 1
    sheet.write(0, col_inx, title)

amount = len(list(final_dict.keys()))

row = 0
for key in final_dict.keys():
    row += 1
    sheet.write(row, 0, key)
    val_li = final_dict[key]
    col_num = 0
    for col_val in val_li:
        col_num += 1
        sheet.write(row, col_num, col_val)

book.save('~/Desktop/论文研究/甲醇/基本面+技术指标.xls')