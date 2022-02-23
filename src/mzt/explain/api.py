# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from ast import Dict
from enum import Enum
import re
from typing import List, Set, TextIO, Tuple

import psycopg2
import psycopg2.extensions
import mzt.dot.api


class ExplainMode(Enum):
    RAW_PLAN = "raw-plan"
    QUERY_GRAPH = "query-graph"
    OPTIMIZED_QUERY_GRAPH = "optimized-query-graph"
    DECORRELATED_PLAN = "decorrelated-plan"
    OPTIMIZED_PLAN = "optimized-plan"

    TYPED_RAW_PLAN = "typed-raw-plan"
    TYPED_QUERY_GRAPH = "typed-query-graph"
    TYPED_OPTIMIZED_QUERY_GRAPH = "typed-optimized-query-graph"
    TYPED_DECORRELATED_PLAN = "typed-decorrelated-plan"
    TYPED_OPTIMIZED_PLAN = "typed-optimized-plan"

    def __str__(self) -> str:
        return self.value

    def qgm_plans() -> Set["ExplainMode"]:
        return {
            ExplainMode.QUERY_GRAPH,
            ExplainMode.OPTIMIZED_QUERY_GRAPH,
            ExplainMode.TYPED_QUERY_GRAPH,
            ExplainMode.TYPED_OPTIMIZED_QUERY_GRAPH,
        }

    def list(qgm: bool) -> List["ExplainMode"]:
        return [
            mode
            for mode in iter(ExplainMode)
            if qgm or mode not in ExplainMode.qgm_plans()
        ]


def query(out: TextIO, query: str, mode: ExplainMode, **kwargs) -> None:
    """Dot graph for 'EXPLAIN {mode} FOR {query}'."""

    # the query string can be optionally prefixed with `SET <option> = <value>;`
    # statements, so we need to parse those before doing the work
    vars, query = parse_set_vars_prefix(query)

    with connect(**kwargs) as conn, conn.cursor() as cursor:
        # prepare ocnnection environment by executing all set_option statements
        for key, val in vars.items():
            cursor.execute(f"SET {key} = {val}")

        # explain the plan in the requested mode
        cursor.execute(f"EXPLAIN {str(mode).replace('-', ' ').upper()} FOR {query}")
        lines = cursor.fetchone()[0].splitlines()

        # for non-QGM plans, convert the ASCII output to a dot graph
        if mode not in ExplainMode.qgm_plans():
            mzt.dot.api.generate_graph(out, lines)
        else:
            out.write("\n".join(lines) + "\n")


def view(out: TextIO, view: str, mode: ExplainMode, **kwargs) -> None:
    """Dot graph for 'EXPLAIN {mode} FOR VIEW {view}'."""

    with connect(**kwargs) as conn, conn.cursor() as cursor:
        query = f"EXPLAIN {str(mode).replace('-', ' ').upper()} FOR VIEW {view}"
        cursor.execute(query)
        lines = cursor.fetchone()[0].splitlines()
        mzt.dot.api.generate_graph(out, lines, view)


def connect(
    db_port: int,
    db_host: str,
    db_name: str,
    db_user: str,
    **kwargs,
) -> psycopg2.extensions.connection:
    return psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user)


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

    return (set_options, query)
