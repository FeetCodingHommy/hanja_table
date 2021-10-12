import scrapy

import os
import pandas as pd
from warnings import warn

from hanja_scrapy.settings import OUTPUT_PATH

class CJKExtBSpiderWAKS(scrapy.Spider):
    """scrap [CJK Unified Ideographs Extension B] from waks.aks.ac.kr

    U+20000 ~ U+0x2A6DF : CJK Unified Ideographs Extension B
      * U+20000 → http://waks.aks.ac.kr/unicode/#/view?uniCode=U+20000
      * U+2A6DF → http://waks.aks.ac.kr/unicode/#/view?uniCode=U+2A6DF
    
    총 42720개의 한자 및 음가 값 크롤링
    """
    name = "cjk_extb_spider_waks"
    # allowed_domains = ["http://waks.aks.ac.kr/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'hanja_scrapy.middlewares.HanjaScrapyDownloaderMiddleware': 100
        }
    }

    def __init__(self, *args, **kwargs):
        base_url = "http://waks.aks.ac.kr/unicode/#/view?uniCode=U+"
        
        self.query_urls = list()

        WANTED_RANGE = list(range(int("0x20000", base=0), int("0x2A6DF", base=0)+1))

        for unicode_num in WANTED_RANGE:
            unicode_hex = hex(unicode_num).replace("0x", '').upper()
            query_url = base_url + unicode_hex
            self.query_urls.append(query_url)
 
    def start_requests(self):
        for url in self.query_urls:
            # dont_filter=True: 동일 요청으로 보고 필터링해서 첫 페이지만 긁는 현상 방지
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8', dont_filter=True)
 
    def parse(self, response):
        hanja_unicode = response.url.split("uniCode=")[-1]
        if hanja_unicode is None:
            warn("No hanja unicode")
            return None
        
        hangul_eumga = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[4]/td[1]/text()').get()
        if response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[4]/th[1]/text()').get() != "한글자음":
            warn("Not hangul eumga")
            hangul_eumga = ''
        if hangul_eumga is None:
            warn("No hangul eumga")
            hangul_eumga = ''
        else:
            hangul_eumga = hangul_eumga.strip().replace(';', ',')

        try:
            info = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[8]/th/text()').get()
            if info == "자형정보":
                match_type = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[2]/td[1]/text()').get()
                match_hanja_unicode = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[8]/td/table/tbody/tr[2]/td[3]/a/text()').get()
                if type(match_hanja_unicode) is str:
                    match_hanja_unicode = match_hanja_unicode.replace("U+0", "U+")
            else:
                match_type = ''
                match_hanja_unicode = ''
        except Exception as e:
            print(e)
            match_type = ''
            match_hanja_unicode = ''
        
        if not os.path.exists(os.path.join(OUTPUT_PATH, "cjk_extb_waks.csv")):
            pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga],
                "match_hanja_unicode": [match_hanja_unicode],
                "match_type": [match_type]
            }).to_csv(os.path.join(OUTPUT_PATH, "cjk_extb_waks.csv"), index=False)
        else:
            pd.DataFrame.from_dict({
                "hanja_unicode": [hanja_unicode],
                "hangul_eumga": [hangul_eumga],
                "match_hanja_unicode": [match_hanja_unicode],
                "match_type": [match_type]
            }).to_csv(os.path.join(OUTPUT_PATH, "cjk_extb_waks.csv"), index=False, mode='a', header=False)
