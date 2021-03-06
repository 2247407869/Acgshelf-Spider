# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pymysql

#这个应该是早期测试mysql可用性的。。

# 打开数据库连接
db = pymysql.connect("localhost", "root", "lls0908329", "testdb", charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

for page in range(1, 200):
    url = 'http://bangumi.tv/game/browser?sort=rank&page=%d' % page
    res = requests.get(url)
    res.encoding = 'utf-8'  # 告诉requests这个网站要用utf-8编码方式
    soup = BeautifulSoup(res.text, 'html.parser')  # 明白指示它剖析器
    for items in soup.select('.item'):
        name = items.select('.l')[0].text
        rank = items.select('.rank')[0].text.strip('Rank ')
        point = items.select('.fade')[0].text
        pnum = items.select('.tip_j')[0].text.rstrip('人评分)').lstrip('(')

        newurlpart = items.select('.l')[0]['href']  # 取得href属性中的内容
        newurl = 'http://bangumi.tv/%s' % newurlpart
        sub = items.select('.l')[0]['href'].strip('/subject/')
        newres = requests.get(newurl)
        newres.encoding = 'utf-8'
        newsoup = BeautifulSoup(newres.text, 'html.parser')
        for newitems in newsoup.select('.infobox'):
            try:
                time = newitems.find(text="发行日期: ").parent.parent.text.lstrip('发行日期: ')
            except:
                time =None

        # time = items.select('.info')[0].text
        # dt = datetime.strptime(time,'')

        data_list = [sub, rank, point, pnum, name, time, newurl]
        print(data_list)

        sub = int(sub)
        rank = int(rank)
        point = float(point)
        pnum = int(pnum)


        #SQL 插入语句
        sql = "INSERT INTO game_ranking(id, ranking, score, pnum, name, faxing, url)\
                     VALUES ('%d', '%d', '%f', '%d', '%s', '%s', '%s')" %(sub, rank, point, pnum, name, time, newurl)

            # 执行sql语句
        cursor.execute(sql)
            # 提交到数据库执行
        db.commit()

# 关闭数据库连接
db.close()