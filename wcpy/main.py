
from wcpy import WCExtractor

import argparse

def get_argument_parser():
    parser = argparse.ArgumentParser(
        description='Count the number of words in the files on a folder',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""

EXAMPLE USAGE:
                wc.py --paths ./
                wc.py --paths ./ --limit 10
                wc.py --paths ./ tests/test_data/doc1.txt --filter-words tool awesome an
                wc.py --paths tests/test_data/ --truncate 100 --columns word count
                wc.py --paths ./ --filter-words tool awesome an --truncate 50 --output output.txt
        """)
    parser.add_argument("--paths", nargs="+", required=True, type=str,
        help="(REQUIRED) Path(s) to folders and/or files to count words from")
    parser.add_argument("--limit", type=int,
        help="(Optional) Limit the number of results that you would like to display.")
    parser.add_argument("--reverse", action="store_true",
        help="(Optional) List is sorted in ascending order by default, use this flag to reverse sorting to descending order.")
    parser.add_argument("--filter-words", nargs="+", type=str, default=[],
        help="(Optional) You can get results filtered to only the list of words provided.")
    parser.add_argument("--file-ext", type=str, default="txt",
        help="(Optional) This is the default file extention for the files being used")
    parser.add_argument("--truncate", type=int, default=50,
        help="(Optional) Output is often quite large, you can truncate the output by passing a number greater than 5")
    parser.add_argument("--columns", type=str, nargs="+", default=[],
        help="(Optional) This argument allows you to choose the columns to be displayed in the output. Options are: word, count, files and sentences.")
    parser.add_argument("--output-file", type=str,
        help="(Optional) Define an output file to save the output")

    return parser

def main(args):

    extractor = WCExtractor(
                    limit=args.limit,
                    direction=not(args.reverse),
                    filter_words=args.filter_words,
                    file_extension=args.file_ext,
                    output_file=args.output_file
                    )

    extractor.display_wc_table(args.paths, char_limit=args.truncate, columns=args.columns)



