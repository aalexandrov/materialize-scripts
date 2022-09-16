# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

import json
import re

from enum import Enum
from typing import Dict, TextIO, Tuple

import mzt.dot.api
import mzt.lib


class TraceConfig(Enum):
    ARITY = "arity"
    JOIN_IMPLS = "join_impls"
    KEYS = "keys"
    LINEAR_CHAINS = "no_linear_chains"
    NON_NEGATIVE = "non_negative"
    NO_FAST_PATH = "no_fast_path"
    RAW_PLANS = "raw_plans"
    RAW_SYNTAX = "raw_syntax"
    SUBTREE_SIZE = "subtree_size"
    TIMING = "timing"
    TYPES = "types"

    def __str__(self) -> str:
        return self.value


def query(out: TextIO, query: str, config: TraceConfig, **kwargs) -> None:
    """Dot graph for 'EXPLAIN OPTIMIZER TRACE WITH({config}) AS TEXT FOR {query}'."""

    # the query string can be optionally prefixed with `SET <option> = <value>;`
    # statements, so we need to parse those before doing the work
    vars, query = parse_set_vars_prefix(query)

    with mzt.lib.db_connect(**kwargs) as conn, conn.cursor() as cursor:
        # prepare ocnnection environment by executing all set_option statements
        for key, val in vars.items():
            cursor.execute(f"SET {key} = {val}")

        # trace the plan in the requested mode
        cursor.execute(
            " ".join(
                [
                    f"EXPLAIN OPTIMIZER TRACE",
                    f"WITH({', '.join(map(str, config))})" if config else "",
                    f"AS TEXT",
                    f"FOR {query}",
                ]
            )
        )

        trace = {
            "explainee": {"query": query},
            "list": [
                {"id": id, "time": int(time), "path": path, "plan": plan}
                for (id, (time, path, plan)) in enumerate(cursor.fetchall())
            ],
        }

        json.dump(trace, out, indent=4)
        out.write("\n")
        out.flush()


def view(out: TextIO, view: str, config: TraceConfig, **kwargs) -> None:
    """Dot graph for 'EXPLAIN OPTIMIZER TRACE WITH({config}) AS TEXT FOR VIEW {view}'."""

    with mzt.lib.db_connect(**kwargs) as conn, conn.cursor() as cursor:
        cursor.execute(
            " ".join(
                [
                    f"EXPLAIN OPTIMIZER TRACE",
                    f"WITH({', '.join(map(str, config))})" if config else "",
                    f"AS TEXT",
                    f"FOR VIEW {view}",
                ]
            )
        )

        trace = {
            "explainee": {"view": view},
            "list": [
                {"id": id, "time": int(time), "path": path, "plan": plan}
                for (id, (time, path, plan)) in enumerate(cursor.fetchall())
            ],
        }

        json.dump(trace, out, indent=4)
        out.write("\n")
        out.flush()


def parse_set_vars_prefix(query: str) -> Tuple[Dict[str, str], str]:
    # matches a statement of the form "SET <option> = <value>;"
    pat = re.compile(r"\s*SET\s*(?P<key>\w+)\s*=\s*(?P<val>\w+)\s*;\s*")

    # find and extract a prefix zero or more SET statements
    set_options = {}
    mat, pos = pat.search(query, 0), 0
    while mat:
        set_options[mat.group("key").lower()] = mat.group("val").lower()
        mat, pos = pat.search(query, mat.end()), mat.end()

    # treat the remainder as the actual query
    query = query[pos:]

    return set_options, query
