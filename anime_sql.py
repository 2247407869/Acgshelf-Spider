# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "testdb", charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

for page in range(1, 200):
    url = 'http://bangumi.tv/anime/browser?sort=rank&page=%d' %page
    res = requests.get(url)
    res.encoding = 'utf-8'    #告诉requests这个网站要用utf-8编码方式
    soup = BeautifulSoup(res.text, 'html.parser')  #明白指示它剖析器
    for items in soup.select('.item'):
        name = items.select('.l')[0].text
        rank = items.select('.rank')[0].text.strip('Rank ')
        point = items.select('.fade')[0].text
        pnum = items.select('.tip_j')[0].text.rstrip('人评分)').lstrip('(')

        newurlpart = items.select('.l')[0]['href']  #取得href属性中的内容
        newurl = 'http://bangumi.tv/%s' %newurlpart
        sub = items.select('.l')[0]['href'].strip('/subject/')
        newres = requests.get(newurl)
        newres.encoding = 'utf-8'
        newsoup = BeautifulSoup(newres.text, 'html.parser')
        for newitems in newsoup.select('.infobox'):
            try:
                time = newitems.find(text="放送开始: ").parent.parent.text.lstrip('放送开始: ')
            except:
                try:
                    time = newitems.find(text="上映年度: ").parent.parent.text.lstrip('上映年度: ')
                except:
                    time = 'unknown'
            try:
                set_number = newitems.find(text="话数: ").parent.parent.text.lstrip('话数: ')
            except:
                set_number = 'unknown'
        #time = items.select('.info')[0].text
        #dt = datetime.strptime(time,'')
        data_list = [sub, rank, point, pnum, name, time, set_number, newurl]
        print(data_list)

        sub = int(sub)
        rank = int(rank)
        point = float(point)
        pnum = int(pnum)

        # SQL 插入语句
        sql = "INSERT INTO anime_ranking(id, ranking, score, pnum, name, faxing, huashu, url)\
                             VALUES ('%d', '%d', '%f', '%d', '%s', '%s', '%s', '%s')" % (
        sub, rank, point, pnum, name, time, set_number, newurl)#需要转译

        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

# 关闭数据库连接
db.close()

# test
