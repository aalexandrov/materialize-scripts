# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

import click

import mzt.cli
import mzt.explain.cli
import mzt.explain.repository.cli

# import logging
#
# logging.basicConfig(
#     encoding="utf-8",
#     level=logging.DEBUG,
#     format=r"- %(asctime)s %(levelname)s %(message)s",
#     datefmt=r"%m/%d/%Y %I:%M:%S %p",
# )


def main() -> None:
    mzt.cli.command(auto_envvar_prefix="MZT")


if __name__ == "__main__":
    main()
