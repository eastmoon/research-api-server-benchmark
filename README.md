# 研究 API Server 基準測試

## 簡介

研究 API Server 的基準測試方法、框架與系統結構，以下研究應包括伺服器：

+ API Server
  - .NET Core API
  - Gunicorn ( Single-worker ) + Flask
  - Gunicorn + Uvicorn ( Multi-worker ) + FastAPI
  - Nginx Loadbalacer + .NET Core API
  - Nginx Loadbalacer + Gunicorn ( Multi-worker ) + Flask
  - Nginx Loadbalacer + Gunicorn + Uvicorn ( Multi-worker ) + FastAPI

執行內容為以下部分：

+ 響應回應 ```curl http://localhost/```
+ 數值運算 ```curl http://localhost/api/add/[number_1]/[number_2]```
+ 字串處理 ```curl http://localhost/api/str/[origin_string]/[target_character]/[replace_character]```

評估標準：

+ 在不同發送端數量下，在每 10 秒內可完成多少次執行
    - 計算在固定送端數量、測試請求單位提升時的總時間、最大、最小、平均、中位數
    - 伺服器中央處理運用、記憶體量的最大、最小、平均值
+ 在固定發送端數量、固定執行秒數下，執行指定次數
    - 計算在測試請求單位提升時的總時間、最大、最小、平均、中位數
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

+ 各 Worker ( .NET Core API ) 的 CPU、MEM 使用率皆不高
    - 提高 Docker Desktop 可用核心數上限 ( 預設為 2 )，約落提高上限
+ 略過負載平衡 ( Server )，直接透過域名分流 ( Worker )
    - 直接使用域名分流可以達到與單體的需求執行數
    - 負載平衡與域名分流的需求執行數約莫為 1:1.5 ~ 1:3 的差別
    - 負載平衡下的工作單元，在 CPU 使用率有相似的曲線，域名分流則會出現不平均的現象
+ 附載平衡調整
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

## 文獻

