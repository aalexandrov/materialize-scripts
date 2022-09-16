# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from pathlib import Path

import click
import psycopg2
import traceback

import mzt.cli
import mzt.trace.cli
import mzt.trace.repository.api

# Click Command
# -------------


@mzt.trace.cli.command.group(name="repository")
def command() -> None:
    """Manage a repository of 'TRACE PLAN' dot graphs."""
    pass


class Opt:
    REPOSITORY = dict(
        default=Path.home() / "mzt-traces" / "default",
        type=click.Path(
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
            readable=True,
            resolve_path=True,
        ),
        envvar="MZT_TRACES",
        help="Trace repository folder.",
        callback=lambda _ctx, _param, value: Path(value),
    )


@command.command()
@click.option("--repository", **Opt.REPOSITORY)
@mzt.cli.is_documented_by(mzt.trace.repository.api.Repository.init)
def init(repository: Path) -> None:
    try:
        repo = mzt.trace.repository.api.Repository(repository)
        repo.init(force=True)
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'repository add' command failed:\n{message}")


@command.command()
@click.argument("query", **mzt.trace.cli.Arg.QUERY)
@click.option("--repository", **Opt.REPOSITORY)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@mzt.cli.is_documented_by(mzt.trace.repository.api.Repository.add)
def add(query: str, repository: Path, **kwargs) -> None:
    try:
        hash = mzt.trace.repository.api.hash(query)
        mzt.cli.info(f"adding entry {hash} to repository at '{repository}'")

        repo = mzt.trace.repository.api.Repository(repository)
        repo.add(query, **kwargs)
    except psycopg2.DatabaseError as e:
        raise mzt.cli.MztException(f"'repository add' command failed: {e}")
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'repository add' command failed:\n{message}")


@command.command()
@click.argument("query", **mzt.trace.cli.Arg.QUERY)
@click.option("--repository", **Opt.REPOSITORY)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@mzt.cli.is_documented_by(mzt.trace.repository.api.Repository.remove)
def remove(query: str, repository: Path, **kwargs) -> None:
    try:
        hash = mzt.trace.repository.api.hash(query)
        mzt.cli.info(f"deleting entry {hash} from repository at '{repository}'")

        repo = mzt.trace.repository.api.Repository(repository)
        repo.remove(query, **kwargs)
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'repository remove' command failed:\n{message}")
