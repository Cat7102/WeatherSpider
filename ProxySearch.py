# -*- coding: utf-8 -*-
# edited : 2022-02-26 13:03:02
# 由于上海生态环境局不允许国外ip访问，因此需要国外服务器转国内代理

import logging,requests

def proxyserch():
    """
    检测当前可用的https代理
    :return: 可用的代理信息
    """
    Header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/97.0.992.38"}
    testurl = "https://link.sthj.sh.gov.cn/aqi/siteAqi/siteAqi.jsp"
    proxy=None

    for i in open("proxy_pool.txt").readlines():
        i=i.strip()
        proxy={'https':'http://'+i}
        try:
            requests.get(testurl, headers=Header, proxies=proxy,timeout=(15,30))
            logging.info('代理可用，将使用该代理:'+str(proxy))
            break
        except:
            logging.info('代理不可用，信息为:'+str(proxy))

    return proxy