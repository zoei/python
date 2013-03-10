#-*- encoding:UTF-8 -*-
'''
Created on 2012-5-22

@author: hazh
'''

from message import MessageDTO, MessageList
from user import Users


class JSONControl():
    def __init__(self):
        pass

    def doit(self, request):
        print(request.path)
        jid = request.parameters.get("jid")
        return eval("json_%s(request)" % jid)

message_list = MessageList()
users = Users()

'''add message'''
def json_1001(request):
    message_list.insert(0, MessageDTO(source=request.parameters))
    return json_1002(request)

'''get message'''
def json_1002(request):
    last_request_time = users.get_time(request.parameters.get("name"))
    if last_request_time is None:
        last_request_time = 0
    josn_message = message_list.get_json_message(request.parameters, last_request_time)
    users.update(request)
    return josn_message

'''get address'''
def json_1003(request):
    return '{"host":"%s"}' % request.parameters.get('host')
