import redis

class Redisdb(object):
    def __init__(self, redis_pool):
        self.pool = redis_pool

    @staticmethod
    def redis_pool(host='127.0.0.1', port=6379, password='123456', db=0, decode_responses=True, **kwargs):
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=db, decode_responses=decode_responses)
        return pool

    def get_redis_conn(self, host=None, port=None, password=None, **kwargs):
        if host and port and password:
            return redis.StrictRedis(host, port, password, decode_responses=True)
        elif host and password:
            return redis.StrictRedis(host, password, decode_responses=True)
        elif self.pool:
            return redis.StrictRedis(connection_pool=self.pool)
        else:
            return 'get redis connection fail.'

    def hsetval(self, key, mapping, conn=None):
        if conn:
            rds = conn
        else:
            rds = self.get_redis_conn()
        res = rds.hmset(key, mapping)
        return res

    def hgetallval(self, key, conn=None):
        if conn:
            rds = conn
        else:
            rds = self.get_redis_conn()
        return rds.hgetall(key)

    def getval(self, key, conn=None):
        if conn:
            rds = conn
        else:
            rds = self.get_redis_conn()
        res = rds.get(key)
        return res
