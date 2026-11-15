"""The checks of Day 4: the notebook, the command line, the tests and the tutor lab."""

from __future__ import annotations

import json
import re
import shutil
import tempfile
from pathlib import Path

import checks as C
import checks3
import data
import labtool

RUN_NOTEBOOK = (
    "import re\n"
    "import nbformat\n"
    "from nbclient import NotebookClient\n"
    "book = nbformat.read('analysis.ipynb', as_version=4)\n"
    "saved = [[c.get('execution_count'), ''.join(o.get('text', '') for o in c.get('outputs', []))]\n"
    "         for c in book.cells if c.cell_type == 'code']\n"
    "sources = [c.source for c in book.cells if c.cell_type == 'code']\n"
    "error = ''\n"
    "try:\n"
    "    NotebookClient(book, timeout=120, kernel_name='python3').execute()\n"
    "except Exception as problem:\n"
    "    error = re.sub(r'\\x1b\\[[0-9;]*m', '', str(problem).strip().splitlines()[-1])\n"
    "fresh = [''.join(o.get('text', '') for o in c.get('outputs', []) if o.get('output_type') == 'stream')\n"
    "         for c in book.cells if c.cell_type == 'code']\n"
    "print(json.dumps({'error': error, 'saved': saved, 'fresh': fresh, 'sources': sources}))"
)


def check_4_1(folder: Path, r: C.Report) -> None:
    if not r.need((folder / "analysis.ipynb").is_file(), "analysis.ipynb is there"):
        return
    # The kernel writes warnings of its own, so the answer is looked for by its first characters.
    status, output = C.py(folder, "-W", "ignore", "-c", "import json\n" + RUN_NOTEBOOK)
    answer = [line for line in output.splitlines() if line.startswith('{"error"')]
    found: object = json.loads(answer[-1]) if answer else None
    why = C.last(output)
    if not r.need(isinstance(found, dict), "the notebook can be opened and run", f"the notebook could not be run: {why}"):
        return
    assert isinstance(found, dict)
    r.need(not found["error"], "a fresh kernel runs the notebook from top to bottom",
           f"a fresh kernel stops in the notebook: {found['error']}")
    fresh = "".join(found["fresh"])
    r.need("17561 readings kept" in fresh, "the fresh run keeps 17561 readings",
           "the fresh run does not print '17561 readings kept'")
    r.need(re.search(r"^18 anomalies", fresh, re.M), "the fresh run finds 18 anomalies",
           "the fresh run does not print '18 anomalies': which value does factor have when that cell runs?")
    setters = [s for s in found["sources"] if re.search(r"^factor\s*=", s, re.M)]
    r.need(len(setters) == 1, "factor is set in one cell only",
           f"factor is set in {len(setters)} cells: a later cell can change what an earlier one means")
    counts = [count for count, _ in found["saved"]]
    r.need(counts == list(range(1, len(counts) + 1)), "the saved file was run in order: the counts go 1, 2, 3 and on",
           f"the saved execution counts are {counts}: restart, run all, then save")
    r.need([text for _, text in found["saved"]] == found["fresh"], "every saved output is what the code produces",
           "a saved output differs from what a fresh run prints: restart, run all, then save")
    finding = C.text_of(folder / "finding.md")
    r.need(C.section_filled(finding, "1.", 12) and "known" in finding,
           "finding.md names what a fresh run could not find",
           "finding.md, section 1: say which name was missing and why the saved file did not show it")
    r.need(C.section_filled(finding, "2.", 12) and "27" in finding and "18" in finding,
           "finding.md names the stale number and the true one",
           "finding.md, section 2: say which saved number was stale, and what a clean run gives")

    homes = {int(n): (word.lower(), reason) for n, word, reason in
             re.findall(r"^([1-4])\s*:\s*(notebook|script|module)\b(.*)$", C.text_of(folder / "homes.md"), re.M | re.I)}
    r.need(len(homes) == 4 and all(C.words(reason) >= 4 for _, reason in homes.values()),
           "homes.md has a choice and a reason for the four tasks",
           f"homes.md has {len(homes)} of 4 choices with a reason (one word, then because and a line)")
    agree = sum(1 for n, word in HOMES.items() if homes.get(n, ("", ""))[0] == word)
    r.need(agree >= 3, f"{agree} of 4 choices match the reference",
           f"{agree} of 4 choices match the reference; discuss the others with your neighbour, then with the trainer")


HOMES = {1: "notebook", 2: "script", 3: "module", 4: "notebook"}
COMMAND = ["-m", "miqyas", "report", "--readings", "data/readings_2026_09.csv", "--meters", "data/meters.csv"]


def reference_report(lab: str) -> bytes:
    """The report of the sound package over the same month."""
    with tempfile.TemporaryDirectory() as tmp:
        for name in labtool.DATA[lab]:
            data.write(name, Path(tmp))
        labtool.package(Path(tmp))
        C.py(Path(tmp), *COMMAND, "--out", "report.md")
        return (Path(tmp) / "report.md").read_bytes()


