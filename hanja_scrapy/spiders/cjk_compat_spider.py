import scrapy

import os
import pandas as pd
from urllib.parse import urlencode
from warnings import warn

from hanja_scrapy.settings import OUTPUT_PATH

class CJKCompatSpider(scrapy.Spider):
    """scrap [CJK Compatibility Ideographs]

    U+F900 ~ U+FAD9 : CJK Compatibility Ideographs
    
    총 474개의 한자 및 음가 값 크롤링
    """
    name = "cjk_compat_spider"
    # allowed_domains = ["https://m.dic.daum.net/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'hanja_scrapy.middlewares.HanjaScrapyDownloaderMiddleware': 100
        }
    }

    def __init__(self, *args, **kwargs):
        base_url = "https://m.dic.daum.net/search.do?"
        
        self.query_urls = list()

        WANTED_RANGE = (int("0xF900", 16), int("0xFAD9", 16))

        for unicode_num in range(WANTED_RANGE[0], WANTED_RANGE[1]+1):
            query_url = base_url + urlencode({'q': chr(unicode_num), "dic": "hanja", "crawling_num": hex(unicode_num).replace("0x", '').upper()})
            self.query_urls.append(query_url)
 
    def start_requests(self):
        for url in self.query_urls:
            # dont_filter=True: 동일 요청으로 보고 필터링해서 첫 페이지만 긁는 현상 방지
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8', dont_filter=True)
 
    def parse(self, response):
        hanja_unicode = response.url.split("crawling_num=")[-1]
        if len(hanja_unicode) != 4:
            warn("Wrong hanja unicode")
            hanja_unicode = ''
        else:
            hanja_unicode = "U+" + hanja_unicode
        hangul_eumga = response.xpath('//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/strong/a[2]/text()').get()
        if hangul_eumga is None:
            warn("No hangul eumga")
            hangul_eumga = ''
        else:
            hangul_eumga = hangul_eumga.strip()
            hangul_eumgas = [hangul_eumga] if ", " not in hangul_eumga else hangul_eumga.split(", ")
            hangul_eumgas = [ he[-1] for he in hangul_eumgas ]
            different_eumgas = list()
            for he in hangul_eumgas:
                if he not in different_eumgas:
                    different_eumgas.append(he)
            hangul_eumga = ','.join(different_eumgas)
        
        if not os.path.exists(os.path.join(OUTPUT_PATH, "cjk_compat.csv")):
            pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga]
            }).to_csv(os.path.join(OUTPUT_PATH, "cjk_compat.csv"), index=False)
        else:
            pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga]
            }).to_csv(os.path.join(OUTPUT_PATH, "cjk_compat.csv"), index=False, mode='a', header=False)
