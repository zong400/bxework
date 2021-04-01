import json
from datacollect.redisdb import Redisdb

class config(object):
    def __init__(self):
        self.__config = self.__open_config_file('conf/wxconfig.json')
        self.__dsconfig = self.__open_config_file('conf/dsconfig.json')

    def __open_config_file(self, path):
        with open(path, mode='r', encoding='utf8') as f:
            conf = json.load(f)
        return conf

    @property
    def redis_pool(self):
        return Redisdb.redis_pool(**self.__dsconfig['redis'])

    @property
    def prometheus_domain(self):
        return self.__dsconfig['prometheus_domain']

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

    def get_callback(self):
        return self.__config['callback']['token'], self.__config['callback']['EncodingAESKey']

    def get_k8s_config(self):
        return self.__dsconfig['kubernetes']

    @property
    def domain(self):
        return self.__config['domain']