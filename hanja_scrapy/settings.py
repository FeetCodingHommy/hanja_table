BOT_NAME = 'hanja_scrapy'

SPIDER_MODULES = ['hanja_scrapy.spiders']
NEWSPIDER_MODULE = 'hanja_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "poor_little_student (https://github.com/FeetCodingHommy)"

# Not obeying robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True



# My Settings
# 참고: "를 CHROMEDRIVER_PATH에 사용하면 selenium.common.exceptions.WebDriverException 발생
CHROMEDRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"
OUTPUT_PATH = "output/"

