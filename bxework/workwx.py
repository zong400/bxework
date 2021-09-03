# coding = utf-8
from functools import reduce
from bxework.config import config
from weixinapi.weixin_msg import WeixinMsg
from weixinapi.weixin import Weixin
from bxework.emailsender import email
from kubernetes import client as kubeclient, config as kubeconfig
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from bxework.kafkaclient import kafkaclient
import json


__conf = config()
__corpid = __conf.get_wx_corpid()
__k8s_secret = __conf.get_wx_app_secretid()
__k8s_agentid = __conf.get_wx_app_agentid()
deploynames = ('muc', 'kq', 'notice', 'tbx', 'expense', 'enroll', 'clazzalbum', 'base', 'applet', 'pay', 'newsfeed')


def warning_status(status):
    if status == 'resolved':
        return '解除'
    elif status == 'firing':
        return '触发'
    else:
        return '状态不明'


def send_node_alert(msg, party='', users=''):
    errsum = 0
    wx = Weixin(corpid=__corpid, corpsecret=__k8s_secret, redis_pool=__conf.redis_pool)
    wxmsg = WeixinMsg(wx)
    markdown_teml = r'''`Prometheus告警`{}, {}
>详细内容：{}
>告警级别：<font color=\"warning\">{}</font>
>实例：<font color=\"info\">{}</font>
>开始时间：<font color=\"comment\">{}</font>
    '''
    for alert in msg['alerts']:
        try:
            stime = alert['startsAt']
            markdown_msg = markdown_teml.format(
                warning_status(alert['status']),
                alert['labels']['alertname'],
                alert['annotations']['description'],
                alert['labels']['severity'],
                alert['labels']['instance'],
                stime.split('.')[0].replace('T', ' '),
            )
        except KeyError as e:
            print('传入的json不存在 {} 键'.format(e))
        else:
            errcode, errmsg = wxmsg.send_markdown_msg(
                markdown_msg, __k8s_agentid, party=party, user=users
            )
            print(errcode, errmsg)
            errsum += errcode
    return errsum


