# coding=utf-8

from bxework import app, workwx
from bxework.config import config
from datacollect.promutil import promutil
#from datacollect.redisdb import Redisdb
#from weixinapi.weixin import Weixin
from flask import request, render_template, g
import weixinapi.WXCallback as wxcb

__conf = config()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/workwx/api/callback', methods=['GET', 'POST'])
def wx_callback():
    get_args = request.args
    if "echostr" in get_args:
        return wxcb.verfiy_echo(get_args)
    if request.method == 'POST':
        content, msg_type, touser, create_time = wxcb.received_from_wx(get_args, request.data)
        print(content, msg_type, touser, create_time)
        return content

@app.route('/workwx/api/prom/traefikstatus')
def reqrate():
    prom = promutil(__conf.prometheus_domain)
    rate = prom.request_rate()
    urlreqs = prom.normal_request()
    badreqs = prom.bad_request()
    return render_template('request_rate.html', rate=rate, urlreqs=urlreqs, badreqs=badreqs)

@app.route('/workwx/api/prom/freemem', methods=['GET'])
def freemem():
    namespace = request.args.get('namespace')
    prom = promutil(__conf.prometheus_domain)
    podmem = prom.container_free_mem(namespace)
    mem_percen = prom.total_mem_percen()
    return render_template('freemem_chart.html', freemem=podmem, mem_percen=mem_percen)

@app.route('/workwx/api/prom/cpuusage')
def cpuusage():
    namespace = request.args.get('namespace')
    #prom = promutil('prometheus:9090')
    prom = promutil(__conf.prometheus_domain)
    podcpu = prom.pod_cpu_usage(namespace)
    cpupercen = prom.total_cpu_percen()
    return render_template('cpu_usage_chart.html', podcpu=podcpu, cpupercen=cpupercen)

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
