from scrapy import cmdline
import sys

# cmdline.execute(['scrapy', 'crawl', 'common_spider'])
# cmdline.execute("scrapy crawl common_spider -a section=TARGET_INFO".split())

section = sys.argv[1] and sys.argv[1] or 'SAMPLE_INFO'
cmdline.execute(['scrapy', 'crawl', 'common_spider', '-a', 'section=' + section])
