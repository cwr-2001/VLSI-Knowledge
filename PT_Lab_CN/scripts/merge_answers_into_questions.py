#!/usr/bin/env python3
"""Merge answerBox content into the preceding questionBox, right after each question.

Removes standalone green answerBox frames so each 答 follows its 问题 in the same box.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parents[1] / "chapters"

QUESTION_BOX_RE = re.compile(
    r"\\begin\{questionBox\}(.*?)\\end\{questionBox\}",
    re.DOTALL,
)
ANSWER_BOX_RE = re.compile(
    r"\\begin\{answerBox\}(.*?)\\end\{answerBox\}",
    re.DOTALL,
)
QNUM_RE = re.compile(r"\\textbf\{问题\s*(\d+)\.?\}")
# Split questionBox body into per-question chunks (keep delimiter)
Q_SPLIT_RE = re.compile(r"(?=\\textbf\{问题\s*\d+\.?\})")


def strip_answer_prefix(body: str, n: int) -> str:
    """Remove leading '\\textbf{问题 N.}' from an answer body."""
    body = body.strip()
    pat = re.compile(
        rf"^\\textbf\{{问题\s*{n}\.?\}}\s*",
    )
    body, cnt = pat.subn("", body, count=1)
    return body.strip()


def format_answer(n: int, body: str) -> str:
    rest = strip_answer_prefix(body, n)
    # Drop leading TeX control-space left from "\textbf{问题 N.}\ text"
    if rest.startswith("\\ "):
        rest = rest[2:].lstrip()
    elif rest.startswith("\\") and len(rest) > 1 and rest[1].isspace():
        rest = rest[2:].lstrip()
    if not rest:
        return "\\textbf{答：} （见上文）"
    # If answer starts with a listing/environment, put 答： on its own line
    if rest.startswith("\\begin") or rest.startswith("\\["):
        return f"\\textbf{{答：}}\\\\\n{rest}"
    return f"\\textbf{{答：}} {rest}"


def extract_following_answers(text: str, start: int) -> tuple[dict[int, str], list[str], int]:
    """From position start, collect consecutive answerBoxes (and interstitial prose).

    Returns (answers_by_num, orphan_chunks_in_order, end_pos).
    """
    answers: dict[int, str] = {}
    orphans: list[str] = []
    pos = start
    last_n: int | None = None

    while True:
        # Skip whitespace
        ws = re.match(r"\s*", text[pos:])
        assert ws
        pos2 = pos + ws.end()
        if pos2 >= len(text):
            break

        # Optional prose before next answerBox (not starting with \)
        # Allow short prose lines like ［可选步骤］
        if not text.startswith(r"\begin{answerBox}", pos2):
            # Stop if next non-space is not answerBox and not plain prose before an answerBox
            m_box = re.search(r"\\begin\{answerBox\}", text[pos2:])
            if not m_box:
                break
            # If something else structural appears before the next answerBox, stop
            gap = text[pos2 : pos2 + m_box.start()]
            # Allow only prose (no \begin{questionBox}, \item, \section, \subsection, \end{enumerate})
            if re.search(
                r"\\begin\{questionBox\}|\\item\b|\\section\b|\\subsection\b|\\end\{enumerate\}|\\end\{itemize\}",
                gap,
            ):
                break
            # If gap has a latex environment other than nothing, be careful
            if r"\begin{" in gap and r"\begin{answerBox}" not in gap:
                break
            prose = gap.strip()
            box_start = pos2 + m_box.start()
        else:
            prose = ""
            box_start = pos2

        end_m = re.search(r"\\end\{answerBox\}", text[box_start:])
        if not end_m:
            raise ValueError("unclosed answerBox")
        box_end = box_start + end_m.end()
        inner = text[box_start + len(r"\begin{answerBox}") : box_end - len(r"\end{answerBox}")]
        nums = [int(x) for x in QNUM_RE.findall(inner)]

        if nums:
            n = nums[0]
            chunk = inner.strip()
            if prose:
                # Keep prose with this answer (rare)
                chunk = prose + "\n\n" + chunk
            answers[n] = chunk
            last_n = n
        else:
            # Continuation / orphan — attach to last answer if any
            extra = inner.strip()
            if prose:
                extra = prose + "\n\n" + extra
            if last_n is not None and last_n in answers:
                answers[last_n] = answers[last_n] + "\n\n" + extra
            else:
                orphans.append(extra)

        pos = box_end

    return answers, orphans, pos


def merge_box(qbody: str, answers: dict[int, str]) -> str:
    """Rebuild questionBox body with answers inlined after each question."""
    parts = [p for p in Q_SPLIT_RE.split(qbody) if p.strip() != ""]
    # First part may be leading whitespace only
    out: list[str] = []
    used: set[int] = set()

    for part in parts:
        m = re.match(r"\\textbf\{问题\s*(\d+)\.?\}", part.strip())
        if not m:
            out.append(part.rstrip())
            continue
        n = int(m.group(1))
        # Remove trailing \\ that was separating questions, and trailing whitespace
        qtext = part.rstrip()
        # Drop a final \\ (line break between questions) — we'll restructure
        qtext = re.sub(r"\\\\\s*$", "", qtext).rstrip()

        block = qtext
        if n in answers:
            used.add(n)
            ans = format_answer(n, answers[n])
            block = qtext + "\\\\[0.35em]\n" + ans
        out.append(block)

    missing = sorted(set(answers) - used)
    if missing:
        # Append any answers that weren't matched (shouldn't happen often)
        for n in missing:
            out.append(format_answer(n, answers[n]))

    return "\n\n".join(out) + "\n"


def process(text: str, path: Path) -> str:
    out: list[str] = []
    pos = 0
    for m in QUESTION_BOX_RE.finditer(text):
        out.append(text[pos : m.start()])
        qbody = m.group(1)
        qnums = [int(x) for x in QNUM_RE.findall(qbody)]
        answers, orphans, end = extract_following_answers(text, m.end())

        # Only consume answers that belong to this question box
        relevant = {n: answers[n] for n in qnums if n in answers}
        extras = {n: answers[n] for n in answers if n not in qnums}
        if extras:
            # Should not happen if answers are contiguous after the box
            print(f"WARNING {path.name}: unused answers after Q{qnums}: {sorted(extras)}")

        new_body = merge_box(qbody, relevant)
        out.append("\\begin{questionBox}\n" + new_body + "\\end{questionBox}")

        if orphans:
            for o in orphans:
                out.append("\n\n" + o)

        # If we didn't use some answers that were between this and next content,
        # keep them only if they weren't in relevant — already warned
        for n, body in extras.items():
            out.append(
                "\n\n\\begin{questionBox}\n"
                + f"\\textbf{{问题 {n}.}}\\\\[0.35em]\n"
                + format_answer(n, body)
                + "\n\\end{questionBox}"
            )

        pos = end

    out.append(text[pos:])
    result = "".join(out)

    # Safety: no answerBox should remain (except we might have missed end-of-chapter section)
    leftover = ANSWER_BOX_RE.findall(result)
    if leftover:
        print(f"WARNING {path.name}: {len(leftover)} answerBox left")

    return result


def main() -> int:
    files = sorted(p for p in CHAPTERS.glob("*.tex") if re.match(r"\d+_lab", p.name))
    for path in files:
        text = path.read_text(encoding="utf-8")
        if r"\begin{answerBox}" not in text:
            print(f"SKIP {path.name} (no answerBox)")
            continue
        try:
            new = process(text, path)
        except Exception as e:
            print(f"ERROR {path.name}: {e}", file=sys.stderr)
            return 1
        # Normalize CRLF
        new = new.replace("\r\n", "\n")
        path.write_text(new, encoding="utf-8", newline="\n")
        left = new.count(r"\begin{answerBox}")
        print(f"OK {path.name} (answerBox left={left})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
