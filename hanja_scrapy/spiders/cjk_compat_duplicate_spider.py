import scrapy
from scrapy.selector import Selector

import os
import pandas as pd
import re

from hanja_scrapy.settings import OUTPUT_PATH

class CJKCompatDuplicateSpider(scrapy.Spider):
    """scrap [CJK Compatibility Ideographs] duplicate characters data

    U+F900 ~ U+FAD9 : CJK Compatibility Ideographs
      * https://namu.wiki/w/완성형/중복%20한자
    
    총 474개의 한자, 매칭된 통합 한자 값 및 음가 값 크롤링
    """
    name = "cjk_compat_duplicate_spider"
    # allowed_domains = ["https://namu.wiki/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'hanja_scrapy.middlewares.HanjaScrapyDownloaderMiddleware': 100
        }
    }

    def __init__(self, *args, **kwargs):
        # TO-DO: 나무위키 크롤링 시 robot 검사 페이지로 이동.
        # base_url = "https://namu.wiki/w/%EC%99%84%EC%84%B1%ED%98%95/%EC%A4%91%EB%B3%B5%20%ED%95%9C%EC%9E%90"
        base_url = "file:///home/hommy_ubuntu/Repositories/hanja_table/temp.html"
        
        self.query_urls = [base_url]

        self.hangul_regex = re.compile("[가-힣]")
 
    def start_requests(self):
        for url in self.query_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')
 
    def parse(self, response):
        # 5.1. 두 번 중복(일반)
        namuwiki_5_1 = response.xpath('//*[@id="app"]/div/div[2]/article/div[3]/div[2]/div/div/div[11]/div[2]/table').get()
        namuwiki_5_1 = Selector(text=namuwiki_5_1)

        skip_first = True
        for tr in namuwiki_5_1.xpath("//tr").getall():
            if skip_first:
                skip_first = False
                continue
            tr = Selector(text=tr)

            hanja_unicode = "U+" + tr.xpath("//tr/td[2]/div/code/text()").get()
            hangul_eumga = tr.xpath("//tr/td[2]/div").get()
            regex_obj = self.hangul_regex.search(hangul_eumga)
            hangul_eumga = regex_obj.group()[0]
            match_hanja_unicode = "U+" + tr.xpath("//tr/td[1]/div/code/text()").get()
            match_hangul_eumga = tr.xpath("//tr/td[1]/div").get()
            regex_obj = self.hangul_regex.search(match_hangul_eumga)
            match_hangul_eumga = regex_obj.group()[0]
            match_type = tr.xpath("//tr/td[3]/div/text()").get()

            self.save_parse_result(pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga],
                "match_hanja_unicode": [match_hanja_unicode],
                "match_hangul_eumga": [match_hangul_eumga],
                "match_type": [match_type]
            }))

        # 5.2. 두 번 중복(두음)
        namuwiki_5_2 = response.xpath('//*[@id="app"]/div/div[2]/article/div[3]/div[2]/div/div/div[12]/div[2]/table').get()
        namuwiki_5_2 = Selector(text=namuwiki_5_2)

        skip_first = True
        for tr in namuwiki_5_2.xpath("//tr").getall():
            if skip_first:
                skip_first = False
                continue
            tr = Selector(text=tr)

            hanja_unicode = "U+" + tr.xpath("//tr/td[2]/div/code/text()").get()
            hangul_eumga = tr.xpath("//tr/td[2]/div").get()
            regex_obj = self.hangul_regex.search(hangul_eumga)
            hangul_eumga = regex_obj.group()[0]
            match_hanja_unicode = "U+" + tr.xpath("//tr/td[1]/div/code/text()").get()
            match_hangul_eumga = tr.xpath("//tr/td[1]/div").get()
            regex_obj = self.hangul_regex.search(match_hangul_eumga)
            match_hangul_eumga = regex_obj.group()[0]
            match_type = tr.xpath("//tr/td[3]/div/text()").get()

            self.save_parse_result(pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga],
                "match_hanja_unicode": [match_hanja_unicode],
                "match_hangul_eumga": [match_hangul_eumga],
                "match_type": [match_type]
            }))

        # 5.3. 세 번 중복
        namuwiki_5_3 = response.xpath('//*[@id="app"]/div/div[2]/article/div[3]/div[2]/div/div/div[13]/div[1]/table').get()
        namuwiki_5_3 = Selector(text=namuwiki_5_3)

        skip_first = True
        for tr in namuwiki_5_3.xpath("//tr").getall():
            if skip_first:
                skip_first = False
                continue
            tr = Selector(text=tr)

            hanja_unicode_1 = "U+" + tr.xpath("//tr/td[3]/div/code/text()").get()
            hangul_eumga_1 = tr.xpath("//tr/td[2]/div").get()
            regex_obj = self.hangul_regex.search(hangul_eumga_1)
            hangul_eumga_1 = regex_obj.group()[0]
            hanja_unicode_2 = "U+" + tr.xpath("//tr/td[3]/div/code/text()").get()
            hangul_eumga_2 = tr.xpath("//tr/td[3]/div").get()
            regex_obj = self.hangul_regex.search(hangul_eumga_2)
            hangul_eumga_2 = regex_obj.group()[0]
            match_hanja_unicode = "U+" + tr.xpath("//tr/td[1]/div/code/text()").get()
            match_hangul_eumga = tr.xpath("//tr/td[1]/div").get()
            regex_obj = self.hangul_regex.search(match_hangul_eumga)
            match_hangul_eumga = regex_obj.group()[0]
            match_type_1 = tr.xpath("//tr/td[4]/div/text()").get()
            match_type_2 = tr.xpath("//tr/td[5]/div/text()").get()

            self.save_parse_result(pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode_1, hanja_unicode_2],
                "hangul_eumga": [hangul_eumga_1, hangul_eumga_2],
                "match_hanja_unicode": [match_hanja_unicode, match_hanja_unicode],
                "match_hangul_eumga": [match_hangul_eumga, match_hangul_eumga],
                "match_type": [match_type_1, match_type_2]
            }))

        # 5.4. 네 번 중복
        namuwiki_5_4 = response.xpath('//*[@id="app"]/div/div[2]/article/div[3]/div[2]/div/div/div[14]/div[1]/table').get()
        namuwiki_5_4 = Selector(text=namuwiki_5_4)

        skip_first = True
        for tr in namuwiki_5_4.xpath("//tr").getall():
            if skip_first:
                skip_first = False
                continue
            tr = Selector(text=tr)

            hanja_unicode_1 = "U+" + tr.xpath("//tr/td[3]/div/code/text()").get()
            hangul_eumga_1 = tr.xpath("//tr/td[2]/div").get()
            regex_obj = self.hangul_regex.search(hangul_eumga_1)
            hangul_eumga_1 = regex_obj.group()[0]
            hanja_unicode_2 = "U+" + tr.xpath("//tr/td[3]/div/code/text()").get()
            hangul_eumga_2 = tr.xpath("//tr/td[3]/div").get()
            regex_obj = self.hangul_regex.search(hangul_eumga_2)
            hangul_eumga_2 = regex_obj.group()[0]
            hanja_unicode_3 = "U+" + tr.xpath("//tr/td[4]/div/code/text()").get()
            hangul_eumga_3 = tr.xpath("//tr/td[4]/div").get()
            regex_obj = self.hangul_regex.search(hangul_eumga_3)
            hangul_eumga_3 = regex_obj.group()[0]
            match_hanja_unicode = "U+" + tr.xpath("//tr/td[1]/div/code/text()").get()
            match_hangul_eumga = tr.xpath("//tr/td[1]/div").get()
            regex_obj = self.hangul_regex.search(match_hangul_eumga)
            match_hangul_eumga = regex_obj.group()[0]
            match_type_1 = tr.xpath("//tr/td[5]/div/text()").get()
            match_type_2 = tr.xpath("//tr/td[6]/div/text()").get()
            match_type_3 = tr.xpath("//tr/td[7]/div/text()").get()

            self.save_parse_result(pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode_1, hanja_unicode_2, hanja_unicode_3],
                "hangul_eumga": [hangul_eumga_1, hangul_eumga_2, hangul_eumga_3],
                "match_hanja_unicode": [match_hanja_unicode, match_hanja_unicode, match_hanja_unicode],
                "match_hangul_eumga": [match_hangul_eumga, match_hangul_eumga, match_hangul_eumga],
                "match_type": [match_type_1, match_type_2, match_type_3]
            }))

    def save_parse_result(self, pandas_dataframe):
        if not os.path.exists(os.path.join(OUTPUT_PATH, "cjk_compat_duplicate.csv")):
            pandas_dataframe.to_csv(os.path.join(OUTPUT_PATH, "cjk_compat_duplicate.csv"), index=False)
        else:
            pandas_dataframe.to_csv(os.path.join(OUTPUT_PATH, "cjk_compat_duplicate.csv"), index=False, mode='a', header=False)
