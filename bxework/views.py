# coding=utf-8

from bxework import app, workwx
from bxework.config import config
from flask import request

__conf = config()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/workwx/api/alarm/receiver', methods=['POST'])
def alarmSend():
    '''
    接收Alarmmanager的告警消息，处理后通过企业微信发送
    :return: errcode
    '''
    #msg1 = request.get_data().decode(encoding='utf-8')
    msg = request.get_json()
    print(msg)
    sendto = __conf.get_sendto()
    errcode = 0
    if sendto['type'] == 'party':
        errcode = workwx.sendToK8sAPP(msg, party=sendto['id'])
    elif sendto['type'] == 'user':
        errcode = workwx.sendToK8sAPP(msg, users=sendto['id'])
    else:
        return 'unknow type of sendto.'
    return 'send to wx, errcode: {}'.format(errcode)


