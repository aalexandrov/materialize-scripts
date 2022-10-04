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
import sys
import traceback

import mzt.cli
import mzt.gdb.api

# Click Command
# -------------


@mzt.cli.command.group(name="gdb")
def command() -> None:
    """Support for GDB output post-processing."""
    pass


class Arg:
    PATH = dict(type=str, nargs=1)
    PATH = dict(
        type=click.Path(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
        nargs=1,
        callback=lambda _ctx, _param, value: Path(value),
    )


@command.command()
@click.argument("path", **Arg.PATH)
@mzt.cli.is_documented_by(mzt.gdb.api.analyze)
def analyze(path: Path, **kwargs) -> None:
    try:
        mzt.gdb.api.analyze(sys.stdout, path, **kwargs)
    except Exception as e:
        message = traceback.format_exc()
        raise mzt.cli.MztException(f"'trace view' command failed:\n{message}")
