from setuptools import find_packages, setup

setup(
    name='DCDownloader',
    version='1.0',
    description="Downloader for www.dmzj.com 动漫之家漫画下载器",
    author='techmoe',
    url='',
    license='MIT',
    packages=['dcdownloader'],
    install_requires=['aiohttp', 'colorlog', 'aiofiles', 'pyquery', 'pyyaml'],
    entry_points="""
    [console_scripts]
    dcdownloader = dcdownloader.main:main
    """
)