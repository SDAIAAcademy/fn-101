"""Read the branch export of the ticket system: data/tickets_branch.jsonl.

    uv run python decode.py

Salma wrote the first version on her office laptop and it worked there for the English
tickets. It names no encoding, so Python used the laptop's default; that default is written
out below, so that the script behaves the same on every machine.
"""

import json
from dataclasses import dataclass
from pathlib import Path

LAPTOP_DEFAULT = "cp1252"   # what open() used on that laptop when no encoding was named
PATH = "data/tickets_branch.jsonl"
META = "data/tickets_branch.meta.json"


@dataclass(frozen=True)
class Failure:
    line_no: int      # the line of the file, counted from 1
    position: int     # the byte within that line at which decoding stopped
    byte: str         # that byte, as text such as "0xc7"


def load(path: str) -> list[dict[str, str]]:
    """The first version: read every ticket of the file."""
    with open(path, encoding=LAPTOP_DEFAULT) as file:
        return [json.loads(line) for line in file]


def decode_lines(path: str, encoding: str) -> tuple[list[str], list[Failure]]:
    """Decode the file line by line: the lines that decode, and a Failure for each that does not.

    Read the file as bytes, split it into lines, and decode each line by itself, so that
    one bad line cannot hide the others.
    """
    raise NotImplementedError("step 3")


def main() -> None:
    tickets = load(PATH)
    print(len(tickets), "tickets read")
    # Step 4: replace the two lines above. Read the declared encoding from META, call
    # decode_lines, print how many lines decoded and the Failure of each line that did not,
    # and write out/decode_report.json:
    #   {"encoding": ..., "lines": ..., "decoded": ..., "failed": [{"line_no": ..., "position": ..., "byte": ...}]}


if __name__ == "__main__":
    main()
