import scrapy
from idoldc.items import IdoldcItem
import logging
import re
from bs4 import BeautifulSoup
import json
from datetime import datetime
from tqdm import tqdm

class ArticleSpider(scrapy.Spider):
    name = "idoldc"
    headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'}

    def start_requests(self):
        """This method returns the first Requests to crawl for this spider.
        """
        self.PAGE = 1 # the start page
        self.LAST_PAGE = int(self.N) # the last page
        self.pbar = tqdm(range(self.LAST_PAGE - 1))
        self.LAST_POSTID = -1
        self.GALLERY = self.BASEURL.split('id=')[-1].strip()
        if self.BASEURL.find('mgallery') > -1:
            self.TYPE = 'mgallery'
        elif self.BASEURL.find('mini') > -1:
            self.TYPE = 'mini'
        else:
            self.TYPE = 'gallery'
        next_page = f'{self.BASEURL}&page={self.PAGE}&list_num=100'
        
        yield scrapy.Request(url=next_page, callback=self.parse_list)
    
    def parse_list(self, response):
        """This method collects the meta information of the posts in the current page.
        """
        item = IdoldcItem()
        logging.info(response.url)
        post_num = 0 # count posts collected in the current page

        soup = BeautifulSoup(response.body, 'html.parser')
        post_list = soup.select('tr.ub-content')
        for post in post_list:
            if post.has_attr('data-no'):
                post_num += 1
                if self.parse_title(item, post, response):
                    item['gall_type'] = self.TYPE
                    item['gallery'] = self.GALLERY
                    item['referer'] = response.url
                    yield item

        self.PAGE += 1

        if self.PAGE == self.LAST_PAGE:
            self.pbar.close()
            logging.info("Last Page = {}".format(response.url))
        else:
            self.pbar.update()
            next_page = f'{self.BASEURL}&page={self.PAGE}&list_num=100'
            yield response.follow(next_page, callback=self.parse_list)

    def parse_title(self, info, e, response):
        """This method collects the detailed information of the given post.
        """
        post_type = e.select_one('a > em').get('class')[1]
        info['post_type'] = post_type
        info['title'] = e.a.text
        post_id = e.select_one('td.gall_num').text
        info['post_id'] = post_id
        if post_type in ['icon_pic','icon_recomimg', 'icon_txt'] :
            self.PREVIOUS_POSTID = int(post_id)
        else :
            self.PREVIOUS_POSTID = self.LAST_POSTID + 1 # @ if [notice] posts are always more than @LAST_POSTID
        info['url'] = e.a.get('href').split('&list_num')[0]
        try:
            info['reply_num'] = e.select_one('a.reply_numbox')
            if info['reply_num'] :
                info['reply_num'] = info['reply_num'].text
                info['reply_num'] = re.findall('\d+',info['reply_num'])[0]
            else:
                info['reply_num'] = 0
            info['usernick'] = e.select_one('td.gall_writer').get('data-nick')
            info['userid'] = e.select_one('td.gall_writer').get('data-uid')
            info['userip'] = e.select_one('td.gall_writer').get('data-ip')
            uploaded_date = e.select_one('td.gall_date').get('title')
            info['uploaded_date'] = datetime.strptime(uploaded_date,'%Y-%m-%d %H:%M:%S')
            info['gall_count'] = e.select_one('td.gall_count').text
            info['gall_recommend'] = e.select_one('td.gall_recommend').text
        except:
            logging.warning(e)
            info['error'] = True
            post_url = 'http://m.dcinside.com/board/{0}/{1}'.format(self.GALLERY, info['post_id'])
            return response.follow(post_url, callback=self.parse_post, meta={'info': info }, headers=self.headers)
        else:
            info['error'] = False
            return info