def check_4_2(folder: Path, r: C.Report) -> None:
    for name in ("cli.py", "__main__.py"):
        r.need((folder / "miqyas" / name).is_file(), f"miqyas/{name} is there")
    status, output = C.py(folder, "-m", "miqyas", "report", "--help")
    r.need(status == 0 and all(flag in output for flag in ("--readings", "--meters", "--out", "--factor")),
           "the tool describes its four arguments with --help",
           f"python -m miqyas report --help does not list --readings, --meters, --out and --factor: {C.last(output)}")
    with tempfile.TemporaryDirectory() as tmp:
        first, second, strict = (Path(tmp) / name for name in ("a.md", "b.md", "strict.md"))
        status, output = C.py(folder, *COMMAND, "--out", str(first))
        if not r.need(status == 0 and first.is_file(), "the tool runs over the month and writes the report",
                      f"the tool stops or writes nothing: {C.last(output)}"):
            return
        r.need(output == "", "a normal run prints nothing: the report is in the file, messages go to the log",
               f"a normal run printed: {C.last(output)[:80]}")
        C.py(folder, *COMMAND, "--out", str(second))
        r.need(first.read_bytes() == second.read_bytes(), "two runs write the same bytes",
               "two runs over the same month write different files")
        r.need(first.read_bytes() == reference_report("4.2"), "the report is the expected one, byte for byte",
               "the report differs from the expected one: compare its numbers with the notebook's "
               "(17561 kept, 18 anomalies), and write it with newline=\"\\n\"")
        C.py(folder, *COMMAND, "--out", str(strict), "--factor", "2")
        r.need("times the meter's median): 27" in C.text_of(strict), "--factor 2 gives 27 anomalies",
               "--factor 2 does not give 27 anomalies: is args.factor passed on?")
        status, output = C.py(folder, "-m", "miqyas", "report", "--readings", "data/no_such_file.csv",
                              "--meters", "data/meters.csv", "--out", str(Path(tmp) / "none.md"))
        r.need(status == 2 and "Traceback" not in output and output,
               "a missing input ends with exit code 2 and one line, not a traceback",
               f"a missing readings file gives exit code {status}" + (" and a traceback" if "Traceback" in output else ""))
        status, output = C.py(folder, *COMMAND, "--out", str(first), "-v")
        r.need(output.count("INFO") >= 3, "with -v the steps are logged",
               "with -v fewer than three INFO lines are logged: log.info what each step did")
    source = "".join(C.text_of(p) for p in sorted((folder / "miqyas").glob("*.py")))
    r.need(not re.search(r"^\s*print\(", source, re.M), "the package logs and returns; it does not print",
           "the package still calls print(): use log.info for messages")
    C.typed(r, folder, "miqyas")


def check_4_3(folder: Path, r: C.Report) -> None:
    file = "test_anomalies.py"
    if not r.need((folder / file).is_file(), f"{file} is there"):
        return
    written = len(re.findall(r"^def test_\w+", C.text_of(folder / file), re.M))
    r.need(written >= 6, f"{written} tests: the supplied one and at least five of yours",
           f"{written} tests: write at least five beside the supplied one")
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(folder / file, Path(tmp) / file)
        labtool.package(Path(tmp))
        status, output = C.py(Path(tmp), "-m", "pytest", "-q", "-p", "no:cacheprovider", file)
        if not r.need(status == 0, f"the tests pass on the real rule ({C.last(output)})",
                      f"a test fails on the real rule, so the test is wrong: {C.last(output)}"):
            return
        for name in labtool.VARIANTS:
            labtool.package(Path(tmp))
            labtool.variant(Path(tmp), name)
            status, _ = C.py(Path(tmp), "-m", "pytest", "-q", "-p", "no:cacheprovider", file)
            r.need(status == 1, f"a test fails when {name}",
                   f"every test still passes when {name}: which example would tell the two rules apart?")


def own_words(folder: Path) -> str:
    """What the participant wrote in explanation.md, without the template's own lines."""
    supplied = set((labtool.KIT / "start" / "4.4" / "explanation.md").read_text(encoding="utf-8").splitlines())
    lines = [line for line in C.text_of(folder / "explanation.md").splitlines() if line not in supplied]
    return re.sub(r"<!--.*?-->", "", "\n".join(lines), flags=re.S)


def check_4_4(folder: Path, r: C.Report) -> None:
    checks3.log_complete(r, folder, ["Defect C"])
    log = C.text_of(folder / "tutor_log.md")
    r.need(log.count("**Tutor:**") >= 1, "tutor_log.md holds at least one exchange with the tutor",
           "tutor_log.md is missing or empty: ask the tutor for one hint (uv run ../tutor.py --recorded)")
    text = own_words(folder)
    r.need(C.words(text) >= 40, f"explanation.md: {C.words(text)} words of your own",
           f"explanation.md has {C.words(text)} words of your own; write at least forty")
    r.need(not re.search(r"`|fromkeys\(|\[\]|\{\}", text), "the explanation is in words, without code",
           "explanation.md contains code: say it in words a colleague could follow")
    if r.need((folder / "test_regression.py").is_file(), "test_regression.py is there"):
        C.tests(r, folder, "test_regression.py", "the regression test, on your fixed package")
        r.need(checks3.fails_on(folder, "test_regression.py", ["D3"]), "the regression test fails when defect C is put back",
               "no test fails when defect C is put back: the test does not guard against it")
    numbers = checks3.month_numbers(r, folder)
    if numbers:
        with tempfile.TemporaryDirectory() as tmp:
            for name in labtool.DATA["4.4"]:
                data.write(name, Path(tmp))
            labtool.package(Path(tmp))
            expected, _ = C.probe(Path(tmp), checks3.MONTH)
        assert isinstance(expected, list)
        r.need(numbers[3] == expected[3], "each district shows its own anomalies: " + json.dumps(expected[3]),
               f"the districts show {json.dumps(numbers[3])}; expected {json.dumps(expected[3])}")
    C.typed(r, folder, "miqyas")


C.CHECKS.update({"4.1": check_4_1, "4.2": check_4_2, "4.3": check_4_3, "4.4": check_4_4})
