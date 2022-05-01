# -*- coding: utf-8 -*-
# edited : 2022-02-26 17:00:05
# Excel操作文件，包含了气象参数爬取所需要的excel步骤

import os,logging,openpyxl

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