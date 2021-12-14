# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from enum import Enum
from typing import TextIO

import psycopg2
import psycopg2.extensions
import mzt.dot.api


class ExplainMode(Enum):
    RAW = "raw"
    DECORRELATED = "decorrelated"
    OPTIMIZED = "optimized"
    TYPED = "typed"

    def __str__(self) -> str:
        return self.value


def query(out: TextIO, query: str, mode: ExplainMode, **kwargs) -> None:
    """Dot graph for 'EXPLAIN {mode} PLAN FOR {query}'."""

    with connect(**kwargs) as conn, conn.cursor() as cursor:
        cursor.execute(f"explain {mode} plan for {query}")
        lines = cursor.fetchone()[0].splitlines()
        mzt.dot.api.generate_graph(out, lines)


def view(out: TextIO, view: str, mode: ExplainMode, **kwargs) -> None:
    """Dot graph for 'EXPLAIN {mode} PLAN FOR VIEW {view}'."""

    with connect(**kwargs) as conn, conn.cursor() as cursor:
        query = f"explain {mode} plan for view {view}"
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
