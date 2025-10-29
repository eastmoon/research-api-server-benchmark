## SCMP vs MCSP

對於單一容器多執行程序 ( SCMP、Single Container, Multiple Processes ) 與多容器單一執行程序 ( MCSP、Multiple Containers, Single Process )，在結構與效能差異約莫如下：

+ 容器執行效能花費：每個容器啟動會佔用容器管理系統的服務效能，因此啟動越多容器會造成效能花費擴大。
+ 資源利用率：多容器可以細膩的再利用與分配資源，從而提高主機整體的資源利用率。
+ 執行程序間通訊：SCMP 可利用 ICP 讓執行程序通訊，MCSP 則利用 API 或共享 Socket 讓執行程序間通訊。
+ 可擴展性：SCMP 內部結構複雜，不利擴展或擴展容易產生資源佔用的死結衝突，MCSP 則是內部結構單純，容器擴展且資源可分配。

若遵守微服務設計原則就使用 MCSP，若對執行程序間有高溝通效率要求就使用 SCMP。
