# ! -*-Encoding:utf-8 -*-
'''
Created on 2013-2-25

@author: Zoei
'''
import sys, urllib.parse, os
from bs4 import BeautifulSoup,Tag
import csv, collections
import http.client
import httplib2

#usrname = sys.args[1]
#pwd = sys.args[2]
#optiontype = sys.args[3]
option = 'submit'
ROOT_DIR = os.getcwd()
TEMP_DIR = os.path.sep.join((ROOT_DIR, "data", "temp"))
OUTPUT_DIR = os.path.sep.join((ROOT_DIR, "data"))
OUTPUT_FILE = os.path.sep.join((OUTPUT_DIR, "%s.csv" % "result"))

Record = collections.namedtuple("Record", "id,summary,submiter,posttime,updatetime")
recordheader = Record("ID", "内容", "提交者", "内容", "备注")
records = []
http = httplib2.Http('.cache')
outputhtml = ''

def downloadPage(url):
    res,ctt = http.request(url, 'GET')
    print('%s [%s]' % (url,res.status))

    restext = ctt.decode('utf_8')

    tempfile = "%s/httplib2_result.html" % (TEMP_DIR)

    save2file(tempfile, restext)
    return parsehtml(restext)

def save2file(filepath, content):
    f = open(filepath, "w", encoding="utf8")
    f.write(content)
    f.close()

def parsehtml(html,optiontype):
    soup = BeautifulSoup(html, from_encoding='gb18030')
    outputhtml = soup.prettify()
    try:
        table = soup('table', { "class" : "datagrid" })[1]('tbody')[0]
        for tr in table('tr'):
            reviewid= tr('img')[0]['data-object-id']
            summary = tr('a')[0].text
            newrecord = Record(reviewid,summary,'','','')
            records.append(newrecord)
            #print('%s [%s]%s ...' %(optiontype,reviewid,summary))
            #eval('%s(%s)' % (optiontype ,reviewid))
        return True
    except Exception as e:
        print(e)
        return False

def submit(reviewid):
    url = ('%s%d%s' % ('http://172.26.184.150/reviews/api/review-requests/' , reviewid , '/?api_format=json'))
    apirequest(url)

def apirequest(url):
    try:
        print(url)
        res,ctt = http.request(url, 'GET')
        print(res.status)
    except Exception as e:
        print('NG:%s' % e)

def parsebyfile(optiontype):
    f = open("list.htm", "r", encoding="utf_8")
    html = f.read()
    f.close()
    parsehtml(html,optiontype)
    
def parsebyurl(optiontype):
    start = 1
    end = 1
    for i in range(start, end+ 1):
        url = "http://s.weibo.com/weibo/"
        if not downloadPage(url,optiontype):
            print("not more content")
            break
    print('提交成功')

def write2html(data):
    #soup = BeautifulSoup()
    #tag1 = Tag(soup, "mytag")
    #tag2 = Tag(soup, "myOtherTag")
    #tag3 = Tag(soup, "myThirdTag")
    #soup.insert(0, tag1)
    #tag1.insert(0, tag2)
    #tag1.insert(1, tag3)

    #print(str(soup))
    
    f = open("result.html", "w", encoding="utf_8")
    f.write('<!DOCTYPE HTML><html><body><table border="1">')
    for r in data:
        f.write('<tr><td><input type="checkbox" name="review" value="{id}"></td><td>{summary}</td></tr>'.format(**r._asdict()))
    f.write('</table></body></html>')
    f.close()

print("----------处理开始----------")
#parsebyurl(option)
parsebyfile(option)

write2html(records)
print("----------处理结束----------")

