import scrapy

import os
import pandas as pd
from warnings import warn

from hanja_scrapy.settings import OUTPUT_PATH

class CJKBasicSpider(scrapy.Spider):
    """scrap [CJK Unified Ideographs Extension A] and [CJK Unified Ideographs]

    U+3400 ~ U+4DBF : CJK Unified Ideographs Extension A
      * U+3400 → http://www.koreanhistory.or.kr/newchar/list_view.jsp?code=1
      * U+4DBF → http://www.koreanhistory.or.kr/newchar/list_view.jsp?code=6582
    U+4E00 ~ U+9FA5 : CJK Unified Ideographs
      * U+4E00 → http://www.koreanhistory.or.kr/newchar/list_view.jsp?code=6583
      * U+9FA5 → http://www.koreanhistory.or.kr/newchar/list_view.jsp?code=27484
    
    총 27484개의 한자 및 음가 값 크롤링
    """
    name = "cjk_basic_spider"
    # allowed_domains = ["http://www.koreanhistory.or.kr/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'hanja_scrapy.middlewares.HanjaScrapyDownloaderMiddleware': 100
        }
    }

    def __init__(self, *args, **kwargs):
        base_url = "http://www.koreanhistory.or.kr/newchar/list_view.jsp?code="
        
        self.query_urls = list()

        WANTED_RANGE = (1, 27484)

        for unicode_num in range(WANTED_RANGE[0], WANTED_RANGE[1]+1):
            query_url = base_url + str(unicode_num)
            self.query_urls.append(query_url)
 
    def start_requests(self):
        for url in self.query_urls:
            # dont_filter=True: 동일 요청으로 보고 필터링해서 첫 페이지만 긁는 현상 방지
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8', dont_filter=True)
 
    def parse(self, response):
        hanja_unicode = response.xpath('//*[@id="box"]/table/tbody/tr[4]/td[4]/text()').get()
        if hanja_unicode is None:
            warn("No hanja unicode")
            return None
        else:
            hanja_unicode = hanja_unicode.strip()
        hangul_eumga = response.xpath('//*[@id="box"]/table/tbody/tr[14]/td[2]/text()').get()
        if hangul_eumga is None:
            warn("No hangul eumga")
            hangul_eumga = ''
        else:
            hangul_eumga = hangul_eumga.strip()
        
        if not os.path.exists(os.path.join(OUTPUT_PATH, "cjk_basic.csv")):
            pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga]
            }).to_csv(os.path.join(OUTPUT_PATH, "cjk_basic.csv"), index=False)
        else:
            pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga]
            }).to_csv(os.path.join(OUTPUT_PATH, "cjk_basic.csv"), index=False, mode='a', header=False)
