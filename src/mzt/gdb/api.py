# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from pathlib import Path
from typing import TextIO

import re
import pandas as pd


def analyze(out: TextIO, path: Path, **kwargs) -> None:
    """Analyze GDB output collected in the given `path`."""

    p_sf = re.compile("Stack frame at (?P<sf>0x[0-9A-Fa-f]+)")
    p_al = re.compile("Arglist at (?P<al>(0x[0-9A-Fa-f]+|unknown address))")

    def convert_frame_address(x: str) -> int:
        s = x.strip().strip('"')
        m = p_sf.match(s)
        # np.int64(int(m["sf"], base=0))
        return m["sf"]

    def convert_arglist_address(x: str) -> int:
        s = x.strip().strip('"')
        m = p_al.match(s)
        # np.int64(int(m["al"], base=0)) if m["al"] != "unknownaddress" else np.NAN
        return "0" if m["al"] == "unknown address" else m["al"]

    df = pd.read_csv(
        path,
        delimiter="|",
        names=["id", "frame_address", "arglist_address", "locals_address", "location"],
        converters={
            "id": lambda x: int(x.strip().lstrip("#")),
            "frame_address": convert_frame_address,
            "arglist_address": convert_arglist_address,
            "locals_address": lambda x: x.strip().strip('"'),
            "location": lambda x: x.strip().strip('"'),
        },
    )

    # remove last row from the dataframe (this should be a clone() at address 0x0 so not very useful)
    df = df.iloc[:-1, :]

    # take the first 100 chars of the code point
    df["code"] = df["location"].apply(lambda x: x[0:150])

    # compute frame_size: frame_size[i] = frame_address[i] - frame_address[i-1]
    df["frame_address_as_int"] = df["frame_address"].apply(lambda x: int(x, base=0))
    df["frame_size"] = df["frame_address_as_int"].diff()

    # compute arglist_size: arglist_size[i] = frame_address[i] - frame_address[i-1]
    # df["arglist_address_as_int"] = df["frame_address"].apply(lambda x: int(x, base=0))

    print(
        df[["id", "frame_address", "frame_size", "code"]]
        .sort_values(by="id", ascending=True)
        .to_string()
    )
