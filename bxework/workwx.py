# coding = utf-8
from bxework.config import config
from weixinapi.weixin_msg import WeixinMsg

__conf = config()
__corpid = __conf.get_wx_corpid()
__k8s_secret = __conf.get_wx_app_secretid()
__k8s_agentid = __conf.get_wx_app_agentid()

def warning_status(status):
    if status == 'resolved':
        return '解除'
    elif status == 'firing':
        return '触发'
    else:
        return '状态不明'

def sendToK8sAPP(msg, party='', users=''):
    '''
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
    '''
    wx = WeixinMsg(__corpid, __k8s_secret)
    errsum = 0
    markdown_teml = r'''`Prometheus告警`{}, {}, {}
-详细内容：<font color=\"info\">{}</font>
-告警级别：<font color=\"warning\">{}</font>
-POD_NAME: <font color=\"comment\">{}</font>
-开始时间：<font color=\"comment\">{}</font>
-容器重启次数：<font color=\"comment\">{}</font>
-NAMESPACE：<font color=\"comment\">{}</font>
        '''
    for alert in msg['alerts']:
        try:
            stime = alert['startsAt']
            markdown_msg = markdown_teml.format(warning_status(alert['status']),
                                                alert['labels']['alertname'],
                                                alert['labels']['container_label_io_kubernetes_container_name'],
                                                alert['annotations']['description'],
                                                alert['labels']['severity'],
                                                alert['labels']['container_label_io_kubernetes_pod_name'],
                                                stime.split('.')[0].replace('T', ' '),
                                                alert['labels']['container_label_annotation_io_kubernetes_container_restartCount'],
                                                alert['labels']['container_label_io_kubernetes_pod_namespace'])
        except KeyError as e:
            print('传入的json不存在 {} 键'.format(e))
        else:
            errcode, errmsg = wx.send_markdown_msg(markdown_msg, __k8s_agentid, party=party, user=users)
            errsum += errcode
    return errsum
