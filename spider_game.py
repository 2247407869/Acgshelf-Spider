# coding: utf-8
import requests
from bs4 import BeautifulSoup
import xlwt

def main():
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1', cell_overwrite_ok=True)
    heads = [u'ID', u'排名', u'分数', u'评论人数', u'名称', u'发行日期', u'url']
    ii = 0
    i = 1
    for head in heads:
        sheet1.write(0, ii, head)
        ii += 1

    for page in range(1, 2):
        url = 'http://bangumi.tv/game/browser?sort=rank&page=%d' %page
        res = requests.get(url)
        res.encoding = 'utf-8'    #告诉requests这个网站要用utf-8编码方式
        soup = BeautifulSoup(res.text, 'html.parser')  #明白指示它剖析器
        for items in soup.select('.item'):
            name = items.select('.l')[0].text
            rank = items.select('.rank')[0].text.strip('Rank ')
            point = items.select('.fade')[0].text
            pnum = items.select('.tip_j')[0].text.rstrip('人评分)').lstrip('(')

            newurlpart = items.select('.l')[0]['href']  #取得href属性中的内容
            newurl = 'http://bangumi.tv%s' %newurlpart
            sub = items.select('.l')[0]['href'].strip('/subject/')
            newres = requests.get(newurl)
            newres.encoding = 'utf-8'
            newsoup = BeautifulSoup(newres.text, 'html.parser')
            for newitems in newsoup.select('.infobox'):
                try:
                    time = newitems.find(text="发行日期: ").parent.parent.text.lstrip('发行日期: ')
                except:
                    time = 'unknown'
            #time = items.select('.info')[0].text
            #dt = datetime.strptime(time,'')
            data_list = [sub, rank, point, pnum, name, time, newurl]
            print(data_list)
            j = 0
            for data in data_list:
                sheet1.write(i, j, data)
                j += 1
            i += 1

    book.save('游戏排名2.0.xls')

if __name__ =='__main__':
    main()