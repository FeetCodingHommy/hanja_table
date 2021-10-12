import subprocess

output = subprocess.run("scrapy runspider hanja_scrapy/spiders/cjk_extb_spider_waks.py", shell=True)
print(output)