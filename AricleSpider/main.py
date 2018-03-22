# -*- coding:UTF-8 -*-
# 让scrapy可以调试，可以控制命令行

# 此函数可以执行scrapy的脚本
from scrapy.cmdline import execute

import sys
import os
# 需要设置工程目录
# 获取到当前目录的路径然后在找到他的父目录就是该工程的目录，这样可以动态的获取
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','jobbole'])








