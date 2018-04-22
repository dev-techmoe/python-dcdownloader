# DCDownloader

![python](https://img.shields.io/badge/python-3.6.4%2B-green.svg)
[![GitHub license](https://img.shields.io/github/license/dev-techmoe/python-dcdownloader.svg)](https://github.com/dev-techmoe/python-dcdownloader/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/dev-techmoe/python-dcdownloader.svg?branch=master)](https://travis-ci.org/dev-techmoe/python-dcdownloader)
[![GitHub stars](https://img.shields.io/github/stars/dev-techmoe/python-dcdownloader.svg)](https://github.com/dev-techmoe/python-dcdownloader/stargazers)

专注于漫画网站、图站等类似形式的内容站点的批量下载器框架。

## 说明
这个项目最开始是作者编写的一个仅支持某个漫画网站的批量下载器，后来有人提建议说有增加网站的需求，作者便重新梳理了一下思路重构了代码，使其作为一种框架形式存在。DCDownloader是目前一款异步实现的、支持自定义适配的，专注于漫画网站、图站等类似形式的内容站点的批量下载器。通过编写Parser来做到适配不同的网站。   
目前项目中内置了三个Parser，分别是

* SimpleParser  一个Parser的例子，希望自己编写Parser的话可以参考这个的实现，同时也应用于单元测试过程中。
* DmzjParser 动漫之家漫画站（非原创区）
* EhentaiParser Ehentai

## 安装
### Windows 
[exe可执行文件下载](https://github.com/dev-techmoe/python-dcdownloader/releases)  

### Linux/OSX  
请确认您本机已安装python和pip并且python版本大于3.4.3
```bash
$ pip3 install https://github.com/dev-techmoe/python-dcdownloader/archive/master.zip
$ dcdownloader -h
```

## 可用命令
```
usage: dcdownloader [-h] [--proxy PROXY] [--no-verify-ssl] [-v] [-V] [--fetch-only]
               URL [OUTPUT_PATH]

positional arguments:
  URL              target URL
  OUTPUT_PATH      output path of downloaded file (default: current directory)

optional arguments:
  -h, --help       show this help message and exit
  --proxy PROXY    HTTP proxy address for connection
  --no-verify-ssl  Disable the SSL certificate verifying when connecting
  -v, --version    show version
  -V, --verbose    show more running detail
  --fetch-only     Ignore all download process (only fetch chapter and image urls)

```

## 免责声明
这个项目更多的其实是作为作者个人的练习项目存在，方便使用只是其二。为了不对目标站造成困扰，作者已将默认并发数设置到了一个作者认为不会对目标站造成影响的程度。由于使用者自身使用所造成的问题作者不付任何责任，同时作者不对任何下载内容承担任何责任。

## 贡献
本项目欢迎提交pr，非常希望您能够帮助改善本项目。您可以帮助我来适配更多的网站，但是我目前**不希望用来解析收录原创漫画站的Parser**，还请见谅。

## License
MIT