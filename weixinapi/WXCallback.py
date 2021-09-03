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
    '''
    接收消息解密后示例：b'<xml><ToUserName><![CDATA[ww521ad0239051c73b]]></ToUserName>
                            <FromUserName><![CDATA[YangWeiZong]]></FromUserName>
                            <CreateTime>1616579111</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[get.pod]]></Content>
                            <MsgId>6943154417203579909</MsgId>
                            <AgentID>1000002</AgentID>
                            </xml>'
    '''
    wxcrypt = __get_wxcrypt()
    ret, xml_content = wxcrypt.DecryptMsg(post_data, get_args['msg_signature'], get_args['timestamp'], get_args['nonce'])
    # print(xml_content)
    if ret != 0:
        return 'Crypt error, code: {}'.format(ret)
    xml_tree = ET.fromstring(xml_content)
    msg_type = xml_tree.find('MsgType').text
    touser = xml_tree.find('ToUserName').text
    fromuser = xml_tree.find('FromUserName').text
    create_time = xml_tree.find('CreateTime').text
    event_key = xml_tree.find('EventKey').text
    event = xml_tree.find('Event').text
    # msgid = xml_tree.find('MsgId').text
    content = ''
    if msg_type == 'text':
        content = xml_tree.find('Content').text
        return msg_type, content, touser, fromuser, create_time
    if msg_type == 'event' and event == 'click':
        content = event_key
        return msg_type, content, touser, fromuser, create_time
    

def EncryptMsg(toUser, createTime, content, nonce):
    rDataXML = '''<xml>
       <ToUserName><![CDATA[{}]]></ToUserName>
       <FromUserName><![CDATA[ww521ad0239051c73b]]></FromUserName> 
       <CreateTime>{}</CreateTime>
       <MsgType><![CDATA[text]]></MsgType>
       <Content><![CDATA[{}]]></Content>
    </xml>'''.format(toUser, createTime, content)
    wxcrypt = __get_wxcrypt()
    ret, sEncryptMsg = wxcrypt.EncryptMsg(rDataXML, nonce)
    if ret != 0:
        return 'Crypt error, code: {}'.format(ret)
    # sEncryptMsg 加密消息，xml格式
    return sEncryptMsg