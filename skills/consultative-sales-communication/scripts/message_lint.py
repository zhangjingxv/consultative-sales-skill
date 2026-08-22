#!/usr/bin/env python3
"""Conservative lint for Chinese customer-visible sales messages."""

from __future__ import annotations

import argparse
import json
import re


RULES = [
    (
        "unsupported-certainty",
        "high",
        re.compile(r"(保证|绝对|百分之百|100%|肯定没问题|一定能|完全兼容)"),
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
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    result = {"ok": not lint(args.text), "findings": lint(args.text)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
