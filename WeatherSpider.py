import requests
a=requests.get("http://api.data.cma.cn/api?key=9826DCE2968D336B393455E6C2900EE4"
               "&data=SURF_CHN_HOR&staIDs=58369&times=20220508020000")
print(a.content)