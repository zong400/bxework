# coding=utf-8
from bxework import app, workwx
from bxework.config import config
from datacollect.promutil import promutil
#from datacollect.redisdb import Redisdb
#from weixinapi.weixin import Weixin
from flask import request, render_template, url_for
import weixinapi.WXCallback as wxcb
import time
from datetime import datetime

 
__conf = config()

@app.route('/')
def hello_world():
    #workwx.top_pods('web-tbx')
    return 'Hello World!!!'

@app.route('/workwx/api/callback', methods=['GET', 'POST'])
def wx_callback():
    get_args = request.args
    if "echostr" in get_args:
        return wxcb.verfiy_echo(get_args)
    if request.method == 'POST':
        content, touser, fromuser, create_time = wxcb.received_from_wx(get_args, request.data)
        commandStr = content.split(' ')[0]
        if commandStr == 'del.pod':
            argsStr = content.split(' ')[1]
            rContent = workwx.del_pod(argsStr)
        elif commandStr == 'get.pod':
            argsStr = content.split(' ')[1]
            url = __conf.domain + url_for('k8s_pod', deployname=argsStr)
            rContent = '点击链接查看: <a href="%s">%s pods</a>' % (url, argsStr)
        elif commandStr == 'top.pod':
            argsStr = content.split(' ')[1]
            rContent = ''.join(map(lambda s: 'Pod name: {}, cpu: {}m, memory: {}Mi \n'.format(s['pod_name'], s['total_cpu'], s['total_mem']), workwx.top_pods(argsStr)))
        elif commandStr == 'scale':
            argsStr = content.split(' ')[1:]
            rContent = workwx.scale_deploy(*argsStr)
        elif commandStr == 'help':
            url = __conf.domain + '/static/help.html'
            rContent = '点击链接查看：<a href="%s">help</a>' % url
        else:
            rContent = content
        return wxcb.EncryptMsg(fromuser, int(time.time() * 1000), rContent, get_args['nonce'])

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

@app.route('/workwx/api/k8s/pod/<deployname>', methods=['GET'])
def k8s_pod(deployname):
    if deployname in ('muc', 'kq', 'notice', 'tbx', 'expense', 'enroll', 'clazzalbum', 'base'):
        deployname = 'core-service-' + deployname
    elif deployname == 'applet':
        deployname = 'core-interactive-applet'
    elif deployname == 'newsfeed':
        deployname = 'sys-newsfeed-core'
    elif deployname == 'pay':
        deployname = 'sys-pay-core'
    pods = workwx.get_pods(deployname)
    return render_template('get_pod.html', pods=pods)

@app.route('/workwx/api/k8s/top/nodes')
def k8s_top_node():
    nodes_metrics = workwx.top_nodes()
    #node_names, node_cpus, node_mems = zip(*[(me['node_name'], me['cpu'], me['memory']) for me in nodes_metrics])
    return render_template('top_nodes.html', nodes_metrics=nodes_metrics)

@app.route('/workwx/api/k8s/dojstack/<podname>', methods=['GET'])
def k8s_pod_jstack(podname):
    workwx.arthas(podname, "thread -n 5;thread -b")
    # workwx.do_jstack(podname)
    return "done"

@app.route('/workwx/api/alarm', methods=['POST'])
def send_alarm_to_EIT():
    msg = request.get_data(as_text=True)
    alarm = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "hadoop",
                "name": "hadoop",
                "massage": msg,
            }
    workwx.send_warn_to_kafka(alarm)
    return "done"
