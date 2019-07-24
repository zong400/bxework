from .WXBizMsgCrypt import WXBizMsgCrypt
from bxework.config import config

def __get_wxcrypt():
    conf = config()
    token, EncodingASEKey = conf.get_callback()
    corpid = conf.get_wx_corpid()
    return WXBizMsgCrypt(token, EncodingASEKey, corpid)

def verfiy_echo(request_args):
    wxcrypt = __get_wxcrypt()
    ret, sReplyEchoStr = wxcrypt.VerifyURL(request_args['msg_signature'], request_args['timestamp'], request_args['nonce'], request_args['echostr'])
    if ret != 0:
        return 'error: verify fail, errcode: {}'.format(ret)
    return sReplyEchoStr

