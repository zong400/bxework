# coding=utf-8

from bxework import app, workwx
from bxework.config import config
from flask import request
import weixinapi.WXCallback as wxcb

__conf = config()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/workwx/api/callback', methods=['GET', 'POST'])
def wx_callback():
    req = request.args
    if "echostr" in req:
        return wxcb.verfiy_echo(req)
    if request.method == 'POST':
        pass


@app.route('/workwx/api/pod/receiver', methods=['POST'])
def send_pod_alert():
    '''
    接收Alarmmanager发出的Kubernetes的告警消息，处理后通过企业微信发送
    :return: errcode
    '''
    #msg1 = request.get_data().decode(encoding='utf-8')
    msg = request.get_json()
    sendto = __conf.get_sendto()
    if sendto['type'] == 'party':
        errcode = workwx.send_k8s_alert(msg, party=sendto['id'])
    elif sendto['type'] == 'user':
        errcode = workwx.send_k8s_alert(msg, users=sendto['id'])
    else:
        return 'unknow type of sendto.'
    return 'send to wx, errcode: {}'.format(errcode)

@app.route('/workwx/api/node/receiver', methods=['POST'])
def send_node_alert():
    '''
    接收Alarmmanager发出的node的告警消息，处理后通过企业微信发送
    :return:
    '''
    msg = request.get_json()
    sendto = __conf.get_sendto()
    if sendto['type'] == 'party':
        errcode = workwx.send_node_alert(msg, party=sendto['id'])
    elif sendto['type'] == 'user':
        errcode = workwx.send_node_alert(msg, users=sendto['id'])
    else:
        return 'sunknow type of sendto.'
    return 'send to wx, errcode: {}'.format(errcode)
