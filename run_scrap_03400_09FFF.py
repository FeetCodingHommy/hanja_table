import subprocess

output = subprocess.run("scrapy runspider hanja_scrapy/spiders/cjk_basic_spider.py", shell=True)
print(output)