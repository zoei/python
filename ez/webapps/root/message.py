#-*- encoding:UTF-8 -*-
'''
Created on 2012-5-22

@author: hazh
'''

class MessageDTO():

    def __init__(self, name=None, message=None, time=None, source=None):
        if source is not None:
            self.name = source.get("name")
            self.message = source.get("message")
            self.time = source.get("time")
        else:
            self.name = name
            self.message = message
            self.time = time

    def to_json(self):
        return '{"name":"%s", "message":"%s", "time":%s}' % (self.name, self.message, self.time)

class MessageList():

    def __init__(self):
        self.message_list = []

    def insert(self, index, new_message):
        self.message_list.insert(index, new_message)
        self.resize()
        return None
    
    def append(self, new_message):
        self.message_list.append(new_message)
        self.resize()
        return None
    
    def resize(self):
        print(len(self.message_list))
        while len(self.message_list) >= 50:
            self.message_list.pop()

    def get_json_message(self, parameters, last_request_time):
        json_message = '';
        for message in self.message_list:
            if message.time > last_request_time:
                if json_message == '':
                    json_message = '%s]' % (message.to_json())
                else:                
                    json_message = '%s,%s' % (message.to_json(), json_message)
        if json_message !='':
            json_message = '[' + json_message
            print(json_message)
            return json_message
        else:
            return None
