# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

import click
import sys
import psycopg2
import traceback

import mzt.cli
import mzt.explain.api

# Click Command
# -------------


@mzt.cli.command.group(name="explain")
def command() -> None:
    """Support for explaining query plans."""
    pass


class Arg:
    QUERY = dict(type=str, nargs=1)
    VIEW = dict(type=str, nargs=1)
    MODE = dict(
        type=click.Choice([str(mode) for mode in mzt.explain.api.ExplainMode]),
        callback=lambda ctx, param, value: mzt.explain.api.ExplainMode(value),
    )


@command.command()
@click.argument("mode", **Arg.MODE)
@click.argument("query", **Arg.QUERY)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@mzt.cli.is_documented_by(mzt.explain.api.query)
def query(query: str, mode: mzt.explain.api.ExplainMode, **kwargs) -> None:
    try:
        mzt.explain.api.query(sys.stdout, query, mode, **kwargs)
    except psycopg2.DatabaseError as e:
        raise mzt.cli.MztException(f"'explain query' command failed: {e}")
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'explain query' command failed:\n{message}")


@command.command()
@click.argument("mode", **Arg.MODE)
@click.argument("view", **Arg.VIEW)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@mzt.cli.is_documented_by(mzt.explain.api.view)
def view(view: str, mode: mzt.explain.api.ExplainMode, **kwargs) -> None:
    try:
        mzt.explain.api.view(sys.stdout, view, mode, **kwargs)
    except psycopg2.DatabaseError as e:
        raise mzt.cli.MztException(f"'explain view' command failed: {e}")
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'explain view' command failed:\n{message}")
