# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from typing import Optional

import psycopg2
import psycopg2.extensions


def db_connect(
    db_port: int,
    db_host: str,
    db_name: str,
    db_user: str,
    db_pass: Optional[str],
    **kwargs,
) -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_pass,
        sslmode="require",
    )
