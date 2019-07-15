# coding=utf-8

from bxework import app, workwx
from bxework.config import config
from flask import jsonify, request

__conf = config()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/workwx/api/alarm/receiver', methods=['POST'])
def alarmSend():
    '''
    接收Alarmmanager的告警消息，处理后通过企业微信发送
    :return: 
    '''
    #msg1 = request.get_data().decode(encoding='utf-8')
    msg = request.get_json()
    print(msg)
    partyid = __conf.get_partyid('运维部')
    errcode = workwx.sendToK8sAPP(msg, party=partyid)
    if errcode == 0:
        return 'send msg ok'
    else:
        return 'send msg fail'