def send_k8s_alert(msg, party='', users=''):
    """
        把json格式的告警消息发送到企业微信的K8s应用
        :param msg: 告警消息，json格式，例子：{
        'receiver': 'work-wx-receiver',
        'status': 'firing',
        'alerts': [{
            'status': 'resolved',
            'labels': {
                'alertname': 'ContainerMEM',
                'container_label_annotation_io_kubernetes_container_hash': '81b50c25',
                'container_label_annotation_io_kubernetes_container_ports': '[{"containerPort":8080,"protocol":"TCP"}]',
                'container_label_annotation_io_kubernetes_container_restartCount': '0',
                'container_label_annotation_io_kubernetes_container_terminationMessagePath': '/dev/termination-log',
                'container_label_annotation_io_kubernetes_container_terminationMessagePolicy': 'File',
                'container_label_annotation_io_kubernetes_pod_terminationGracePeriod': '30',
                'container_label_io_kubernetes_container_logpath': '/var/log/pods/defba5c5-9ec3-11e9-85c6-525400321d7f/web-clazzalbum/0.log',
                'container_label_io_kubernetes_container_name': 'web-clazzalbum',
                'container_label_io_kubernetes_docker_type': 'container',
                'container_label_io_kubernetes_pod_name': 'web-clazzalbum-875ff996f-zx9n9',
                'container_label_io_kubernetes_pod_namespace': 'bxr-pro',
                'container_label_io_kubernetes_pod_uid': 'defba5c5-9ec3-11e9-85c6-525400321d7f',
                'container_label_io_kubernetes_sandbox_id': '14087e5f56b23c5d70b97a148e83375e148c693d6edae53fcd0ab5e9590a5669',
                'id': '/kubepods/burstable/poddefba5c5-9ec3-11e9-85c6-525400321d7f/de3a9fb5d5c52b90244e5e2a7527fc61de5e42c814576925a238b26034cfedfe',
                'image': 'registry.bxr.cn/web-clazzalbum@sha256:478ee171619d3f8b8c792fe0749efeeb97a5a96df0c358bc3bdb8e7d8fa5ddfe',
                'instance': '172.17.173.186:8080',
                'job': 'cadvisor',
                'name': 'k8s_web-clazzalbum_web-clazzalbum-875ff996f-zx9n9_bxr-pro_defba5c5-9ec3-11e9-85c6-525400321d7f_0',
                'namespace': 'bxr-pro',
                'severity': 'warning'
            },
            'annotations': {
                'description': '容器 web-clazzalbum-875ff996f-zx9n9 可用MEMORY资源即将触及限制，当前值：4.65234375 MB。',
                'summary': '容器 web-clazzalbum-875ff996f-zx9n9 Free Memory 低'
            },
            'startsAt': '2019-07-10T09:05:09.027094078Z',
            'endsAt': '2019-07-11T00:06:09.027094078Z',
            'generatorURL': 'http://prometheus-789dfd4c68-sdkkd:9090/graph?g0.expr=abs%28container_spec_memory_limit_bytes%7Bcontainer_label_io_kubernetes_container_name%21%3D%22POD%22%2Ccontainer_label_io_kubernetes_pod_namespace%3D%22bxr-pro%22%2Cimage%21%3D%22%22%2Cname%3D~%22%5Ek8s_.%2A%22%7D+-+container_memory_working_set_bytes%7Bcontainer_label_io_kubernetes_container_name%21%3D%22POD%22%2Ccontainer_label_io_kubernetes_pod_namespace%3D%22bxr-pro%22%2Cimage%21%3D%22%22%2Cname%3D~%22%5Ek8s_.%2A%22%7D%29+%2F+1024+%2F+1024+%3C+50&g0.tab=1'
        }, ｛
            'status': 'resolved',
            'labels': {
                'alertname': 'ContainerMEM',
                'container_label_annotation_io_kubernetes_container_hash': '72eafcc8',
                'container_label_annotation_io_kubernetes_container_ports': '[{"containerPort":20880,"protocol":"TCP"}]',
                'container_label_annotation_io_kubernetes_container_restartCount': '0',
                'container_label_annotation_io_kubernetes_container_terminationMessagePath': '/dev/termination-log',
                'container_label_annotation_io_kubernetes_container_terminationMessagePolicy': 'File',
                'container_label_annotation_io_kubernetes_pod_terminationGracePeriod': '30',
                'container_label_io_kubernetes_container_logpath': '/var/log/pods/8825a3a4-9ec3-11e9-85c6-525400321d7f/core-interactive-applet/0.log',
                'container_label_io_kubernetes_container_name': 'core-interactive-applet',
                'container_label_io_kubernetes_docker_type': 'container',
                'container_label_io_kubernetes_pod_name': 'core-interactive-applet-86b9fc8d4f-k8q94',
                'container_label_io_kubernetes_pod_namespace': 'bxr-pro',
                'container_label_io_kubernetes_pod_uid': '8825a3a4-9ec3-11e9-85c6-525400321d7f',
                'container_label_io_kubernetes_sandbox_id': 'e01d4aa8298a0f908b2e0f9bf1b1b22365c1948ff7be5597c3c4ace4f524368b',
                'id': '/kubepods/burstable/pod8825a3a4-9ec3-11e9-85c6-525400321d7f/3c8f79f8a9aa06f356b37c634ca5b1fe33faccd60d132a3d2137af49b599c22f',
                'image': 'registry.bxr.cn/core-interactive-applet@sha256:cc50e645441234f07e4d9723e954b49d7f81c641b12b9c22400ebcc4b575b02e',
                'instance': '172.17.3.116:8080',
                'job': 'cadvisor',
                'name': 'k8s_core-interactive-applet_core-interactive-applet-86b9fc8d4f-k8q94_bxr-pro_8825a3a4-9ec3-11e9-85c6-525400321d7f_0',
                'namespace': 'bxr-pro',
                'severity': 'warning'
            },
            'annotations': {
                'description': '容器 core-interactive-applet-86b9fc8d4f-k8q94 可用MEMORY资源即将触及限制，当前值：2.44140625 MB。',
                'summary': '容器 core-interactive-applet-86b9fc8d4f-k8q94 Free Memory 低'
            },
            'startsAt': '2019-07-10T09:05:09.027094078Z',
            'endsAt': '2019-07-11T00:02:09.027094078Z',
            'generatorURL': 'http://prometheus-789dfd4c68-sdkkd:9090/graph?g0.expr=abs%28container_spec_memory_limit_bytes%7Bcontainer_label_io_kubernetes_container_name%21%3D%22POD%22%2Ccontainer_label_io_kubernetes_pod_namespace%3D%22bxr-pro%22%2Cimage%21%3D%22%22%2Cname%3D~%22%5Ek8s_.%2A%22%7D+-+container_memory_working_set_bytes%7Bcontainer_label_io_kubernetes_container_name%21%3D%22POD%22%2Ccontainer_label_io_kubernetes_pod_namespace%3D%22bxr-pro%22%2Cimage%21%3D%22%22%2Cname%3D~%22%5Ek8s_.%2A%22%7D%29+%2F+1024+%2F+1024+%3C+50&g0.tab=1'
        }],
        'groupLabels': {
            'alertname': 'ContainerMEM',
            'namespace': 'bxr-pro'
        },
        'commonLabels': {
            'alertname': 'ContainerMEM',
            'container_label_annotation_io_kubernetes_container_restartCount': '0',
            'container_label_annotation_io_kubernetes_container_terminationMessagePath': '/dev/termination-log',
            'container_label_annotation_io_kubernetes_container_terminationMessagePolicy': 'File',
            'container_label_annotation_io_kubernetes_pod_terminationGracePeriod': '30',
            'container_label_io_kubernetes_docker_type': 'container',
            'container_label_io_kubernetes_pod_namespace': 'bxr-pro',
            'job': 'cadvisor',
            'namespace': 'bxr-pro',
            'severity': 'warning'
        },
        'commonAnnotations': {},
        'externalURL': 'http://prometheus-789dfd4c68-sdkkd:9093',
        'version': '4',
        'groupKey': '{}/{severity="warning"}/{namespace="bxr-pro"}:{alertname="ContainerMEM", namespace="bxr-pro"}'
    }
        :param party: 通讯录的部门id
        :return: 返回微信errcode，errmsg
    """
    wx = Weixin(corpid=__corpid, corpsecret=__k8s_secret, redis_pool=__conf.redis_pool)
    wxmsg = WeixinMsg(wx)
    errsum = 0
    markdown_teml = r'''`Prometheus告警`{}, {}, {}
>详细内容：<font color=\"info\">{}</font>
>告警级别：<font color=\"warning\">{}</font>
>POD_NAME: <font color=\"comment\">{}</font>
>开始时间：<font color=\"comment\">{}</font>
>容器重启次数：<font color=\"comment\">{}</font>
>NAMESPACE：<font color=\"comment\">{}</font>
        '''
    for alert in msg['alerts']:
        try:
            stime = alert['startsAt']
            markdown_msg = markdown_teml.format(
                warning_status(alert['status']),
                alert['labels']['alertname'],
                alert['labels']['container_label_io_kubernetes_container_name'],
                alert['annotations']['description'],
                alert['labels']['severity'],
                alert['labels']['container_label_io_kubernetes_pod_name'],
                stime.split('.')[0].replace('T', ' '),
                alert['labels'][
                    'container_label_annotation_io_kubernetes_container_restartCount'
                ],
                alert['labels']['container_label_io_kubernetes_pod_namespace'],
            )
        except KeyError as e:
            print('传入的json不存在 {} 键'.format(e))
        else:
            errcode, errmsg = wxmsg.send_markdown_msg(
                markdown_msg, __k8s_agentid, party=party, user=users
            )
            errsum += errcode
    return errsum


