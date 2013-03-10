# ! -*-Encoding:utf-8 -*-
'''
Created on 2013-2-25

@author: Zoei
'''
import sys, urllib, os
from bs4 import BeautifulSoup
import csv, collections, re
import http.client

inputkey = sys.argv[1]
startpage = int(sys.argv[2])
endpage = int(sys.argv[3])
timescope = sys.argv[4]
starttime = timescope.split(":")[1]
endtime = timescope.split(":")[2]
print("===========搜索（%s）, 页码（%d-%d）, 时间(%s ~ %s)===========" % (inputkey, startpage, endpage, starttime, endtime))

ROOT_DIR = os.getcwd()
TEMP_DIR = os.path.sep.join((ROOT_DIR, "data", "temp"))
OUTPUT_DIR = os.path.sep.join((ROOT_DIR, "data"))
OUTPUT_FILE = os.path.sep.join((OUTPUT_DIR, "%s_%s_%s.csv" % (inputkey, starttime, endtime)))
ZUANJIA_FILE = os.path.sep.join((OUTPUT_DIR, "%s_%s_%s_500plus.csv" % (inputkey, starttime, endtime)))

news = collections.namedtuple("News", "title,time,author,detail,remark")
weibo = [news("关键字", "时间", "作者", "内容", "备注")]
zuanjiaweibo = [news("关键字", "时间", "作者", "内容", "备注")]

def downloadPage(keyword, index):
    url = "http://s.weibo.com/weibo/"
    keywordmap = {'':keyword}
    values = {'':urllib.parse.urlencode(keywordmap)[1:]}
    if index == 1 :
        values['Refer'] = 'g'
    else:
        values['page'] = index
# #    values['timescope'] = timescope
    encoded_param = urllib.parse.urlencode(values)[1:]
    full_url = url + encoded_param + '&timescope=' + timescope
    
    conn = http.client.HTTPConnection("s.weibo.com", 80)
    conn.request("GET", full_url)
    res = conn.getresponse()
    restext = res.read().decode('utf_8')
    print("download page %d: %s [%s]" % (index, full_url, res.status))

# #    tempfile = "%s/%s_%d.html" % (TEMP_DIR, keyword, index)
# #    save2file(tempfile, restext)
    return parsehtml(restext)

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
            zuanjia = False
            for a in content('p', {'class':'info W_linkb W_textb'})[0]('a')[:3]:
                remark += a.text + '|'
                start = remark.find("(")
                end = remark.find(")")
                if not start == -1 and not end == -1:
                    num = int(remark[start+1:end])
                    if num > 10:
                        zuanjia = True
                        
            if len(content('img', {'action-type':'feed_list_media_img'})) > 0:
                remark += '有图片|'
            if len(content('img', {'action-type':'feed_list_media_video'})) > 0:
                remark += '有视频'
    
            if zuanjia:
                zuanjiaweibo.append(news(title, time, author, detail, remark))
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
            print("not more content")
            break
    if len(weibo) > 1:
        f = open(OUTPUT_FILE, "w", encoding="gb18030")
        writer = csv.writer(f, "excel")
        for item in weibo:
            writer.writerow(item)
        print("解析成功,保存结果到文件：%s" % OUTPUT_FILE)
    if len(zuanjiaweibo) > 1:
        f = open(ZUANJIA_FILE, "w", encoding="gb18030")
        writer = csv.writer(f, "excel")
        for item in zuanjiaweibo:
            writer.writerow(item)
        print("解析转发超过500数据成功,保存结果到文件：%s" % ZUANJIA_FILE)

# #if not os.path.exists(TEMP_DIR):
# #    os.makedirs(TEMP_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
print("----------解析开始----------")
parsebyurl()
print("----------解析结束----------")
