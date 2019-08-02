# coding = utf-8

import requests
import time
from .DataCollectException import DataCollectError

class promutil():
    def __init__(self, promdomain):
        self.__promdomain = promdomain

    def __exec_query(self, query):
        params = {'query': query}
        url = 'http://{}/api/v1/query'.format(self.__promdomain)
        req = requests.get(url, params=params)
        data = req.json()
        if not data['status'] == 'success':
            raise DataCollectError(data['errorType'], data['error'])
        return req.json()

    def bad_request(self):
        query = r'sum(rate(traefik_backend_requests_total{protocol=~"http|https",code=~"(^4\\d{2}|^5\\d{2})",backend=~"(bxr|www).banxiaoer.net.*"}[1h]))'
        try:
            json_data = self.__exec_query(query)
        except DataCollectError as e:
            print(e)
        else:
            return json_data['data']['result'][0]['value'][1]

    def normal_request(self):
        query = r'sum(traefik_backend_requests_total{code=~"(^2\\d{2}|^3\\d{2})",backend=~"(bxr|www).banxiaoer.net.*",method!="HEAD"}) by (backend)'
        normal_req = []
        try:
            json_data = self.__exec_query(query)
        except DataCollectError as e:
            print(e)
        else:
            results = json_data['data']['result']
            for res in results:
                normal_req.append({'value': res['value'][1], 'name': res['metric']['backend']})
        finally:
            return normal_req


    def request_rate(self, min=60):
        '''
        过去min分钟的请求变化率，间隔5min取样一次
        :param min:
        :return:
        '''
        query = r'ceil(sum(irate(traefik_backend_requests_total[5m] offset {}m)))'
        query_now = r'ceil(sum(irate(traefik_backend_requests_total[5m])))'
        last = 5
        now = time.time()
        times = [time.strftime('%H:%M', time.localtime(now))]
        values = []
        try:
            val = self.__exec_query(query_now)
            values.append(val['data']['result'][0]['value'][1])
            while last < min:
                val = self.__exec_query(query.format(last))
                values.append(val['data']['result'][0]['value'][1])
                last_time = time.strftime('%H:%M', time.localtime(now-last*60))
                times.append(last_time)
                last += 5
        except DataCollectError as e:
            print(e)
        finally:
            return {'times': times, 'values': values}

    def pod_cpu_usage(self, namespace, topn=5):
        query = r'topk({}, sort_desc(sum (rate (container_cpu_usage_seconds_total{{image!="",name=~"^k8s_.*",container_label_io_kubernetes_pod_namespace="{}"}}[1m])) by (container_label_io_kubernetes_pod_name)))'.format(topn, namespace)
        podnames = []
        values = []
        try:
            json_data = self.__exec_query(query)
        except DataCollectError as e:
            print(e)
        else:
            results = json_data['data']['result']
            for res in results:
                podnames.append(res['metric']['container_label_io_kubernetes_pod_name'])
                values.append(res['value'][1][:5])
        finally:
            return {'podnames': podnames, 'values': values}

    def total_cpu_percen(self):
        query = r'ceil(sum (rate (container_cpu_usage_seconds_total{id="/"}[1m])) / sum (machine_cpu_cores) * 100)'
        try:
            json_data = self.__exec_query(query)
        except DataCollectError as e:
            print(e)
        else:
            return json_data['data']['result'][0]['value'][1]

    def total_mem_percen(self):
        '''
        集群的总内存使用率
        :return:
        '''
        query = r'ceil(sum(container_memory_working_set_bytes{id="/"})/sum(machine_memory_bytes)*100)'
        try:
            json_data = self.__exec_query(query)
        except DataCollectError as e:
            print(e)
        else:
            return json_data['data']['result'][0]['value'][1]


    def container_free_mem(self, namespace, topn=5):
        '''
        获取可用内存最少的5个pod
        :param namespace: k8s的namespacen
        :param topn: 获取前N个值
        :return: 返回pod名字和内存值的字典，{podname1:freemem, podname2:freemem}
        '''
        query = r'topk({top}, sort(round(abs(container_spec_memory_limit_bytes{{container_label_io_kubernetes_container_name!="POD",container_label_io_kubernetes_pod_namespace="{ns}",image!="",name=~"^k8s_.*"}}- container_memory_working_set_bytes{{container_label_io_kubernetes_container_name!="POD",container_label_io_kubernetes_pod_namespace="{ns}",image!="",name=~"^k8s_.*"}})/1024/1024)))'.format(top=topn, ns=namespace)
        podnames = []
        values = []
        try:
            json_data = self.__exec_query(query)
        except DataCollectError as e:
            print(e)
        else:
            results = json_data['data']['result']
            for res in results:
                podnames.append(res['metric']['container_label_io_kubernetes_pod_name'])
                values.append(res['value'][1])
        finally:
            return {'podnames' : podnames, 'values' : values}