def check_auth(user):
    if user in ('Zong', 'ethan'):
        return True
    else:
        return False


def _full_deployment_name(shortname):
    if shortname in deploynames:
        if shortname in ('muc', 'kq', 'notice', 'tbx', 'expense', 'enroll', 'clazzalbum', 'base'):
            return 'core-service-' + shortname
        elif shortname == 'applet':
            return 'core-interactive-applet'
        elif shortname == 'newsfeed':
            return 'sys-newsfeed-core'
        elif shortname == 'pay':
            return 'sys-pay-core'
    else:
        return shortname


def get_pods(deployname='all'):
    kube_conf = __conf.get_k8s_config()
    kubeconfig.load_kube_config(
        config_file=kube_conf['kubeconfig'], context=kube_conf['context']
    )
    v1 = kubeclient.CoreV1Api()
    ret = v1.list_namespaced_pod(namespace=kube_conf['namespace'])
    if deployname == 'all':
        pods = [
            {
                "pod_name": i.metadata.name,
                "pod_ip": i.status.pod_ip,
                "host_ip": i.status.host_ip,
                "status": i.status.phase,
                "restart_count": i.status.container_statuses[0].restart_count,
            }
            for i in ret.items
        ]
    elif deployname in deploynames:
        pods = [
            {
                "pod_name": i.metadata.name,
                "pod_ip": i.status.pod_ip,
                "host_ip": i.status.host_ip,
                "status": i.status.phase,
                "restart_count": i.status.container_statuses[0].restart_count,
            }
            for i in list(
                filter(
                    lambda m: m.metadata.name[: len(deployname)] == deployname,
                    ret.items,
                )
            )
        ]
    return pods


