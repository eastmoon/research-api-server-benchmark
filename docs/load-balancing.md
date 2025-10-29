## Load Balancing

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
