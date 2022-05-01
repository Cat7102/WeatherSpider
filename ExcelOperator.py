# -*- coding: utf-8 -*-
# edited : 2022-02-26 17:00:05
# Excel操作文件，包含了气象参数爬取所需要的excel步骤

import os,logging,openpyxl
import xlrd
import xlwt
from xlutils.copy import copy
import logging

def check_xlsx(filename):
    """
    检查污染物数据表格文件是否已经存在
    :param filename: excel文件名
    :return: 文件是否存在
    """
    if os.path.isfile(filename):
        logging.info("文件已存在，将追加写入:"+filename)
        return True
    else:
        logging.info("文件不存在，将创建:"+filename)
        return False

def creat_xlsx(filename,stationname_list):
    """
    创建excel并进行初始化
    :param filename: excel文件名
    :param stationname_list: 站点列表
    """
    workbook=openpyxl.Workbook()
    title_list=["时间","PM2.5(μg/m3)","PM10(μg/m3)","O3(μg/m3)","CO(mg/m3)","SO2(μg/m3)","NO2(μg/m3)"]
    for i in stationname_list[0::]:
        workbook.create_sheet(title=i, index=-1)
        for j in range(len(title_list)):
            workbook[i].cell(1,j+1).value=title_list[j]
    workbook.remove(workbook['Sheet'])
    workbook.save(filename)
    logging.info(filename+"文件创建完毕")

def append_xlsx(filename,sheetname,weatherdata):
    """
    在污染物excel文件中进行追加写入
    :param filename: excel文件名
    :param sheetname: 站点列表
    :param weatherdata: 气象数据list
    """
    workbook = openpyxl.load_workbook(filename)
    table = workbook[sheetname]
    nrows = table.max_row  # 获得行数
    for i in range(len(weatherdata)):
        table.cell(nrows+1,i+1).value=weatherdata[i]
    workbook.save(filename)

def append_xlsx2(filename,weatherdata):
    """
    在污染物excel文件中进行追加写入,使用openpyxl，更改了下代码提高性能
    :param filename: excel文件名
    :param weatherdata: 气象数据list
    :return: None
    """
    workbook = openpyxl.load_workbook(filename)
    for weatherlist in weatherdata:
        station=weatherlist[0]
        table = workbook[station]
        table.append(weatherlist[1::])
        logging.info(station+"信息已写入")
    workbook.save(filename)

def append_xlsx_xlwt(filename,weatherdata):
    """
    在污染物excel文件中进行追加写入,使用xlwt库，效率更高，但是只支持xls文件
    :param filename: excel文件名
    :param weatherdata: 气象数据list
    :return: None
    """
    wb=xlrd.open_workbook(filename)
    excel=copy(wb) # 对复制的对象进行操作
    for weatherlist in weatherdata:
        station=weatherlist[0]
        nrows = wb.sheet_by_name(station).nrows # 获取最大行数
        sheet_index = [s.name for s in wb.sheets()].index(station)
        sheet = excel.get_sheet(sheet_index)
        c=0
        for value in weatherlist[1::]:
            sheet.write(nrows, c, value)
            c += 1
        logging.info(station+"信息已写入")
    excel.save(filename)