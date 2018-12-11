## AddCdnDomain.json配置说明
refer to: https://help.aliyun.com/document_detail/91176.html?spm=a2c4g.11186623.6.678.19c319e0pFxi1v
```
[
  // 依次对应添加域名输入框， 从上到下
  {
    "DomainName": "domain-test",    // 加速域名
    "CdnType": "download",    // 业务类型, 可选为web: 图片及小文件分发; download: 大文件下载加速
    // 依次对应基本配置->源站配置修改配置输入框
    // type:源站类型， 可选为 ipaddr: ip源站; domain: 域名源站; oss: OSS bucket为源站
    // content: 回源地址，可以是IP或域名
    // port: 可以指定443,80端口
    // priority: 源站地址对应的优先级，默认20。
    // weight: 回源权重，默认10
    "Sources":"[{\"type\": \"domain\",\"content\": \"test-domain.com\",\"port\": \"443\",\"priority\": \"20\", \"weight\": \"10\"}]",
    "Scope": "domestic"    // 可选值为 domestic, overseas, global
  }
]
```
