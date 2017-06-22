#!/usr/bin/env python3

from pywc.main import get_argument_parser
from pywc.main import main

if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()
    main(args)