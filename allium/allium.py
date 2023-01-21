#!/usr/bin/env python

"""
File: allium.py (executable)

"""

import argparse
import json
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

environment = Environment(loader=FileSystemLoader("templates/"))

results_filename = "torrc"
relays_json = "relays.json"
results_template = environment.get_template("torrc.j2")


if __name__ == "__main__":
    desc = "allium: generate node lists and torrc file by requirements, default generation of excluded nodes"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--onionoo-url",
        dest="onionoo_url",
        type=str,
        default="https://onionoo.torproject.org/details",
        help="onionoo HTTP URL (default " '"https://onionoo.torproject.org/details")',
        required=False,
    )
    parser.add_argument(
        "--filter-by-bandwidth",
        dest="bandwidth_threshold",
        type=int,
        default=12500000,
        help="Define bandwidth threshold in bytes (default " "12500000)",
        required=False,
    )
    parser.add_argument(
        "--generate-nodes",
        dest="generate_nodes",
        type=str,
        default=[],
        nargs="+",
        help="Generates lists of specified node types. In order format, e.g: entry middle exit (default "
        "None)",
        required=False,
    )
    args = parser.parse_args()

    # object containing onionoo data and processing routines
    RELAY_SET = Relays(args.onionoo_url, args.generate_nodes, args.bandwidth_threshold)
    if RELAY_SET.json is None:
        sys.exit(0)

    with open(relays_json, mode="w", encoding="utf-8") as results:
        results.write(json.dumps(RELAY_SET.all_list()))
        logger.info(f"... wrote {relays_json} file")

    relays = {
        "exit_nodes": RELAY_SET.exit_nodes(),
        "middle_nodes": RELAY_SET.middle_nodes(),
        "entry_nodes": RELAY_SET.entry_nodes(),
        "exclude_nodes": RELAY_SET.exclude_nodes(),
    }

    with open(results_filename, mode="w", encoding="utf-8") as results:
        results.write(results_template.render(relays))
        logger.info(f"... wrote {results_filename} file")
