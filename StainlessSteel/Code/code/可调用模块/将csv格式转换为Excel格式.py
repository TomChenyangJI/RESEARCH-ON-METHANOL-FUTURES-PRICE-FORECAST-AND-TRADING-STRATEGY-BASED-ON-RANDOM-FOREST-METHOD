
import os
import sys
import xlrd
import re
import xlwt

# 这是文件夹的路径，此程序是将这个文件夹中的csv文件转换为xls文件，保存的路径也为本文件夹
directory_path = '~/Desktop/ 小论文/数据/库存/卓创的铁矿石库存'

filesAndDirectories = os.listdir(directory_path)

def getCSVFiles(fileList):
    csv_files = []
    for item in fileList:
        string = item
        result = string.split('.')

        if len(result) == 1:
            pass
        else:
            if result[1] == 'csv':
                csv_files.append(string)

    return csv_files


def getExcelFileName(fileName):
    result = fileName.split('.')
    fileName = result[0]
    return fileName

def convertCSVToExcel(csv_file_base_path, csv_file_name):
    file_obj = open(csv_file_base_path + '/' + csv_file_name, 'r')
    # csv_file_name = getFileName(csv_file_path)
    lines = file_obj.readlines()
    book = xlwt.Workbook(csv_file_name) # 这里要解析一下文件的名称
    sheet = book.add_sheet('sheet1')
    sheet.write(0, 0, '日期')
    sheet.write(0, 1, '价格')

    i = 0
    for row in lines[1:]:
        i += 1
        row_split = row.split(',')
        date = row_split[0]
        price = row_split[1]
        date = date.replace('-', '') # 这一行代码是针对日期格式为 2020-01-29的
        sheet.write(i, 0, date)
        sheet.write(i, 1, price)
    file_obj.close()
    book.save(csv_file_base_path + '/' + getExcelFileName(csv_file_name) + '.xls')

csvFiles = getCSVFiles(filesAndDirectories)

for csv_file in csvFiles:
    convertCSVToExcel(directory_path, csv_file)

