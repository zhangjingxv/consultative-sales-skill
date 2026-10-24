#!/usr/bin/env python3
"""Offline Chinese/English review cues, not factual or evidence verification.

Each rule occurs once. Its ``matches`` contain exact text and zero-based Python
character offsets (end exclusive), including every occurrence of the cue. Length
is a message-level check and deliberately has no full-message excerpt.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


RULES = [
    (
        "unsupported-certainty",
        "high",
        re.compile(
            r"绝对|百分之百|100\s*%|肯定没问题|一定能|完全兼容|保证|"
            r"\b(?:guarantee(?:d|s)?|absolutely|definitely|certainly|"
            r"fully\s+compatible|risk[- ]free|no\s+risk)\b",
            re.IGNORECASE,
        ),
        "可能存在无证据的确定性承诺。 Review certainty claims and their evidence/conditions.",
    ),
    (
        "commercial-claim",
        "high",
        re.compile(
            r"全网最低|最低价|最后一天|仅剩\d+|现货充足|领导已经批了|"
            r"\b(?:(?:lowest|best)\s+price|last\s+day|today\s+only|"
            r"offer\s+ends\s+today|in\s+stock|plenty\s+of\s+stock|"
            r"only\s+\d+\s+(?:units?|items?|spots?|seats?)\s+(?:left|remaining)|"
            r"(?:management|leadership|(?:my|our|the)\s+(?:manager|boss))\s+"
            r"(?:(?:has|have)\s+)?(?:already\s+)?approved)\b",
            re.IGNORECASE,
        ),
        "价格、库存、期限或审批表述需要当前证据。 Verify current commercial evidence.",
    ),
    (
        "empty-chase",
        "medium",
        re.compile(
            r"在吗|考虑得怎么样|怎么不回复|看过了吗|什么时候定|"
            r"\b(?:are\s+you\s+there|any\s+(?:updates?|news)|"
            r"just\s+(?:checking\s+in|following\s+up)|"
            r"have\s+you\s+(?:seen|read|reviewed)\s+"
            r"(?:it|this|the\s+(?:proposal|quote|email))|"
            r"why\s+haven['’]t\s+you\s+(?:replied|responded)|"
            r"when\s+(?:will|can)\s+you\s+decide)\b",
            re.IGNORECASE,
        ),
        "可能是没有新价值的催促。 Check whether this follow-up adds useful information.",
    ),
    (
        "pressure",
        "high",
        re.compile(
            r"今天必须|必须|赶紧|错过就没有|不买就|别再犹豫|"
            r"\b(?:you\s+(?:must|have\s+to|need\s+to)\s+"
            r"(?:buy|order|decide|sign|pay|confirm)|"
            r"(?:buy|order|decide|sign|pay|confirm)\s+(?:right\s+now|immediately|today)|"
            r"act\s+now|hurry(?:\s+up)?|don['’]t\s+(?:wait|hesitate)|"
            r"before\s+it['’]s\s+too\s+late|miss\s+out)\b",
            re.IGNORECASE,
        ),
        "可能制造不当压力或假紧迫。 Review pressure or urgency language.",
    ),
    (
        "internal-commercial-data",
        "high",
        re.compile(
            r"我们的成本|内部成本|毛利|返点|供应商底价|内部审批备注|"
            r"\b(?:our\s+(?:internal\s+)?costs?|"
            r"internal\s+(?:costs?|pricing|approval\s+notes?)|"
            r"(?:profit|gross)\s+margins?|"
            r"supplier(?:['’]s|s['’]?)?\s+(?:floor|bottom|lowest)\s+price|"
            r"(?:supplier|channel)\s+rebates?|kickbacks?)\b",
            re.IGNORECASE,
        ),
        "客户可见文本可能泄露内部商业信息。 Review internal commercial information.",
    ),
]

# For certainty only, match a negation immediately before a cue. Never remove or suppress an
# entire sentence: a later positive claim must still be reviewed. This is a
# deliberately limited heuristic; quotation, irony and complex scope need review.
NEGATED_PREFIX = re.compile(
    r"(?:不|不能|无法|暂不|没法|没有|并非|不是|不敢|未能|不作|不做|不予)"
    r"(?:先|直接|现在|目前|完全|明确|作出|做出|任何){0,3}\s*$|"
    r"\b(?:cannot|can['’]t|could\s+not|couldn['’]t|do\s+not|don['’]t|"
    r"does\s+not|doesn['’]t|will\s+not|won['’]t|would\s+not|wouldn['’]t|"
    r"should\s+not|shouldn['’]t|must\s+not|mustn['’]t|not|never|no|"
    r"unable\s+to|not\s+able\s+to)"
    r"(?:\s+(?:currently|yet|now|really|honestly|confidently|fully|ever|a|the))*\s+$",
    re.IGNORECASE,
)
REQUEST_CUES = re.compile(
    r"(?:方便[^，。！？；]{0,12}(?:发|给|确认|说|回复)|能否|"
    r"可以[^，。！？；]{0,8}(?:发|给|确认|回复)|"
    r"请[^，。！？；]{0,12}(?:发|给|确认|回复)|"
    r"您看[^，。！？；]{0,16}(?:吗|呢)|什么时候[^，。！？；]{0,8}(?:定|确认|回复))|"
    r"\b(?:(?:can|could|would|will)\s+you\s+(?:please\s+)?"
    r"(?:send|share|confirm|tell|provide|reply|choose|check|review)|"
    r"please\s+(?:send|share|confirm|tell|provide|reply|choose|check|review)|"
    r"let\s+me\s+know)\b",
    re.IGNORECASE,
)
CJK_CHARACTER = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
ENGLISH_WORD = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")


def _locations(matches: list[re.Match[str]]) -> list[dict[str, object]]:
    return [
        {"match": match.group(), "start": match.start(), "end": match.end()}
        for match in matches
    ]


def lint(text: str) -> list[dict[str, object]]:
    """Return review cues; an empty list does not establish factual accuracy."""
    findings: list[dict[str, object]] = []
    questions = list(re.finditer(r"[?？]+", text))
    question_count = len(questions)
    if question_count > 1:
        findings.append(
            {
                "rule": "multiple-questions",
                "severity": "medium",
                "message": f"包含{question_count}处问号，检查是否超过一个主要回应入口。 Review multiple questions.",
                "matches": _locations(questions),
            }
        )
    requests = list(REQUEST_CUES.finditer(text))
    request_count = len(requests)
    if question_count <= 1 and request_count > 1:
        findings.append(
            {
                "rule": "multiple-response-entries",
                "severity": "medium",
                "message": f"检测到约{request_count}个请求入口，检查是否能只保留一个主要下一步。 Review multiple requests.",
                "matches": _locations(requests),
            }
        )
    cjk_count = len(CJK_CHARACTER.findall(text))
    word_count = len(ENGLISH_WORD.findall(text))
    # Roughly 240 Chinese characters or 80 English words; mixed messages use
    # the same combined budget. Spaces and long English spellings add no cost.
    if cjk_count + 3 * word_count > 240:
        findings.append(
            {
                "rule": "long-message",
                "severity": "low",
                "message": (
                    f"消息含约{cjk_count}个中文字符、{word_count}个英文/数字词，"
                    "检查能否缩短或转电话／会议。 Review message length."
                ),
            }
        )
    for rule, severity, pattern, message in RULES:
        matches = [
            match for match in pattern.finditer(text)
            if rule != "unsupported-certainty"
            or not NEGATED_PREFIX.search(text[max(0, match.start() - 100):match.start()])
        ]
        if matches:
            findings.append({
                "rule": rule,
                "severity": severity,
                "message": message,
                "matches": _locations(matches),
            })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Offline Chinese/English review cues; does not verify facts or supporting evidence."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    args = parser.parse_args()
    if args.text is not None:
        content = args.text
    elif args.file is not None:
        content = args.file.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        parser.error("请提供 --text、--file，或通过标准输入传入客户可见文本")
    findings = lint(content)
    result = {
        "ok": not findings,
        "findings": findings,
        "scope": "heuristic-language-cues; facts and supporting evidence are not verified",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
