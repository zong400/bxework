# bxework
为Prometheus开发的基于企业微信的告警应用，使用webhook方式接收alertmanager发出的告警信息

## 启动
使用flask框架，推荐使用docker部署

### bxework配置
配置文件使用json格式，放在conf/wxconfig.json，请自行创建
```json
{
  "name": "企业号名称",
  "corpid": "",
  "sendto": {"name": "运维部", "id": 2, "type": "party"},
  "app": {
    "name": "k8s",
    "secret": "",
    "agentid": ""
  }
}
```

- name：企业号名字
- sendto: 指定发送给谁，可以是部门或者用户，由type指定
> - 例如发送给张三李四，id是微信号，人员必须已经加入企业号，{"name": "张三、李四", "id": "zhangsan|lisi", "type": "user"}  
- app：接受告警信息的企业应用名字

### 启动
推荐使用docker镜像，需要自行把wxconfig.json挂载进镜像
```
docker run -v /your/conf:/Bxework/conf -p 8800:8800
```
不使用docker可以直接git clone后用gunicorn运行：
```
gunicorn -w 1 bxework:app
```
> 项目依赖flask、requests，请先安装

## alertmanager配置
添加一个receiver：
```yaml
receivers:
- name: 'work-wx-receiver'
  webhook_configs:
  - url: 'http://your.domain/workwx/api/alert/receiver'
```


