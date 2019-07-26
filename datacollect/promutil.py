# coding = utf-8

import requests

class promutil():
    def __init__(self, promdomain):
        self.__promdomain = promdomain

    def total_mem_percen(self):
        query = r'ceil(sum(container_memory_working_set_bytes{id="/"})/sum(machine_memory_bytes)*100)'
        params = {'query': query}
        url = 'http://{}/api/v1/query'.format(self.__promdomain)
        req = requests.get(url, params=params)
        json_data = req.json()
        if not json_data['status'] == 'success':
            return 'query fail. errorType: {}, error: {}'.format(json_data['errorType'], json_data['error'])
        return json_data['data']['result'][0]['value'][1]

    def container_free_mem(self, namespace, topn=5):
        '''
        获取可用内存最少的5个pod
        :param namespace: k8s的namespacen
        :param topn: 获取前N个值
        :return: 返回pod名字和内存值的字典，{podname1:freemem, podname2:freemem}
        '''
        query = r'sort(round(abs(container_spec_memory_limit_bytes{{container_label_io_kubernetes_container_name!="POD",container_label_io_kubernetes_pod_namespace="{ns}",image!="",name=~"^k8s_.*"}}- container_memory_working_set_bytes{{container_label_io_kubernetes_container_name!="POD",container_label_io_kubernetes_pod_namespace="{ns}",image!="",name=~"^k8s_.*"}})/1024/1024))'.format(ns=namespace)
        params = {'query': query}
        url = 'http://{}/api/v1/query'.format(self.__promdomain)
        req = requests.get(url, params=params)
        json_data = req.json()
        if not json_data['status'] == 'success':
            return 'query fail. errorType: {}, error: {}'.format(json_data['errorType'], json_data['error'])
        podnames = []
        values = []
        results = json_data['data']['result']
        for res in results[:topn]:
            podnames.append(res['metric']['container_label_io_kubernetes_pod_name'])
            values.append(res['value'][1])
        result_dict = {'podnames' : podnames, 'values' : values}
        return result_dict
