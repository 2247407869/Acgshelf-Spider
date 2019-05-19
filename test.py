# coding: utf-8
import requests
from bs4 import BeautifulSoup
import pymysql

#这个应该是最新在使用的

rank = 0

# 打开数据库连接
db = pymysql.connect("localhost", "root", "lls0908329", "acgshelf", charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

for page in range(1, 200):
    url = 'http://bangumi.tv/anime/browser?sort=rank&page=%d' %page
    res = requests.get(url)
    res.encoding = 'utf-8'    #告诉requests这个网站要用utf-8编码方式
    soup = BeautifulSoup(res.text, 'html.parser')  #明白指示它剖析器
    for items in soup.select('.item'):

        sub = items.select('.l')[0]['href'].strip('/subject/')
        sub = int(sub)

        url = 'http://api.bgm.tv/subject/%d' % sub
        values = requests.get(url).json()

        try:
            type = values["type"]
        except:
            continue

        id = values["id"]
        if id != sub:
            continue

        url = values["url"]

        name = values["name"]
        name = name.replace("\\\'", "'")
        name = name.replace("'", "\\\'")

        name_cn = values["name_cn"]
        name_cn = name_cn.replace("\\\'", "'")
        name_cn = name_cn.replace("'", "\\\'")

        summary = values["summary"]
        summary = summary.replace("\\\'", "'")
        summary = summary.replace("'", "\\\'")

        try:
            eps_count = values["eps_count"]
        except:
            eps_count = '0'

        air_date = values["air_date"]
        air_weekday = values["air_weekday"]
        try:
            rating_score = values["rating"]["score"]
        except:
            rating_score = '0'

        try:
            rank = values["rank"]
        except:
            rank = '0'

        try:
            images_large = values["images"]["large"]
            images_common = values["images"]["common"]
            images_medium = values["images"]["medium"]
            images_small = values["images"]["small"]
            images_grid = values["images"]["grid"]
        except:
            images_large = ''
            images_common = ''
            images_medium = ''
            images_small = ''
            images_grid = ''
        try:
            collection_collect = values["collection"]["collect"]
        except:
            collection_collect = '0'

        data_list = [id, url, type, name, name_cn, eps_count, air_date, air_weekday, rating_score, rank, images_large,
                     collection_collect]  # 加summary
        print(data_list)

        id = int(id)
        eps_count = int(eps_count)
        air_weekday = int(air_weekday)
        rating_score = float(rating_score)
        rank+1
        collection_collect = int(collection_collect)

        # SQL 插入语句
        # if type == 2:
        sql = "INSERT INTO anime(id, url, name, name_cn, summary, eps_count, air_date, air_weekday, rating_score, " \
              "rank, images_large, images_common, images_medium, images_small, images_grid, collection_collect) VALUES " \
              "('%d', '%s', '%s', '%s', '%s', '%d', '%s', '%d', '%f', '%d', '%s', '%s', '%s', '%s', '%s', '%d')" % \
              (id, url, name, name_cn, summary, eps_count, air_date, air_weekday, rating_score, rank, images_large,
               images_common, images_medium, images_small, images_grid, collection_collect)




        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

# 关闭数据库连接
db.close()

# test
