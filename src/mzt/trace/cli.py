# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from pathlib import Path

import tempfile
import click
import sys
import psycopg2
import traceback

import mzt.cli
import mzt.trace.api

# Click Command
# -------------


@mzt.cli.command.group(name="trace")
def command() -> None:
    """Support for traceing query plans."""
    pass


class Arg:
    QUERY = dict(type=str, nargs=1)
    VIEW = dict(type=str, nargs=1)


class Opt:
    CONFIG = dict(
        type=click.Choice([str(config) for config in mzt.trace.api.TraceConfig]),
        callback=lambda ctx, param, values: [
            mzt.trace.api.TraceConfig(value) for value in values
        ],
        help="Trace WITH(..) config values.",
        envvar="MZT_TRACE_CONFIG",
        multiple=True,
    )


@command.command()
@click.argument("query", **Arg.QUERY)
@click.option("--with", "-w", "config", **Opt.CONFIG)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@click.option("--db-pass", **mzt.cli.BaseOpt.DB_PASS)
@mzt.cli.is_documented_by(mzt.trace.api.query)
def query(query: str, config: mzt.trace.api.TraceConfig, **kwargs) -> None:
    try:
        mzt.trace.api.query(sys.stdout, query, config, **kwargs)
    except psycopg2.DatabaseError as e:
        raise mzt.cli.MztException(f"'trace query' command failed: {e}")
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'trace query' command failed:\n{message}")


@command.command()
@click.argument("path", **Arg.VIEW)
@click.option("--with", "-w", "config", **Opt.CONFIG)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@click.option("--db-pass", **mzt.cli.BaseOpt.DB_PASS)
@mzt.cli.is_documented_by(mzt.trace.api.view)
def view(view: str, config: mzt.trace.api.TraceConfig, **kwargs) -> None:
    try:
        mzt.trace.api.view(sys.stdout, view, config, **kwargs)
    except psycopg2.DatabaseError as e:
        raise mzt.cli.MztException(f"'trace view' command failed: {e}")
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'trace view' command failed:\n{message}")
