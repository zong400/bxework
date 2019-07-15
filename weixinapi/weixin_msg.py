import requests

class WeixinMsg(object):
    def __init__(self, corpid, corpsecret):
        self.__corpid = corpid
        self.__corpsecret = corpsecret
        self.__token = self.__get_token()

    def __get_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(self.__corpid, self.__corpsecret)
        req = requests.get(url)
        if req.json()['errcode'] == 0:
            return req.json()['access_token']
        else:
            print('Get access token error, {}'.format(req.json()['errmsg']))

    def send_txt_msg(self, msg, agentid, user='', party=''):
        #token = self.__get_token()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(self.__token)
        text = '''{{
   "touser" : "{}",
   "toparty" : "{}",
   "msgtype" : "text",
   "agentid" : {},
   "text" : {{
       "content" : "{}"
   }},
   "safe":0
    }}'''.format(user, party, agentid, msg).encode('utf-8')
        req = requests.post(url, data=text, headers={"Content-Type": "application/json; charset=utf-8"})
        return  req.json()['errcode'], req.json()['errmsg']

    def send_markdown_msg(self, msg, agentid, user='', party=''):
        #token = self.__get_token()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(self.__token)
        text = '''{{
   "touser" : "{}",
   "toparty" : "{}",
   "msgtype": "markdown",
   "agentid" : {},
   "markdown": {{
        "content": "{}"
   }}
}}
'''.format(user, party, agentid, msg).encode('utf-8')
        req = requests.post(url, data=text, headers={"Content-Type": "application/json; charset=utf-8"})
        return req.json()['errcode'], req.json()['errmsg']