import os
import re
import sys
from argparse import ArgumentParser
from os.path import basename


def main():
    parser = ArgumentParser()

    parser.add_argument("-i", "--increment", dest="incrementing", default="release",
                        help="Which part of application version will be incremented: major, minor or release.",
                        metavar="INCREMENTING")

    parser.add_argument("-f", "--version-file", dest="version_file",
                        help="Path to project's version.py", required=True,
                        metavar="VERSION_FILE")

    version_groups = ["major", "minor", "release"]
    args = parser.parse_args()
    version_file_content = open(args.version_file).read()

    if not os.path.isfile(args.version_file) or basename(args.version_file) != "version.py" or \
            not '__version__' in version_file_content:
        print >> sys.stderr.write("Incorrect version.py path")

    if args.incrementing not in version_groups:
        print >> sys.stderr.write(
            "Incorrect increment(-i/--incrementing) argument. Should be one of those: major, minor, release")

    regex_split_version_var = re.compile(r'^__version__.*\"(\d+)\.(\d+)\.(\d+)\"$', flags=re.MULTILINE)

    splitted_version_var = regex_split_version_var.split(version_file_content)

    version_number = [item for item in splitted_version_var if item.isdigit()]

    if len(version_number) != 3:
        print >> sys.stderr.write("Invalid version format, should be MAJOR.MINOR.RELEASE (ie: 1.1.5)")

    version = {"major": int(version_number[0]),
               "minor": int(version_number[1]),
               "release": int(version_number[2])
               }
    old_version = "{}.{}.{}".format(version["major"], version["minor"], version["release"])
    version[args.incrementing] += 1
    new_version = "{}.{}.{}".format(version["major"], vergit sion["minor"], version["release"])

    version_py_content = open(args.version_file, "r").read()
    version_py_stream = open(args.version_file, "w+")

    version_py_content = version_py_content.replace("\"{}\"".format(old_version), "\"{}\"".format(new_version))

    version_py_stream.writelines(version_py_content)
    print("=== Incremented application version from {} to {} ===".format(old_version, new_version))
    print("=== Check {} file to see the new __version__ value ===".format(basename(args.version_file)))
