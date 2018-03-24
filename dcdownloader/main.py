import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

from dcdownloader import arg_parse

# for unittest
cmd_args = None

def main():
    args = arg_parse.parser.parse_args(cmd_args)
    
    from dcdownloader.scheduler import Scheduler
    from dcdownloader import parser_selector
    from dcdownloader.parser.DmzjParser import DmzjParser
    s = Scheduler(url=args.url, output_path=args.output_path, parser=parser_selector.get_parser(args.url))
    s.run()


if __name__ == '__main__':
    main()