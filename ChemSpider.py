# -*- coding: utf-8 -*-
# edited : 2022-02-26 17:02:21
# 气象爬虫文件，主要任务为爬取气象文件

import requests,logging,datetime,openpyxl
from bs4 import BeautifulSoup

def get_weather(former_time):
    """
    爬取上海生态环境局的污染物数据文件
    :param former_time: 上一次文件更新的时间
    :return: 气象数据list以及这一次的更新时间
    """
    Header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/94.0.4606.71 Safari/537.36 Edg/97.0.992.38"}
    url = "https://link.sthj.sh.gov.cn/aqi/siteAqi/siteAqi.jsp"
    # 首先尝试不带代理读取，如果不报错则代表网络可用
    try:
        res = requests.get(url, headers=Header)
        soup = BeautifulSoup(res.content, 'html.parser')
    # 如果报错则说明网络不可用，需要添加代理
    except:
        for i in open("proxy_pool.txt").readlines():
            i=i.strip()
            proxy={'https':'http://'+i}
            try:
                res=requests.get(url, headers=Header, proxies=proxy,timeout=(15,30))
                logging.info('代理可用，将使用该代理:'+str(proxy))
                soup = BeautifulSoup(res.content, 'html.parser')
                break
            except:
                logging.info('代理不可用，信息为:'+str(proxy))
    station1 = soup.find_all(attrs={'class': 'even'})
    station1_nd = station1[10::]
    station2 = soup.find_all(attrs={'class': 'odd'})
    station2_nd = station2[9::]
    station = station1_nd+station2_nd
    update_time = soup.find(class_="t-time fr")
    update_time=update_time.text[6::]

    weather_list=[]
    if update_time==former_time:
        logging.info("检测到上海生态环境局未更新数据")
        return False,update_time
    else:
        logging.info("检测到上海生态环境局已经更新数据")
        print("更新时间：{}".format(update_time))
        print("上次更新时间：{}".format(former_time))
        year=datetime.datetime.today().year
        writing_time=str(year)+"年"+update_time
        for i in station:
            td=i.find_all("td")
            weather_list.append([td[0].text,writing_time,td[1].text,td[2].text,td[3].text,td[4].text,td[5].text,td[6].text])
        return weather_list,update_time

def get_last_updatetime(filename,sheetname):
    """
    获取上一次更新时间
    :param filename: 写入数据的文件
    :return: 上一次更新时间
    """
    workbook = openpyxl.load_workbook(filename,read_only=True)
    table = workbook[sheetname]
    nrows = table.max_row  # 获得行数
    last_updatetime=table.cell(nrows,1).value
    last_updatetime=last_updatetime.split("年")[1]   # 使用split区分，取后半段
    return last_updatetime

if __name__=="__main__":
    a=get_last_updatetime("chem_data.xlsx","普陀监测站")
    print(a)