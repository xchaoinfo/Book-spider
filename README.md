# Book-spider

### requirenments

- scrapy>=1.1.1
- scrapy-fake-useragent 产生动态的 User-Agent
- scrapy-proxies 配置后可以使用 IP 代理
- mysql-connector 连接 MySQL 数据库
可以使用 `pip` 来安装需要依赖的模块
` pip install -r requirenments.txt`

mysql-connector 安装遇到问题可以参考 
[install mysql-connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html)

### 数据库结构

 - id -- [确定书籍的唯一性，hash.md5(name+packed)]
 - url -- [书籍的商品的 URL]
 - name -- [书名]
 - packed -- [装帧方式]
 - comments_num -- [评论数]
 - price -- [价格]

创建数据库的语句
```
CREATE DATABASE bookspider DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
```

创建数据表的语句
```
CREATE TABLE IF NOT EXISTS `amazon_book`
(
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    url VARCHAR(500),
    name VARCHAR(50),
    packed VARCHAR(10),
    comments_num int(6),
    price decimal(10,2)
) charset utf8 collate utf8_general_ci
```
数据库的信息的配置请在 settings 设置
