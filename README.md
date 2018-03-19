# DCDownloader
由Python编写的全异步实现的动漫之家(dmzj)漫画批量下载器（爬虫）

## 说明
这是一个使用Python3编写的动漫之家的漫画批量下载器。相比于我之前所写过的几个爬虫，这个爬虫也是我第一次尝试**全异步**实现的一个爬虫例子，使用了*aiohttp*和*aiofile*这两个异步实现库来做支撑，相对于单线程爬虫和多线程爬虫，使用异步(async)这种方式能够更好的分配计算和IO资源，保证了资源的充分利用以及速度。同时，这也是我第一次较为完整编写的一个Python开源项目。

## 特点
* 更高效的资源利用和优秀的速度
* 彩色控制台终端日志输出（colorlog）

## 安装 
* Linux和OSX  
    ```bash
    $ git clone git@github.com:dev-techmoe/python-dcdownloader.git
    $ cd python-dcdownloader
    $ python3 setup.py install
    ```
* Windows平台  
    也可以采取上面的方法安装，也可以直接来下载运行预编译的二进制文件来使用(待补充)

## 配置
配置是可选的，您完全可以不用配置就使用本程序。  
配置文件名为config.yml，yaml格式，请保存在程序运行的目录下。  
|配置项|说明|默认值|
|-----|-----|-----|
|debug_mode|调试模式|False|
|save_manifest_file|保存元数据以供增量下载 *未完成*|false|
|proxy|代理服务器|None|
|downloader_max_connection_number|下载器并发数（最大同时下载任务数）|5|
|downloader_max_retry_number|下载器最大重试次数|5|
|friendly_console_output|人类友好的控制台输出 *未完成*|false|
|header|自定义请求header|默认仅设置了ua和referer|

## 使用
```
dcdownloader <target_comic_index_page_url> <save_path>
```
* `target_comic_index_page_url`: 目标漫画的主页URL
* `save_path`: （可选）下载保存路径（默认路径为`./output`）  

下载到的漫画将以`<漫画名>/<章节名>/漫画.png`这样的格式来保存  
e.g.:
```
output
└── 幸运星
    ├── 入学手册
    │   ├──  073.jpg
    │   ├──  074.jpg
    │   └──  ...
    ├── ...
```
## 免责声明
这个项目更多的其实是作为作者个人的练习项目存在，方便使用只是其二。为了不对目标站造成困扰，作者已将默认并发数设置到了一个作者认为不会对其造成影响的程度。由于自身使用所造成的问题作者不付任何责任，同时作者不对任何下载内容承担任何责任。

## License
MIT

