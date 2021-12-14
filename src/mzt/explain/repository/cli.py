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
import mzt.cli
import mzt.explain.cli
import mzt.explain.repository.api

# Click Command
# -------------


@mzt.explain.cli.command.group(name="repository")
def command() -> None:
    """Manage a repository of 'EXPLAIN PLAN' dot graphs."""
    pass


class Opt:
    REPOSITORY = dict(
        default=Path.home() / "mzt-repos" / "default",
        type=click.Path(
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
            readable=True,
            resolve_path=True,
        ),
        envvar="MZT_REPOSITORY",
        help="Repository folder.",
        callback=lambda _ctx, _param, value: Path(value),
    )


@command.command()
@click.argument("query", **mzt.explain.cli.Arg.QUERY)
@click.option("--repository", **Opt.REPOSITORY)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@mzt.cli.is_documented_by(mzt.explain.repository.api.Repository.add)
def add(query: str, repository: Path, **kwargs) -> None:
    try:
        hash = mzt.explain.repository.api.hash(query)
        mzt.cli.info(f"adding entry {hash} to repository at '{repository}'")

        repo = mzt.explain.repository.api.Repository(repository)
        repo.add(query, **kwargs)
    except Exception as e:
        raise click.ClickException(f"run command failed: {e}")


@command.command()
@click.argument("query", **mzt.explain.cli.Arg.QUERY)
@click.option("--repository", **Opt.REPOSITORY)
@click.option("--db-port", **mzt.cli.BaseOpt.DB_PORT)
@click.option("--db-host", **mzt.cli.BaseOpt.DB_HOST)
@click.option("--db-name", **mzt.cli.BaseOpt.DB_NAME)
@click.option("--db-user", **mzt.cli.BaseOpt.DB_USER)
@mzt.cli.is_documented_by(mzt.explain.repository.api.Repository.remove)
def remove(query: str, repository: Path, **kwargs) -> None:
    try:
        hash = mzt.explain.repository.api.hash(query)
        mzt.cli.info(f"deleting entry {hash} from repository at '{repository}'")

        repo = mzt.explain.repository.api.Repository(repository)
        repo.remove(query, **kwargs)
    except Exception as e:
        raise click.ClickException(f"run command failed: {e}")