def top_pods(podname):
    kube_conf = __conf.get_k8s_config()
    kubeconfig.load_kube_config(
        config_file=kube_conf['kubeconfig'], context=kube_conf['context']
    )
    cuObj = kubeclient.CustomObjectsApi()
    try:
        resp = cuObj.list_namespaced_custom_object(
            'metrics.k8s.io', 'v1beta1', kube_conf['namespace'], 'pods'
        )
        # 筛选符合podname的数据
        pods = list(
            filter(lambda pod: podname in pod['metadata']['name'], resp['items'])
        )
        if not pods:
            return '%s 没有找到' % podname
        # 扁平化数据结构
        pods = list(
            map(
                lambda i: {
                    'pod_name': i['metadata']['name'],
                    'container_metrics': i['containers'],
                },
                pods,
            )
        )
        # 扁平化数组里面每个usage的数据结构
        for pod in pods:
            pod['container_metrics'] = list(
                map(
                    lambda i: {
                        'name': i['name'],
                        'cpu': format_top_data(i['usage']['cpu'], 'cpu'),
                        'memory': format_top_data(i['usage']['memory'], 'memory'),
                    },
                    pod['container_metrics'],
                )
            )
            if len(pod['container_metrics']) > 1:
                pod['total_cpu'] = reduce(
                    lambda a, b: a['cpu'] + b['cpu'], pod['container_metrics']
                )
                pod['total_mem'] = reduce(
                    lambda a, b: a['memory'] + b['memory'], pod['container_metrics']
                )
            elif len(pod['container_metrics']) == 1:
                pod['total_cpu'] = pod['container_metrics'][0]['cpu']
                pod['total_mem'] = pod['container_metrics'][0]['memory']
    except ApiException as e:
        print('k8s api出错，reason: %s, message: %s' % (e.reason, e.body))
    finally:
        return pods


def format_top_data(input, type):
    if type == 'cpu':
        result = round(int(input.replace('n', '')) / 1000000)
    elif type == 'memory':
        result = round(int(input.replace('Ki', '')) / 1024)
    return result


def top_nodes():
    """
    return: {'node_name': 'node1', 'cpu': 23, 'memory': 3442} cpu单位m，memory单位Mi
    """
    kube_conf = __conf.get_k8s_config()
    kubeconfig.load_kube_config(
        config_file=kube_conf['kubeconfig'], context=kube_conf['context']
    )
    cuObj = kubeclient.CustomObjectsApi()
    try:
        resp = cuObj.list_cluster_custom_object('metrics.k8s.io', 'v1beta1', 'nodes')
        nodes_metrics = list(
            map(
                lambda n: {
                    'node_name': n['metadata']['name'],
                    'cpu': format_top_data(n['usage']['cpu'], 'cpu'),
                    'memory': format_top_data(n['usage']['memory'], 'memory'),
                },
                resp['items'],
            )
        )
    except ApiException as e:
        print('k8s api出错，reason: %s, message: %s' % (e.reason, e.body))
    finally:
        return nodes_metrics


