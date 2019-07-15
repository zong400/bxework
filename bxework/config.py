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

    def get_partyid(self):
        '''
        返回部门id，如果没找到部门默认返回第一个
        :param name: 企业号名字
        :param party_name: 部门名字
        :return: partyid
        '''
        return self.__config['party']['party_id']

