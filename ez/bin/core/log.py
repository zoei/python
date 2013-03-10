#-*- encoding:UTF-8 -*-
'''
Created on 2012-3-28

@author: hazh
'''
import datetime
import os

LOG_NORMAL = 0
LOG_INFO = 1
LOG_DEBUG = 2
LOG_LEVEL = (1, 2)

class Log():
    LOG_NORMAL = 0
    LOG_INFO = 1
    LOG_DEBUG = 2
    LOG_LEVEL = ("NORMAL", "INFO", "DEBUG")
    LOG_MODEL = ("log", "html")
    HTML_TAG_START = ('', '<font color="blue">', '<font color="red" >')
    HTML_TAG_END = ('</br>', '</font></br>', '</font></br>')
    LOG_FILE_PATH_ROOT = "/zoei/workspace/Python/poker/WebRoot/log"

    def __init__(self, module_name, log_file = None, model = 1):
        self.module_name = module_name
        self.model = model
        if log_file is not None:
            self.log_file = log_file
        else:
            self.log_file = self.module_name
        
        date_str = str(datetime.date.today()).split("-")
        self.year = int(date_str[0])
        self.month = int(date_str[1])
        self.day = int(date_str[2])

        self.file = "%s/%s/%s/%s/%s/%s.%s" % (Log.LOG_FILE_PATH_ROOT, self.module_name,\
                                                   self.year, self.month, self.day, self.log_file, Log.LOG_MODEL[model])
        
    def log(self, info = None, level = 0, show_console = True):
        if not os.path.isfile(self.file):
            if not os.path.isdir(os.path.dirname(self.file)):
                # 创建目录
                os.makedirs(os.path.dirname(self.file))
            # 创建文件
            f = open(self.file, "w")
            f.write('''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n''')
        else:
            f = open(self.file, "a")

        content = "[%s][%s]%s\n" % (datetime.datetime.today(), Log.LOG_LEVEL[level], info)
        if show_console:
            print content
        if self.model == 1:
            f.write("%s%s%s" % (Log.HTML_TAG_START[level], content, Log.HTML_TAG_END[level]))
        else:
            f.write(content)
        f.close()

    def log_method(self, method_name, info = None, level = 0, show_console = True):
        if info is None:
            info = "start"
        self.log("%s():%s" % (method_name, info), level, show_console)

    def log_class(self, class_name, method_name, info = None, level = 0, show_console = True):
        self.log_method("%s.%s" % (class_name, method_name), info, level, show_console)

    def log_test(self):
        dt = datetime.datetime
        print dt.today()

l = Log("poker")
def log(info, level = 0, show_console = True):
    if level not in LOG_LEVEL:return
    l.log(info, level, show_console)
    
def log_method(method_name, info = None, level = 0, show_console = True):
    if level not in LOG_LEVEL:return
    l.log("%s():%s" % (method_name, info), level, show_console)

def log_class(class_name, method_name, info = None, level = 0, show_console = True):
    if level not in LOG_LEVEL:return
    l.log_method("%s.%s" % (class_name, method_name), info, level, show_console)