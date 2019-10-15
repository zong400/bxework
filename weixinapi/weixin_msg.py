import requests
from .weixin import TokenExpiredError

class WeixinMsg(object):
    def __init__(self, Weixin):
        self.__weixin = Weixin

    def _message_send_wx(self, text):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(self.__weixin.token)
        req = requests.post(url, data=text.encode('utf-8'), headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            if req.json()['errcode'] == 40014:
                raise TokenExpiredError(self.__weixin)
            errcode = req.json()['errcode']
            errmsg = req.json()['errmsg']
            return errcode, errmsg
        except TokenExpiredError as e:
            print(e)
            errcode, errmsg = self._message_send_wx(text)
            return errcode, errmsg
        except Exception as e:
            print(e)
            return 1, e


    def send_txt_msg(self, msg, agentid, user='', party=''):
        #token = self.__get_token()
        text = '''{{
   "touser" : "{}",
   "toparty" : "{}",
   "msgtype" : "text",
   "agentid" : {},
   "text" : {{
       "content" : "{}"
   }},
   "safe":0
    }}'''.format(user, party, agentid, msg)
        errcode, errmsg = self._message_send_wx(text)
        return  errcode, errmsg

    def send_markdown_msg(self, msg, agentid, user='', party=''):
        #token = self.__get_token()
        text = '''{{
   "touser" : "{}",
   "toparty" : "{}",
   "msgtype": "markdown",
   "agentid" : {},
   "markdown": {{
        "content": "{}"
   }}
}}
'''.format(user, party, agentid, msg)
        errcode, errmsg = self._message_send_wx(text)
        return errcode, errmsg