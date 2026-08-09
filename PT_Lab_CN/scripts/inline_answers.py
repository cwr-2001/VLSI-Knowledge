#!/usr/bin/env python3
"""Move per-question answerBox blocks to sit immediately after their questionBox."""
from __future__ import annotations

import re
import sys
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parents[1] / "chapters"

NOTE_RE = re.compile(
    r"\\subsection\{答案 / 解答\}\s*"
    r"(?:\\label\{[^}]+\}\s*)?"
    r"\\noindent\\textit\{Answers / Solutions\}\s*"
    r"本实验手册在每个 Lab 后半部分给出全部问题的答案与解答。\s*"
    r"若答题需要帮助，或希望核对结果，请查阅本 Lab 后部的解答章节。\s*",
    re.DOTALL,
)

SOL_SPLIT = re.compile(r"\\section\{答案 / 解答\}")
ANSWER_BOX_INNER = re.compile(
    r"\\begin\{answerBox\}(.*?)\\end\{answerBox\}",
    re.DOTALL,
)
QUESTION_BOX_RE = re.compile(
    r"(\\begin\{questionBox\}.*?\\end\{questionBox\})",
    re.DOTALL,
)
QNUM_RE = re.compile(r"\\textbf\{问题\s*(\d+)\.?")


def undouble_newlines(text: str) -> str:
    """Undo files where every newline was accidentally doubled."""
    text = text.replace("\r\n", "\n")
    lines = text.splitlines()
    empty = sum(1 for L in lines if L == "")
    if lines and empty / len(lines) > 0.35:
        text = text.replace("\n\n", "\n")
    return text


def extract_answers(solutions: str) -> dict[int, str]:
    """Map question number -> text to insert (answerBoxes + optional prose)."""
    answers: dict[int, str] = {}
    current: int | None = None
    pos = 0
    while True:
        m = re.search(r"\\begin\{answerBox\}", solutions[pos:])
        if not m:
            break
        start = pos + m.start()
        end_m = re.search(r"\\end\{answerBox\}", solutions[start:])
        if not end_m:
            raise ValueError("unclosed answerBox")
        end = start + end_m.end()
        box = solutions[start:end].strip()

        preamble = solutions[pos:start].strip()
        preamble = re.sub(
            r"^\\label\{[^}]+\}\s*"
            r"(?:\\noindent\\textit\{Answers / Solutions\}\s*)?",
            "",
            preamble,
        ).strip()

        body = ANSWER_BOX_INNER.match(box)
        if not body:
            raise ValueError(f"bad answerBox:\n{box[:200]}")
        nums = [int(n) for n in QNUM_RE.findall(body.group(1))]

        if nums:
            n = nums[0]
            if n in answers:
                raise ValueError(f"duplicate answer for 问题 {n}")
            chunk = box if not preamble else preamble + "\n\n" + box
            answers[n] = chunk
            current = n
        else:
            if current is None:
                raise ValueError(f"orphan answerBox:\n{box[:200]}")
            extra = box if not preamble else preamble + "\n\n" + box
            answers[current] = answers[current] + "\n\n" + extra

        pos = end
    return answers


def process(text: str, path: Path) -> str:
    text = undouble_newlines(text)
    parts = SOL_SPLIT.split(text, maxsplit=1)
    if len(parts) != 2:
        raise ValueError(f"{path.name}: missing \\section{{答案 / 解答}}")

    body, solutions = parts
    answers = extract_answers(solutions)

    body2, nsub = NOTE_RE.subn("\n", body, count=1)
    if nsub != 1:
        print(f"WARNING {path.name}: answers-note not removed ({nsub})")

    used: set[int] = set()

    def repl_qbox(m: re.Match[str]) -> str:
        qbox = m.group(1)
        qnums = [int(n) for n in QNUM_RE.findall(qbox)]
        if not qnums:
            return qbox
        chunks = [qbox]
        for n in qnums:
            if n not in answers:
                raise ValueError(f"{path.name}: no answer for 问题 {n}")
            if n in used:
                raise ValueError(f"{path.name}: 问题 {n} already inlined")
            used.add(n)
            chunks.append("")
            chunks.append(answers[n])
        return "\n".join(chunks)

    new_body = QUESTION_BOX_RE.sub(repl_qbox, body2)
    missing = sorted(set(answers) - used)
    if missing:
        raise ValueError(f"{path.name}: answers not placed: {missing}")
    return new_body.rstrip() + "\n"


def main() -> int:
    files = sorted(p for p in CHAPTERS.glob("*.tex") if re.match(r"\d+_lab", p.name))
    for path in files:
        text = path.read_text(encoding="utf-8")
        if r"\section{答案 / 解答}" not in text:
            print(f"SKIP {path.name} (already inlined)")
            continue
        try:
            new = process(text, path)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        path.write_text(new, encoding="utf-8", newline="\n")
        print(f"OK {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