+ [Gunicorn](https://gunicorn.org/)
    - [uWSGI 配置參數講解](https://www.maxlist.xyz/2020/06/20/flask-uwsgi/)
    - [Uvicorn, Gunicorn, Daphne, and FastAPI: A Guide to Choosing the Right Stack](https://medium.com/@ezekieloluwadamy/76ffaa169791)
        + Uvicorn handles HTTP requests efficiently. Gunicorn manages multiple Uvicorn instances, enabling scalability. By combining them, you get the best of both worlds: Uvicorn’s speed and Gunicorn’s stability for production.
+ [Grafana K6](https://k6.io/)
    - [讓開發人員如沐春風的壓力測試工具 - K6](https://blog.darkthread.net/blog/k6-load-testing/)

### 文獻彙整

#### SCMP vs MCSP

對於單一容器多執行程序 ( SCMP、Single Container, Multiple Processes ) 與多容器單一執行程序 ( MCSP、Multiple Containers, Single Process )，在結構與效能差異約莫如下：

+ 容器執行效能花費：每個容器啟動會佔用容器管理系統的服務效能，因此啟動越多容器會造成效能花費擴大。
+ 資源利用率：多容器可以細膩的再利用與分配資源，從而提高主機整體的資源利用率。
+ 執行程序間通訊：SCMP 可利用 ICP 讓執行程序通訊，MCSP 則利用 API 或共享 Socket 讓執行程序間通訊。
+ 可擴展性：SCMP 內部結構複雜，不利擴展或擴展容易產生資源佔用的死結衝突，MCSP 則是內部結構單純，容器擴展且資源可分配。

若遵守微服務設計原則就使用 MCSP，若對執行程序間有高溝通效率要求就使用 SCMP。

#### Load Balancing vs Single Server

+ [Load Balancing VS Clustering](https://medium.com/@kapare.sushant23/load-balancing-vs-clustering-6620cffb0969)
+ [What is the difference between a reverse proxy and a load balancer?](https://www.f5.com/glossary/reverse-proxy-vs-load-balancer)
+ [All You Need to Know About Load Balancing](https://www.dnsstuff.com/load-balancing-tools)
+ [Load Balancing Deep Dive: Algorithms, Types, and Use-Cases](https://stonefly.com/resources/load-balancing-algorithms-types-use-cases/)

負載平衡將流量分配到多台伺服器以提高效能和可靠性，而單一伺服器則單獨處理所有請求，這種方式更簡單，但可擴展性和可靠性較差。主要區別在於，負載平衡提供高可用性和可擴展性，但增加了複雜性；而單一伺服器易於管理，但隨著需求的增長，會成為瓶頸和單點故障。

| Feature | Load Balancing | Single Server |
| :-: | :--- | :--- |
| Architecture | Multiple servers work together as a "server farm". | A single server handles all traffic and data. |
| Scalability | Highly scalable; can easily add more servers to handle increased demand. | Limited scalability; performance degrades and it may crash under heavy load. |
| Performance | Improves performance by distributing the load, reducing latency, and preventing any single server from being overwhelmed. | Performance is limited by the capacity of the single server and can become a bottleneck. |
| Availability/Reliability | High availability; if one server fails, the others can continue to operate, and traffic is redistributed. | Low availability; if the single server fails, the entire application goes down, creating a single point of failure. |
| Complexity | High; requires more complex setup, management, and infrastructure. | Low; simple to set up and manage for basic applications. |
| Cost | Higher initial and ongoing costs due to more hardware, software, and management overhead. | Lower initial and ongoing costs. |
| Use Case | Ideal for applications with high traffic, critical uptime requirements, and the need for fault tolerance. | Suitable for small applications with low traffic and no critical uptime requirements. |


#### API gateway vs Load balancer vs Reverse proxy

+ [Load Balancer vs. Reverse Proxy vs. API Gateway: Demystifying Web Architectures](https://www.designgurus.io/blog/load-balancer-reverse-proxy-api-gateway)
+ [Load Balancer vs Reverse Proxy vs API Gateway](https://medium.com/codenx/load-balancer-vs-reverse-proxy-vs-api-gateway-fcb79912abbf)
+ [Load Balancer vs Reverse Proxy vs API Gateway](https://blog.algomaster.io/p/load-balancer-vs-reverse-proxy-vs-api-gateway)
+ [API Gateway vs Reverse Proxy vs Load Balancer: Understanding the Differences](https://api7.ai/learning-center/api-gateway-guide/api-gateway-vs-reverse-proxy-vs-load-balancer)

##### Reverse Proxy:

+ Function: A reverse proxy sits in front of one or more web servers, intercepting client requests and forwarding them to the appropriate backend server. It acts as an intermediary, hiding the backend server's identity and providing a single public-facing endpoint.
+ Key Features: Security (hiding internal network details), caching static content, SSL termination, URL rewriting.
+ Analogy: A receptionist who directs visitors to the correct department within an office, without the visitors needing to know the internal layout.

##### Load Balancer:

+ Function: A load balancer distributes incoming network traffic across multiple servers in a server farm. Its primary goal is to ensure high availability, scalability, and optimal resource utilization.
+ Key Features: Traffic distribution algorithms (e.g., round robin, least connections), health checks to remove unhealthy servers, session persistence.
+ Analogy: A traffic controller directing cars to different lanes on a highway to prevent congestion and ensure smooth flow.

##### API Gateway:

+ Function: An API gateway acts as a single entry point for all API requests to a backend system, especially common in microservices architectures. It handles various cross-cutting concerns before routing requests to specific backend services.
+ Key Features: Request routing, authentication and authorization, rate limiting, logging and monitoring, request/response transformation, protocol translation.
+ Analogy: A concierge at a hotel who manages all guest requests, handles various services (reservations, room service), and directs guests to the appropriate facilities.

##### Relationship and Overlap:
+ A reverse proxy can provide basic load balancing functionality, but a dedicated load balancer offers more sophisticated algorithms and features for traffic distribution.
+ An API gateway often incorporates reverse proxy and load balancing capabilities as part of its broader functionality. It sits at a higher level, focusing on API-specific concerns and service orchestration.
+ It is common to see these components layered, with a reverse proxy or load balancer handling initial traffic, and an API gateway managing API-specific interactions with backend services.
