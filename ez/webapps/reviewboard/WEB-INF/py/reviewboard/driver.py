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

username = sys.argv[1]
passwd = sys.argv[2]
option = sys.argv[3]
#option = 'submit'
ROOT_DIR = os.getcwd()

Record = collections.namedtuple("Record", "id,summary,submiter,posttime,updatetime")
recordheader = Record("ID", "内容", "提交者", "内容", "备注")
records = []
outputhtml = ''

http = httplib2.Http('.cache')
HOST = 'http://172.26.184.150'
headers = {'Content-type': 'application/x-www-form-urlencoded'}

login_url = 'http://172.26.184.150/reviews/account/login/'
login_data = {'username':username ,'password':passwd, 'next_page':'/reviews/dashboard/'}

submit_url = 'http://172.26.184.150/reviews/api/review-requests/%s/'
submit_data = {'api_format':'json', 'status':'submitted'}

review_url = 'http://172.26.184.150/reviews/api/review-requests/%s/reviews/'
review_data = {'api_format':'json', 'ship_it':'1', 'body_top':'', 'body_bottom':'', 'public':'1'}

ship_url = 'http://172.26.184.150/reviews/api/review-requests/%s/reviews/'
ship_data = {'api_format':'json', 'ship_it':'1', 'body_top':'', 'body_bottom':'', 'public':'1'}

def login():
    url = "http://172.26.184.150/reviews/account/login/"
    res,ctt = apirequest(url)
    headers['Cookie'] = res['set-cookie']

    res,ctt = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(login_data))
    headers['Cookie'] = res['set-cookie']
    print('login success')

def downloadPage(url,optiontype):
    res,ctt = apirequest(url)
    print('%s [%s]' % (url,res.status))

    restext = ctt.decode('utf_8')

    tempfile = "httplib2_result.html"

    save2file(tempfile, restext)
    return parsehtml(restext,optiontype)

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
        return True
    except Exception as e:
        print(e)
        return False

def submit(reviewid):
    url = ('%s%s%s' % ('http://172.26.184.150/reviews/api/review-requests/' , reviewid , '/'))
    submit_data = {'api_format':'json', 'status':'submitted'}
    res,ctt = http.request(url, 'PUT', headers=headers, body=urllib.parse.urlencode(submit_data))
    apirequest(url)

def submitall(data):
    print('开始提交')
    for r in data:
        print('%s [%s]%s ...' %('提交',r.id,r.summary))
        submit(r.id)
    print('全部提交成功')

def apirequest(url):
    try:
        print('url: ' + url)
        res,ctt = http.request(url, 'GET', headers=headers)
        print(res.status)
        return res,ctt
    except Exception as e:
        print('NG:%s' % e)
        return None,None

def parsebyfile(optiontype):
    f = open("list.htm", "r", encoding="utf_8")
    html = f.read()
    f.close()
    parsehtml(html,optiontype)

def parsebyurl(optiontype):
    start = 1
    end = 1
    login()
    for i in range(start, end+ 1):
        url = "http://172.26.184.150/reviews/dashboard/?view=outgoing"
        if not downloadPage(url,optiontype):
            print("not more content")
            break
    print('下载成功')

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
parsebyurl(option)
#parsebyfile(option)
write2html(records)
submitall(records)
print("----------处理结束----------")

