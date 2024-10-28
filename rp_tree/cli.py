"""cli for rptree 
    """
import argparse
import pathlib
import sys

from . import __version__
from .rptree import DirectoryTree


def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    output_file = args.output_file
    if output_file is not None:
        output_file = output_file[0]
    # check if given path is a dir
    if not root_dir.is_dir():
        sys.exit("path given is not directory")
    tree = DirectoryTree(
        root_dir=root_dir, dir_only=args.dir_only, output_file=output_file)
    tree.generate()


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog='tree',
        description='rptree, a directory tree generator',
        epilog='Thanks for using rptree'
    )

    parser.dir_only = False
    # is this how you default an argument value of an optional arg
    parser.version = f"RP Tree v{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("-d", "--dir_only", action="store_true")
    parser.add_argument("-o", "--output_file", nargs=1)
    parser.add_argument("root_dir", metavar="ROOT_DIR", nargs="?", default=".",
                        help="Generate a full directory tree starting at ROOTDIR")
    return parser.parse_args()
