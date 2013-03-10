# ! -*-Encoding:utf-8 -*-
'''
Created on 2013-2-25

@author: Zoei
'''
import sys, urllib, os
from bs4 import BeautifulSoup
import csv, collections
import http.client

#inputkey = sys.argv[1]
#startpage = int(sys.argv[2])
#endpage = int(sys.argv[3])
#print("==========================搜索（%s）, 页码（%d-%d）==========================" % (inputkey, startpage, endpage))

ROOT_DIR = os.getcwd()
TEMP_DIR = os.path.sep.join((ROOT_DIR, "data", "temp"))
OUTPUT_DIR = os.path.sep.join((ROOT_DIR, "data"))
OUTPUT_FILE = os.path.sep.join((OUTPUT_DIR, "%s.csv" % "result"))

news = collections.namedtuple("News", "title,time,author,detail,remark")
weibo = [news("关键字", "时间", "作者", "内容", "备注")]

def downloadPage():
    url = "http://172.26.184.150/reviews/dashboard"
    keywordmap = {'view':'mine'}
    encoded_param = urllib.parse.urlencode(keywordmap)
    full_url = url + "?" + encoded_param
    
    conn = http.client.HTTPConnection("172.26.184.15", 80)
    conn.request("GET", url)
    res = conn.getresponse()
    restext = res.read().decode('utf_8')
    print("download page %s [%s]" % (full_url, res.status))

    tempfile = "%s/result.html" % (TEMP_DIR)

    save2file(tempfile, restext)
    return True #parsehtml(restext)

def save2file(filepath, content):
    f = open(filepath, "w", encoding="utf8")
    f.write(content)
    f.close()

def parsehtml(html):
    soup = BeautifulSoup(html, from_encoding="gb18030")
    soup.prettify()
    try:
        for content in soup('dd', { "class" : "content" }):
            title = inputkey
            time = content('a', {'class':'date'})[0].text
            author = content('a')[0]['title']
            detail = content('p', {'node-type':'feed_list_content'})[0]('em')[0].text
            remark = ''
            for a in content('p', {'class':'info W_linkb W_textb'})[0]('a')[:3]:
                remark += a.text + '|'
            if len(content('img', {'action-type':'feed_list_media_img'})) > 0:
                remark += '有图片|'
            if len(content('img', {'action-type':'feed_list_media_video'})) > 0:
                remark += '有视频'
    
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
            print("not more content")
            break
    if len(weibo) > 0:
        f = open(OUTPUT_FILE, "w", encoding="gb18030")
        writer = csv.writer(f, "excel")
        for item in weibo:
            writer.writerow(item)
        print("解析成功,保存结果到文件：%s" % OUTPUT_FILE)

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
print("----------解析开始----------")
#parsebyurl()
downloadPage()
print("----------解析结束----------")

