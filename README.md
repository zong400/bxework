# bxework
为Prometheus开发的基于企业微信的告警应用，使用webhook方式接收alertmanager发出的告警信息

## alertmanager配置

```yaml
receivers:
- name: 'work-wx-receiver'
  webhook_configs:
  - url: 'http://your.domain/workwx/api/alarm/receiver'
```

## bxework配置
配置文件使用json格式，放在conf/wxconfig.json
```json
{
  "name": "企业号名称",
  "corpid": "",
  "partys": [{"party_name": "运维部", "party_id": 2}],
  "app": {
    "name": "k8s",
    "secret": "",
    "agentid": ""
  }
}
```

- name：企业号名字
- partys：企业部门，可以多个
- app：接受告警信息的企业应用名字