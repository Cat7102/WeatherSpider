# -*- coding: utf-8 -*-
# edited : 2022-02-26 16:57:56
# 运行脚本

import ProxySearch,ExcelOperator,ChemSpider
import time,os,logging

# 路径获取
cur_dir = os.path.abspath(os.   path.dirname(__file__))
log_path = os.path.join(cur_dir, "weather.log")
logging.basicConfig(filename=log_path, level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
filename="chem_data.xlsx"
update_time=ChemSpider.get_last_updatetime(filename,"普陀监测站")    # 获取上一次更新时间
logging.info("上一次更新时间为：{}".format(update_time))
while True:
    try:
        #proxy=ProxySearch.proxyserch()
        weather_list, update_time = ChemSpider.get_weather(update_time)
        stationname_list = []
        if weather_list!=False:
            for i in weather_list:
                stationname_list.append(i[0])
            result=ExcelOperator.check_xlsx(filename)
            if result==False:
                ExcelOperator.creat_xlsx(filename,stationname_list)
                for i in range(len(stationname_list)):
                    ExcelOperator.append_xlsx(filename,stationname_list[i],weather_list[i][1::])
                    logging.info(stationname_list[i] + "信息已写入")
            elif result==True:
                ''' 老方法
                for i in range(len(stationname_list)):
                    ExcelOperator.append_xlsx(filename,stationname_list[i],weather_list[i][1::])
                    logging.info(stationname_list[i] + "信息已写入")
                '''
                ExcelOperator.append_xlsx2(filename,weather_list)
        logging.info("本轮信息更新完成")
        time.sleep(60 * 30)
    except:
        logging.info("网络暂时无法连接，1分钟后重试")
        time.sleep(60)


