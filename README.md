## ShaishufangCrawler
Use scrapy crawl shaishufang.com

## 根据uid抓取isbn
```bash
./runUID uid
```
程序运行完成后会在当前文件夹生成uid-isbns.csv文件

## 批量爬取
```bash
./run
```

## 通过HTTP URL的方式获取
1, 首先启动服务器
```bash
python Server.py
```

2, 访问链接，给定uid，获取isbn
```bash
GET http://localhost:5000/uid/1
```
