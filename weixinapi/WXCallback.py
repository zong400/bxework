from .WXBizMsgCrypt import WXBizMsgCrypt
from bxework.config import config
from urllib import parse

def __get_wxcrypt():
    conf = config()
    token, EncodingASEKey = conf.get_callback()
    corpid = conf.get_wx_corpid()
    return WXBizMsgCrypt(token, EncodingASEKey, corpid)

def verfiy_echo(request_args):
    wxcrypt = __get_wxcrypt()
    sEchoStr = parse.unquote(request_args['echostr'], encoding='utf-8', errors='replace')
    ret, sReplyEchoStr = wxcrypt.VerifyURL(request_args['msg_signature'], request_args['timestamp'], request_args['nonce'], sEchoStr)
    if ret != 0:
        return 'error: verify fail, errcode: {}'.format(ret)
    return sReplyEchoStr

