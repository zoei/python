#-*- encoding:UTF-8 -*-
'''
Created on 2012-5-22

@author: hazh
'''

class UserDTO():

    def __init__(self, name=None, time=None, source=None):
        if source is not None:
            self.name = source.get("name")
            self.request_time = source.get("time")
        else:
            self.name = name
            self.request_time = time

class Users():

    def __init__(self):
        self.user_list = {}
 
    def update(self, request):
        self.user_list[request.parameters.get("name")] = request.parameters.get("time")
        return None
    
    def get_time(self, name):
        return self.user_list.get(name)