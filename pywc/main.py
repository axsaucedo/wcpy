
import argparse

def get_argument_parser():
    parser = argparse.ArgumentParser(
        description='Count the number of words in the files on a folder')
    parser.add_argument("--limit", type=int,
        help="Limit the number of results that you would like to display.")
    parser.add_argument("--reverse", action="store_true",
        help="List is sorted in ascending order by default, use this flag to reverse sorting to descending order.")
    parser.add_argument("--filter-words", nargs="+", type=str,
        help="You can get results filtered to only the list of words provided.",
        epilog="--filter-words tool awesome an is this")
    parser.add_argument("--file-ext", type=str, default="txt",
        help="This is the default file extention for the files being used")
    parser.add_argument("--truncate", type=int, default=50,
        help="Output is often quite large, you can truncate the output by passing a number greater than 5")
    parser.add_argument("--columns", type=str, nargs="+",
        help="This argument allows you to choose the columns to be displayed in the output. Options are: word, count, files and sentences.",
        epilog="--columns word count")

    return parser

def main(args):
    pass