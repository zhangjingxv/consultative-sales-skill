#!/usr/bin/env python3
"""Conservative lint for Chinese customer-visible sales messages."""

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
        re.compile(r"(绝对|百分之百|100%|肯定没问题|一定能|完全兼容)"),
        "可能存在无证据的确定性承诺。",
    ),
    (
        "commercial-claim",
        "high",
        re.compile(r"(全网最低|最低价|最后一天|仅剩\d+|现货充足|领导已经批了)"),
        "价格、库存、期限或审批表述需要当前证据。",
    ),
    (
        "empty-chase",
        "medium",
        re.compile(r"(在吗|考虑得怎么样|怎么不回复|看过了吗|什么时候定)"),
        "可能是没有新价值的催促。",
    ),
    (
        "pressure",
        "high",
        re.compile(r"(必须|赶紧|错过就没有|不买就|今天必须|别再犹豫)"),
        "可能制造不当压力或假紧迫。",
    ),
    (
        "internal-commercial-data",
        "high",
        re.compile(r"(我们的成本|内部成本|毛利|返点|供应商底价|内部审批备注)"),
        "客户可见文本可能泄露内部商业信息。",
    ),
]

NEGATED_GUARANTEE = re.compile(r"(不|不能|无法|暂不|没法)(先|直接|现在)?保证")
GUARANTEE = re.compile(r"保证")
REQUEST_CUES = re.compile(
    r"(?:方便[^，。！？；]{0,12}(?:发|给|确认|说|回复)|能否|"
    r"可以[^，。！？；]{0,8}(?:发|给|确认|回复)|"
    r"请[^，。！？；]{0,12}(?:发|给|确认|回复)|"
    r"您看[^，。！？；]{0,16}(?:吗|呢)|什么时候[^，。！？；]{0,8}(?:定|确认|回复))"
)


def lint(text: str) -> list[dict[str, str]]:
    findings = []
    question_count = len(re.findall(r"[?？]", text))
    if question_count > 1:
        findings.append(
            {
                "rule": "multiple-questions",
                "severity": "medium",
                "message": f"包含{question_count}个问号，检查是否超过一个主要回应入口。",
            }
        )
    request_count = len(REQUEST_CUES.findall(text))
    if question_count <= 1 and request_count > 1:
        findings.append(
            {
                "rule": "multiple-response-entries",
                "severity": "medium",
                "message": f"检测到约{request_count}个请求入口，检查是否能只保留一个主要下一步。",
            }
        )
    if len(text) > 240:
        findings.append(
            {
                "rule": "long-message",
                "severity": "low",
                "message": f"消息长度为{len(text)}字符，检查能否缩短或转电话／会议。",
            }
        )
    for rule, severity, pattern, message in RULES:
        if pattern.search(text):
            findings.append({"rule": rule, "severity": severity, "message": message})
    guarantee_text = NEGATED_GUARANTEE.sub("", text)
    if GUARANTEE.search(guarantee_text):
        findings.append(
            {
                "rule": "unsupported-certainty",
                "severity": "high",
                "message": "“保证”可能构成无证据的确定性承诺；若已有证据，也应写清适用条件。",
            }
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
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
    result = {"ok": not findings, "findings": findings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
