from .WXBizMsgCrypt import WXBizMsgCrypt
from bxework.config import config
from urllib import parse
import xml.etree.cElementTree as ET

def __get_wxcrypt():
    conf = config()
    token, EncodingASEKey = conf.get_callback()
    corpid = conf.get_wx_corpid()
    return WXBizMsgCrypt(token, EncodingASEKey, corpid)

def verfiy_echo(get_args):
    wxcrypt = __get_wxcrypt()
    sEchoStr = parse.unquote(get_args['echostr'], encoding='utf-8', errors='replace')
    ret, sReplyEchoStr = wxcrypt.VerifyURL(get_args['msg_signature'], get_args['timestamp'], get_args['nonce'], sEchoStr)
    if ret != 0:
        return 'error: verify fail, errcode: {}'.format(ret)
    return sReplyEchoStr

def received_from_wx(get_args, post_data):
    wxcrypt = __get_wxcrypt()
    ret, xml_content = wxcrypt.DecryptMsg(post_data, get_args['msg_signature'], get_args['timestamp'], get_args['nonce'])
    if ret != 0:
        return 'Crypt error, code: {}'.format(ret)
    xml_tree = ET.fromstring(xml_content)
    content = xml_tree.find('Content').text
    msg_type = xml_tree.find('MsgType').text
    touser = xml_tree.find('ToUserName').text
    fromuser = xml_tree.find('FromUserName').text
    create_time = xml_tree.find('CreateTime').text
    print(xml_content)
    return content, msg_type, touser, fromuser, create_time

def reply_to_user(msg, get_args):
    wxcrypt = __get_wxcrypt()
    ret, xml = wxcrypt.EncryptMsg(msg, get_args['nonce'])
    if ret != 0:
        return 'Crypt error, code: {}'.format(ret)
    print(xml)
    return xml