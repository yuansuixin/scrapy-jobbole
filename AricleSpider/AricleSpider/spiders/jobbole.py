# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from AricleSpider.items import JobBoleArticleItem,ArticleItemLoader
from AricleSpider.utils.common import get_md5


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
        # re_selector = response.xpath('//div[@class="entry-header"]/h1/text()')
        # print(response,'-----')

        #抓取到列表页中的文章url
        # post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract() # 一旦调用extract()，就变成了数组，无法进行二次调用
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            # 这个地方有一个问题，如果封面不是文章的第一个图片，那么怎么将封面传递给response呢，
            # 需要加一个参数meta，（重要）
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url,post_url),meta={'front_image_url':image_url},callback=self.parse_detail)
            print(post_url)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first('') # 两个class定位一个结点,两个class定位之间不加空格
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)



    def parse_detail(self,response):
        article_item = JobBoleArticleItem()
        # 提取文章的具体字段
        # title= response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·','').strip()
        # #点赞，收藏
        # praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        # fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        # match_re = re.match('.*?(\d+).*',fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums=0
        # # 评论
        # comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        # match_re = re.match('.*?(\d+).*', comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # # 正文
        # content = response.xpath('//div[@class="entry"]').extract()[0]
        # # 类别
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tags = ','.join(tag_list)
        # print('*******88',tag_list)
        # print(type(tag_list))
        # print(tags)


        # article_item['url_object_id'] = get_md5(response.url)
        # print(front_image_url)
        # article_item['title'] = title
        # article_item['url'] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date,'%Y%m/%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now()
        # article_item['create_date'] = create_date
        # article_item['front_image_url'] = [front_image_url]
        # article_item['praise_nums'] = praise_nums
        # article_item['comment_nums'] = comment_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['tags'] = tags
        # article_item['content'] = content



        front_image_url = response.meta.get('front_image_url', '')  # 文章封面图
        # 通过item——loader加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        # 选择之后再添加值
        item_loader.add_css('title','.entry-header h1::text')
        #直接添加值
        item_loader.add_value('url',response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        print(get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()


        #直接传递到pipelines中去
        yield article_item



        # 通过css选择器提取字段
        #
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
