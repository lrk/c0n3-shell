import argparse
from c0n3shell.shellclass import C0n3Shell

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='C0n3Shell')

    parser.add_argument('-u', '--url', dest='target', help='target url')

    parser.add_argument('-m', '--method', dest='http_verb',
                        help='http method/verb', default='get')

    parser.add_argument('-p', '--param', dest='parameter',
                        help='parameter', default='cmd')

    args = parser.parse_args()
    shell = C0n3Shell(
        url=args.target,
        http_verb=args.http_verb,
        attribute=args.parameter
    )
    shell.cmdloop()
