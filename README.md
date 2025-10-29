# WebServer 基準測試

## 簡介

研究 WebServer 的基準測試，框架與系統結構，以下研究應包括：

+ WebServer
  - .NET Core API
  - Gunicorn ( Single-worker ) + Flask
  - Uvicorn ( Single-worker ) + FastAPI
  - Gunicorn + Uvicorn ( Multi-worker ) + FastAPI
  - Nginx Loadbalacer + Gunicorn + Uvicorn ( Multi-worker ) + FastAPI
  - Nginx Loadbalacer + Uvicorn ( Single-worker ) + FastAPI
  - Nginx Loadbalacer + .NET Core API

+ Async API test tools
  - Apache JMeter
  - Python Locust

執行內容為以下部分：

+ 數值運算 ```curl http://localhost/api/add/[number_1]/[number_2]```
+ 字串處理 ```curl http://localhost/api/str/[origin_string]/[target_character]/[replace_character]```

評估標準：

+ 在不同發送端數量下，在每 10 秒內可完成多少次執行
    - 計算在固定送端數量、測試請求單位提升時的總時間、最大、最小、平均、中位數
    - 伺服器中央處理運用、記憶體量的最大、最小、平均值

## 執行

+ 啟動環境，例如 dotnet
```
bm dotnet
```
+ 進入 ISA
```
bm dotnet --into
```
+ 進入伺服器
```
bm dotnet --into=server
```
+ 進入測試
```
bm dotnet --into=tester
```

## 議題

### 基本單元比對

.NET Core API >> Uvicorn ( Single-worker ) + FastAPI > Gunicorn ( Single-worker ) + Flask

### 負載平衡

Nginx Loadbalacer + .NET Core API << .NET Core API

+ 無論怎麼調整 Nginx 都限制在 30000 請求，檢查各 Worker ( .NET Core API ) 的 CPU、MEM 使用率皆不高
    - 關機重新測試，狀態恢復到與單一容器相似，偶發現象
    - 提高 Docker Desktop 可用核心數上限 ( 預設為 2 )，約落提高上限
+ 略過負載平衡 ( Server )，直接透過域名分流 ( Worker )
    - 直接使用域名分流可以達到與單體的需求執行數
    - 負載平衡與域名分流的需求執行數約莫為 1:1.5 ~ 1:3 的差別
    - 負載平衡下的工作單元，在 CPU 使用率有相似的曲線，域名分流則會出現不平均的現象
    - 可能疑慮
        + Nginx 最大吞吐量限制
            - 在 Nginx 單容器測試下排除此項可能
        + Nginx 流程影響
            - 議題
                + 擴展數為 1
                + 透過 Upstream 直接指定網址
                + 透過 Prxoy_Pass 直些指定網址
            - 出現固定的不穩定區間，動吞吐量沒變
        + Nginx proxy 限制
            - [Module ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
            - nginx proxy_pass throughput
                + ```worker_processes``` and ```worker_connections```: Proper tuning of these directives to match your system's resources (CPU cores, available file descriptors) is crucial.
                + ```proxy_buffering```: By default, Nginx buffers responses from the backend. While beneficial for managing slow clients and protecting backends, disabling it (proxy_buffering off;) can sometimes improve performance for specific scenarios where the backend can serve data quickly and directly to the client.
                + ```proxy_read_timeout```, ```proxy_send_timeout```, ```client_body_timeout```, ```client_header_timeout```: Adjusting these timeouts can prevent connections from being held open unnecessarily and improve resource utilization.
            - 關閉 ```proxy_buffering``` 將吞吐量提升一倍
+ Python 伺服器不穩定執行數問提
    - 無論在單一容器、擴展容器、增加執行程序數狀況皆會出現
        + 發生期間，會有相應 CPU 使用率低落
        + 在相同測試中，特定 vus 區間會發生相似狀況
    - 補充測試
        + 指定 VUS 下的長時間測試

## 文獻

+ [Gunicorn](https://gunicorn.org/)
    - [uWSGI 配置參數講解](https://www.maxlist.xyz/2020/06/20/flask-uwsgi/)
    - [Uvicorn, Gunicorn, Daphne, and FastAPI: A Guide to Choosing the Right Stack](https://medium.com/@ezekieloluwadamy/76ffaa169791)
        + Uvicorn handles HTTP requests efficiently. Gunicorn manages multiple Uvicorn instances, enabling scalability. By combining them, you get the best of both worlds: Uvicorn’s speed and Gunicorn’s stability for production.
+ [Grafana K6](https://k6.io/)
    - [讓開發人員如沐春風的壓力測試工具 - K6](https://blog.darkthread.net/blog/k6-load-testing/)
+ 彙整
    - [SCMP vs MCSP](./dcos/scmp-vs-mcsp.md)
    - [Load Balancing](./docs/load-balancing.md)
    - [API Gateway vs Load balacer vs Reverse Proxy](./docs/api-gateway-vs-load-balancer-vs-reverse-proxy.md)
