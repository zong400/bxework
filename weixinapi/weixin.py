import requests
import time
from datacollect.redisdb import Redisdb

class Weixin(object):
    def __init__(self, corpid, corpsecret, redis_pool):
        self.__corpid = corpid
        self.__corpsecret = corpsecret
        self.__redis_pool = redis_pool

    def _get_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(self.__corpid,
                                                                                            self.__corpsecret)
        req = requests.get(url)
        if req.json()['errcode'] == 0:
            token = req.json()['access_token']
            rds = Redisdb(self.__redis_pool)
            rds.hsetval('wxtoken', {"token": token, "token_time": time.time_ns()})
            return token
        else:
            print('Get access token error, {}'.format(req.json()['errmsg']))
            return None

    @property
    def token(self):
        rds = Redisdb(self.__redis_pool)
        res = rds.hgetallval('wxtoken')
        if not res:
            # 没有缓存重新获取
            return self._get_token()
        elif time.time_ns() - int(res['token_time']) < 7200 * 1000000000:
            # 当前时间 - 缓存时间 < 7200s 就返回缓存token
            return res['token']
        else:
            # 过期重新获取
            return self._get_token()

    def update_token(self):
        self._get_token()

class WeixinError(Exception):
    def __init__(self):
        pass

class TokenExpiredError(WeixinError):
    def __init__(self, Weixin):
        Weixin.update_token()
    def __str__(self):
        return '40014 - 不合法的access_token，尝试重新获取'
