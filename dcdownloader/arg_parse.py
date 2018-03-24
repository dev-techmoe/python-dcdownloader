import argparse


parser = argparse.ArgumentParser()

parser.add_argument('url', metavar='URL', help='target URL')
parser.add_argument('output_path', metavar="OUTPUT_PATH", nargs='?', default='.', help='output path of downloaded file (default: current directory)')
parser.add_argument('-v', '--version', action='version', help='show version', version='dcdownloader 1.0')
parser.add_argument('-V', '--verbose', action='store_true', help='show more running detail')