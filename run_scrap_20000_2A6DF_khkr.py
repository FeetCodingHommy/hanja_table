import subprocess

output = subprocess.run("scrapy runspider hanja_scrapy/spiders/cjk_extb_spider_khkr.py", shell=True)
print(output)