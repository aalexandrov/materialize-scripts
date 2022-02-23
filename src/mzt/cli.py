# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from typing import Any
import click


# Click CLI Application
# ---------------------


@click.group()
def command() -> None:
    pass


# Base Options & Args
# -------------------


class BaseOpt:
    DB_PORT = dict(
        default=6875,
        help="DB connection port.",
        envvar="MZT_DB_PORT",
    )

    DB_HOST = dict(
        default="localhost",
        help="DB connection host.",
        envvar="MZT_DB_HOST",
    )

    DB_NAME = dict(
        default="materialize",
        help="DB connection database.",
        envvar="MZT_DB_NAME",
    )

    DB_USER = dict(
        default="materialize",
        help="DB connection user.",
        envvar="MZT_DB_USER",
    )


# Utility methods
# ---------------


def is_documented_by(original: Any) -> Any:
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target

    return wrapper


def info(msg: str, fg: str = "green") -> None:
    click.secho(msg, fg=fg)


def err(msg: str, fg: str = "red") -> None:
    click.secho(msg, fg=fg, err=True)