def del_pod(pod_name):
    kube_conf = __conf.get_k8s_config()
    kubeconfig.load_kube_config(
        config_file=kube_conf['kubeconfig'], context=kube_conf['context']
    )
    v1 = kubeclient.CoreV1Api()
    try:
        res = v1.delete_namespaced_pod(pod_name, kube_conf['namespace'])
        if not res.reason:
            ret = 'delete成功'
        else:
            ret = res.reason
    except ApiException as e:
        ret = 'delete失败，原因：%s' % e.reason
        print('k8s api出错，reason: %s, message: %s' % (e.reason, e.body))
    finally:
        return ret


def scale_deploy(deployname, podnum):
    if deployname:
        deployname = _full_deployment_name(deployname)
        kube_conf = __conf.get_k8s_config()
        kubeconfig.load_kube_config(
            config_file=kube_conf['kubeconfig'], context=kube_conf['context']
        )
        v1 = kubeclient.AppsV1Api()
        try:
            body = json.loads('{"spec": {"replicas": %s} }' % podnum)
            res = v1.patch_namespaced_deployment(name=deployname, namespace=kube_conf['namespace'], body=body)
            ret = f"{deployname} replicas={res.spec.replicas}"
        except ApiException as e:
            ret = 'scale失败，原因：%s' % e.reason
            print('k8s api出错，reason: %s, message: %s' % (e.reason, e.body))
        finally:
            return ret
    else:
        return 'deploy name 错误。'


def do_exec(pod_name, exec_cmd):
    kube_conf = __conf.get_k8s_config()
    kubeconfig.load_kube_config(
        config_file=kube_conf['kubeconfig'], context=kube_conf['context']
    )
    v1 = kubeclient.CoreV1Api()
    try:
        rep = stream(
            v1.connect_get_namespaced_pod_exec,
            pod_name,
            kube_conf['namespace'],
            command=exec_cmd,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False,
        )
        return rep
    except ApiException as e:
        print('k8s api出错，reason: %s, message: %s' % (e.reason, e.body))
        return None


def do_jstack(pod_name):
    exec_command = [
        "/bin/sh",
        "-c",
        "JPID=`ps|grep jar|grep -v tini|grep -v grep|awk {'print $1'}` && /usr/lib/jvm/java-1.8-openjdk/bin/jstack -l $JPID",
    ]
    # exec_command = ["/bin/sh", "-c", "ps"]
    jdump = do_exec(pod_name, exec_command)
    if jdump:
        mail = email()
        mail.send_mail('%s 的dump结果' % pod_name, jdump)
        return {"status": 0, "msg": "ok"}
    else:
        return {"status": 1, "msg": "fail"}


def arthas(pod_name, command):
    exec_command = [
        "/bin/sh",
        "-c",
        "JPID=`ps|grep jar|grep -v tini|grep -v grep|awk {'print $1'}` && java -jar arthas/arthas-boot.jar -c '%s' $JPID" % command
    ]
    result = do_exec(pod_name, exec_command)
    if result:
        mail = email()
        mail.send_mail('%s 的arthas分析结果' % pod_name, result)
        return {"status": 0, "msg": "ok"}
    else:
        return {"status": 1, "msg": "fail"}


def set_zk(key, value):
    exec_command = ["/bin/sh", "-c", f"bin/zkCli.sh -server localhost:2181 set /wbyb/{key} {value}"]
    result = do_exec("zk3-k8s-node4.bxr.cn", exec_command)
    return "done"


def send_warn_to_kafka(waring):
    """
    发告警信息到kafka
    :param warings:
    :return:
    """
    kafka = kafkaclient(['10.22.0.18:9092'])
    # res = kafka.send('k8swarning', {"node": "node4", "status": "not ready", "message": "node offline"})
    res = kafka.send('k8swarning', waring)
        #logging.debug('send waring to kafka ' + res)
    #logging.info('send to kafka complete.')