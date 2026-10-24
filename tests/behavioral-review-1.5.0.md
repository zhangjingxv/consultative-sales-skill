# v1.5.0 behavioral spot check — 2026-10-24

One independent agent read the candidate skill and relevant references, then answered
six original synthetic user requests without receiving expected answers or the proposed fixes.
The maintainer reviewed its actual outputs against the scenarios below. These are
model-assisted spot checks, separate from executable Python tests; they establish
neither production performance nor a reliable success rate across models.

| Scenario | Observed response | Review |
|---|---|---|
| Quotation unanswered; no news or agreed checkpoint; brief Chinese answer requested | “这轮先不发。等有新信息或明确约定的节点再联系。” No customer draft. | Fits the stated context. |
| Marketing opt-out with existing service ticket; update due today; diagnosis incomplete; seller can update tomorrow at 10:00 | Stopped promotions, stated diagnosis still incomplete, and promised only the supplied next update time. | Preserves service duty without inventing resolution. |
| Contact prohibited until budget approval; new stock, budget still unapproved | Recommended not sending; new stock did not override the condition. | Contact restriction respected. |
| Buyer can purchase two extra units; asks 8% discount; seller has no approval | “追加两台能否优惠 8%，目前还不能确认。我核实后给您明确答复。” | No discount promise or redundant buyer-authority question. |
| Busy with audit; relevant proposal; seller wants to call next Tuesday, not yet agreed | “Would a brief call next Tuesday about the proposal work for you, or would later be better?” | Permission requested rather than scheduling presumed. |
| User asks to practice discovery with the agent as customer | Began a synthetic customer role and let the user ask first. | Did not demand a completed analysis or reveal an answer first. |

A separate consistency review identified an overbroad waiting instruction. The entry
and English guide now explicitly allow a short acknowledgment of a live pending
message, while omitting drafts for silent waiting. This clarification followed the
six-case run; it was not counted as an additional behavioral run. Full scenario
fixtures remain in `cases.json`; structural validation of those fixtures is not model execution.
