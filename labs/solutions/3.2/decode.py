"""Read the branch export of the ticket system: data/tickets_branch.jsonl.

    uv run python decode.py

The file is declared as UTF-8, and seven of its lines were written by an old branch terminal
in Windows-1256. Every line is decoded by itself; the lines that fail are reported with the
byte at which decoding stopped, and nothing is ignored or replaced.
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

PATH = "data/tickets_branch.jsonl"
META = "data/tickets_branch.meta.json"


@dataclass(frozen=True)
class Failure:
    line_no: int      # the line of the file, counted from 1
    position: int     # the byte within that line at which decoding stopped
    byte: str         # that byte, as text such as "0xc7"


def decode_lines(path: str, encoding: str) -> tuple[list[str], list[Failure]]:
    """Decode the file line by line: the lines that decode, and a Failure for each that does not."""
    decoded: list[str] = []
    failed: list[Failure] = []
    data = Path(path).read_bytes()
    for line_no, raw in enumerate(data.splitlines(), start=1):
        try:
            decoded.append(raw.decode(encoding))
        except UnicodeDecodeError as problem:
            failed.append(Failure(line_no, problem.start, hex(raw[problem.start])))
    return decoded, failed


def main() -> None:
    with open(META, encoding="utf-8") as file:
        encoding = json.load(file)["encoding"]
    decoded, failed = decode_lines(PATH, encoding)
    print(f"declared encoding {encoding}: {len(decoded)} lines decoded, {len(failed)} failed")
    for failure in failed:
        print(f"  line {failure.line_no}: byte {failure.byte} at position {failure.position}")
    report = {"encoding": encoding, "lines": len(decoded) + len(failed), "decoded": len(decoded),
              "failed": [asdict(failure) for failure in failed]}
    Path("out").mkdir(exist_ok=True)
    with open("out/decode_report.json", "w", encoding="utf-8", newline="\n") as file:
        json.dump(report, file, indent=2)
        file.write("\n")
    # The stretch: the old terminal wrote Windows-1256, so those lines can be recovered.
    data = Path(PATH).read_bytes().splitlines()
    recovered = [json.loads(data[failure.line_no - 1].decode("cp1256")) for failure in failed]
    print(len(recovered), "lines recovered as Windows-1256; the first is ticket", recovered[0]["ticket_id"])


if __name__ == "__main__":
    main()
