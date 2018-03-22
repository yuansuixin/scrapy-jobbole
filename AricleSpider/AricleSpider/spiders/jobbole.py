# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # response 本身就带有xpath方法
    def parse(self, response):
        '''
        1.获取文章列表页中的文章url并交给scrapy下载后进行解析函数具体字段的解析
        2. 获取下一页的url并交给scrapy进行下载

        :param response:
        :return:
        '''

        # 下标是从1开始的   //*[@id="post-113740"]/div[1]/h1
        # /html/body/div[3]/div[3]/div[1]/div[1]
        # //*[@id="post-113740"]/div[1]/h1
        # 去到title
        re_selector = response.xpath('//div[@class="entry-header"]/h1/text()')
        print(response,'-----')

        #抓取到列表页中的文章url
        post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url,post_url),callback=self.parse_detail)
            print(post_url)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first('') # 两个class定位一个结点,两个class定位之间不加空格
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)



    def parse_detail(self,response):
        # 提取文章的具体字段
        title= response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·','').strip()
        #点赞，收藏
        praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        match_re = re.match('.*?(\d+).*',fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums=0
        # 评论
        comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        match_re = re.match('.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        # 正文
        content = response.xpath('//div[@class="entry"]').extract()[0]
        # 类别
        tags_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()[0]


        # 通过css选择器提取字段
        # title = response.css('.entry-header h1::text').extract()
        # create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·','').strip()
        # # 点赞，收藏
        # praise_nums = response.css('.vote-post-up h10::text').extract()[0]
        # fav_nums = response.css('.bookmark-btn::text').extract()[0]
        # match_re = re.match('.*?(\d+).*', fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        #
        # comment_nums = response.css('a[href="#article-comment"] span::text').extract()[0]
        # match_re = re.match('.*?(\d+).*', comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        # # 正文
        # content = response.css('.entry').extract()[0]
        # # 类别
        # tags_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()[0]
