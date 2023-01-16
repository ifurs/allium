#!/usr/bin/env python3

"""
File: allium.py (executable)

Generate complete set of relay HTML pages and copy static files to the
output_dir

Default output directory: ./www
"""

import argparse
import os
import pkg_resources
import sys
from jinja2 import Environment, FileSystemLoader
from lib.relays import Relays
from lib.logger import logger

jinja_version = pkg_resources.parse_version(
    pkg_resources.get_distribution("jinja2").version
)

if jinja_version < pkg_resources.parse_version("2.11.2"):
    sys.exit("Jinja2>=2.11.2 required")

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

environment = Environment(loader=FileSystemLoader("parsed/"))

results_filename = "torrc"
results_template = environment.get_template("torrc.j2")


if __name__ == "__main__":
    desc = "allium: generate static tor relay metrics and statistics"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--out",
        dest="output_dir",
        type=str,
        default="./www",
        help='directory to store rendered files (default "./www")',
        required=False,
    )
    parser.add_argument(
        "--onionoo-url",
        dest="onionoo_url",
        type=str,
        default="https://onionoo.torproject.org/details",
        help="onionoo HTTP URL (default " '"https://onionoo.torproject.org/details")',
        required=False,
    )
    args = parser.parse_args()

    # object containing onionoo data and processing routines
    RELAY_SET = Relays(args.output_dir, args.onionoo_url)
    if RELAY_SET.json is None:
        sys.exit(0)

    RELAY_SET.all_list()

    relays = {
        "exit_nodes": RELAY_SET.exit_nodes(),
        "middle_nodes": RELAY_SET.middle_nodes(),
        "entry_nodes": RELAY_SET.entry_nodes(),
    }

    with open(results_filename, mode="w", encoding="utf-8") as results:
        results.write(results_template.render(relays))
        logger.info(f"... wrote {results_filename} file")
