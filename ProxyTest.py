# -*- coding: utf-8 -*-
# edited : 2022-02-26 21:07:28
# 测试文件，用于检测https代理是否可用

import requests

def proxytest():
    """
    检测当前可用的https代理
    :return: 可用的代理信息
    """
    Header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/97.0.992.38"}
    testurl = "https://link.sthj.sh.gov.cn/aqi/siteAqi/siteAqi.jsp"

    for i in open("proxy_pool.txt").readlines():
        i=i.strip()
        proxy={'https':'http://'+i}
        print(proxy)
        try:
            requests.get(testurl, headers=Header, proxies=proxy,timeout=(15,30))
            print('代理可用:'+str(i))
        except:
            print('代理不可用:'+str(i))

if __name__ == '__main__':
    proxytest()