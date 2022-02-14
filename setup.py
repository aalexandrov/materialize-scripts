# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from setuptools import find_packages, setup

setup(
    name="mzt",
    version="0.0.1",
    description="Materialize developer tools",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "mzt.explain.repository.api": ["*.xml", "*.xsl", "*.css", "*.js"],
    },
    install_requires=[
        "click==8.0.3",
        "lxml==4.7.1",
        "psycopg2-binary==2.9.1",
        "types-pkg-resources==0.1.3",
    ],
    entry_points={
        "console_scripts": [
            "mzt=mzt:main",
        ],
    },
)
