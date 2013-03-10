# ! -*-Encoding:utf-8 -*-
'''
Created on 2013-2-25

@author: Zoei
'''
import sys, urllib, os
from bs4 import BeautifulSoup
import csv, collections
import http.client

#inputkey = "Movies"
#startpage = 1
#endpage = 3
inputkey = sys.argv[1]
startpage = int(sys.argv[2])
endpage = int(sys.argv[3])
startime,endtime = sys.argv[4].split(":")
print("=======搜索（%s）, 页码（%d-%d）时间段（%s ~ %s）=======" % (inputkey, startpage, endpage, startime, endtime))

ROOT_DIR = os.getcwd()
TEMP_DIR = os.path.sep.join((ROOT_DIR, "data", "temp"))
OUTPUT_DIR = os.path.sep.join((ROOT_DIR, "data"))
OUTPUT_FILE = os.path.sep.join((OUTPUT_DIR, "%s(%sto%s).csv" % (inputkey,startime,endtime)))
OUTPUT_HOT_FILE = os.path.sep.join((OUTPUT_DIR, "%s(%sto%s)_hot.csv" % (inputkey,startime,endtime)))

news = collections.namedtuple("News", "title,time,author,detail,remark")
weibo = [news("关键字", "时间", "作者", "内容", "备注")]
weibo_hot = [news("关键字", "时间", "作者", "内容", "备注")]

def downloadPage(keyword, index):
    url = "http://s.weibo.com/weibo/"
    keywordmap = {'':keyword}
    values = {'':urllib.parse.urlencode(keywordmap)[1:]}
    values['scope'] = 'ori'
    if index == 1 :
        values['Refer'] = 'g'
    else:
        values['page'] = index
    values['timescope'] = "custom:%s:%s" % (startime, endtime)
    encoded_param = urllib.parse.urlencode(values)[1:]
    full_url = url + encoded_param
    
    conn = http.client.HTTPConnection("s.weibo.com", 80)
    conn.request("GET", full_url)
    res = conn.getresponse()
    restext = res.read().decode('utf_8')
    print("download page %d: %s [%s]" % (index, full_url, res.status))

#    tempfile = "%s/%s_%d.html" % (TEMP_DIR, keyword, index)
#    save2file(tempfile, restext)
    return parsehtml(restext)

def save2file(filepath, content):
    f = open(filepath, "w", encoding="utf8")
    f.write(content)
    f.close()

def parsehtml(html):
    soup = BeautifulSoup(html, from_encoding="gb18030")
    try:
        contents = soup('dd', { "class" : "content" })
        if not contents:
            return False
        for content in soup('dd', { "class" : "content" }):
            ishot = False
            title = inputkey
            time = content('a', {'class':'date'})[0].text
            author = content('a')[0]['title']
            detail = content('p', {'node-type':'feed_list_content'})[0]('em')[0].text
            remark = ''
            for a in content('p', {'class':'info W_linkb W_textb'})[0]('a')[:3]:
                remark += a.text + '|'
                lbrackets = remark.find("(")
                rbrackets = remark.find(")")
                iszuan = a.text.find("转发")
                if not lbrackets == -1 and not rbrackets == -1 and not iszuan == -1 and int(remark[lbrackets+1:rbrackets])>=200:
                    ishot = True
            if len(content('img', {'action-type':'feed_list_media_img'})) > 0:
                remark += '有图片|'
            if len(content('img', {'action-type':'feed_list_media_video'})) > 0:
                remark += '有视频'

            if ishot:
                weibo_hot.append(news(title, time, author, detail, remark))
            else:
                weibo.append(news(title, time, author, detail, remark))
        return True
    except Exception as e:
        print(e)
        return False

def parsebyfile():
    f = open("D:/collection/temp/%s_1.html" % inputkey, "r", encoding="utf8")
    html = f.read()
    f.close()
    parsehtml(html)
    
def parsebyurl():
    for i in range(startpage, endpage + 1):
        if not downloadPage(inputkey, i):
            print("没有更多的搜索结果")
            break
    if len(weibo) > 1:
        f = open(OUTPUT_FILE, "w", encoding="gb18030")
        writer = csv.writer(f, "excel")
        for item in weibo:
            writer.writerow(item)
        print("解析成功, 保存至文件：%s" % OUTPUT_FILE)
    if len(weibo_hot) > 1:
        f = open(OUTPUT_HOT_FILE, "w", encoding="gb18030")
        writer = csv.writer(f, "excel")
        for item in weibo_hot:
            writer.writerow(item)
        print("解析成功, 保存至文件：%s" % OUTPUT_HOT_FILE)

#if not os.path.exists(TEMP_DIR):
#    os.makedirs(TEMP_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
print("---------- 解析开始 ----------")
parsebyurl()
print("---------- 解析结束 ----------")

