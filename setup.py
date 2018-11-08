from setuptools import find_packages, setup

# load requirement list
with open('requirements.txt') as f:
    required_modules = f.read().splitlines()

setup(
    name='DCDownloader',
    version='1.0',
    description="a downloader that supports many comic sites",
    author='techmoe',
    url='https://github.com/dev-techmoe/python-dcdownloader',
    license='MIT',
    packages=find_packages(include='dcdownloader.*'),
    install_requires=required_modules,
    entry_points="""
    [console_scripts]
    dcdownloader = dcdownloader.main:main
    """
)