# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.


import hashlib
import os
import shutil
import logging
import lxml.etree as ET
from pathlib import Path
from subprocess import check_call

import mzt.explain.api
from pkg_resources import resource_filename


class Repository:
    def __init__(self, root: Path) -> None:
        """initialize folder structure if needed"""

        self.root = root
        
        if not self.root.exists():
            logging.info(f"initialize new repository in {self.root}")
            self.root.mkdir(parents=True)
        
        for ext in ["js", "css", "xml", "xsl"]:
            file = f"index.{ext}"
            if not (self.root / file).exists():
                if ext == "xml":
                    logging.info(f"copy initial {self.root / file}")
                    shutil.copy(resource_path(file), self.root / file)
                else:
                    logging.info(f"create soft link to {self.root / file}")
                    os.symlink(resource_path(file), self.root / file)
        
        for ext in ["svg", "png"]:
            file = f"not_available.{ext}"
            if not (self.root / file).exists():
                logging.info(f"create soft link to {self.root / file}")
                os.symlink(resource_path(file), self.root / file)

    def add(self, query: str, **kwargs) -> None:
        """Add an entry for a query from the repository."""
        logging.info(f"add entry {hash(query)} to the repository at '{self.root}'")

        # ensure that the query directory exists
        entry_path = self.entry_path(query)
        if not entry_path.exists():
            entry_path.mkdir(parents=True)

        # qrite query to file
        query_path = entry_path / f"query.sql"
        query_path.write_text(query.strip() + "\n", "utf8")

        # the query string can be optionally prefixed with `SET <option> = <value>;`
        # statements, and we need to extract those as they guide the following work
        vars, _ = mzt.explain.api.parse_set_vars_prefix(query)

        # iterate over explain modes
        qgm_enabled = bool(vars.get("qgm_optimizations_experimental", False))
        modes = mzt.explain.api.ExplainMode.list(qgm_enabled)
        for mode in modes:
            # generate dot files for mode
            dot_path = entry_path / f"{mode}.dot"
            with dot_path.open("wt") as dot_file:
                mzt.explain.api.query(dot_file, query, mode, **kwargs)

            # generate png files mode
            for format in ["svg", "png"]:
                img_path = entry_path / f"{mode}.{format}"
                check_call(["dot", "-T", format, str(dot_path), "-o", str(img_path)])

        # re-index
        self.index()

    def remove(self, query: str, **kwargs) -> None:
        """Remove the entry for a query to the repository."""
        logging.info(f"remove entry {hash(query)} from the repository at '{self.root}'")

        # remove the query directory exists
        entry_path = self.entry_path(query)
        if entry_path.exists():
            shutil.rmtree(entry_path)

        # re-index
        self.index()

    def entry_path(self, query: str) -> Path:
        return self.root / hash(query)

    def index(self) -> Path:
        queries = [
            xml_query((child / "query.sql").read_text("utf8"))
            for child in self.root.iterdir()
            if (child / "query.sql").is_file()
        ]

        tree = ET.parse(str(self.root / "index.xml"))
        tree.getroot().clear()
        tree.getroot().extend(queries)
        tree.write(str(self.root / "index.xml"), pretty_print=True)


def xml_query(query: str) -> ET.Element:
    element = ET.Element("query")
    ET.SubElement(element, "id").text = hash(query)
    ET.SubElement(element, "sql").text = query.strip()
    return element


def resource_path(name: str) -> Path:
    return Path(resource_filename(__name__, name))


def hash(query: str) -> str:
    return hashlib.md5(query.strip().encode()).hexdigest()[0:8]
