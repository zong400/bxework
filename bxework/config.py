import json

class config(object):
    def __init__(self):
        self.__config = self.__open_config_file('conf/wxconfig.json')

    def __open_config_file(self, path):
        with open(path, mode='r', encoding='utf8') as f:
            conf = json.load(f)
        return conf

    def get_wx_corpid(self):
        return self.__config['corpid']

    def get_wx_app_secretid(self):
        return self.__config['app']['secret']

    def get_wx_app_agentid(self):
        return self.__config['app']['agentid']

    def get_sendto(self):
        id = self.__config['sendto']['id']
        type = self.__config['sendto']['type']
        return {"id":id ,"type":type}

