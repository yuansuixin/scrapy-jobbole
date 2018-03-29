

### 爬取伯乐在线最新文章里的所有文章
##### 网址：http://blog.jobbole.com/all-posts/， 使用scrapy shell调试工具




- 爬取伯乐在线的最新文章的列表页中所有的文章url
    > 使用到的知识点

        - xpath匹配或者使用css匹配
        - yield 关键字
        - scrapy框架
        - itemLoader容器
        - 数据同步保存到mysql数据库
        - 数据异步保存到mysql数据库，使用twisted


- 使用execute函数执行scrapy的脚本，写成main函数的形式，动态获取工程目录便于调试


