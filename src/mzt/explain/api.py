# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from enum import Enum
from typing import TextIO, List

import psycopg2
import psycopg2.extensions
import mzt.dot.api


class ExplainMode(Enum):
    RAW_PLAN = "raw-plan"
    DECORRELATED_PLAN = "decorrelated-plan"
    OPTIMIZED_PLAN = "optimized-plan"

    TYPED_RAW_PLAN = "typed-raw-plan"
    TYPED_DECORRELATED_PLAN = "typed-decorrelated-plan"
    TYPED_OPTIMIZED_PLAN = "typed-optimized-plan"

    QUERY_GRAPH = "query-graph"
    TYPED_QUERY_GRAPH = "typed-query-graph"

    def __str__(self) -> str:
        return self.value

    def qgm_plans() -> List["ExplainMode"]:
        return [ExplainMode.QUERY_GRAPH, ExplainMode.TYPED_QUERY_GRAPH]

    def list(qgm: bool) -> List["ExplainMode"]:
        return [
            mode
            for mode in iter(ExplainMode)
            if qgm or mode not in ExplainMode.qgm_plans()
        ]


def query(out: TextIO, query: str, mode: ExplainMode, **kwargs) -> None:
    """Dot graph for 'EXPLAIN {mode} FOR {query}'."""

    with connect(**kwargs) as conn, conn.cursor() as cursor:
        cursor.execute(f"EXPLAIN {str(mode).replace('-', ' ').upper()} FOR {query}")
        lines = cursor.fetchone()[0].splitlines()
        if mode not in [ExplainMode.QUERY_GRAPH, ExplainMode.TYPED_QUERY_GRAPH]:
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
