# Observable decision labels

These labels describe actions, not certainty about customer intent. Match observable
behavior and check the counterexample. The behavior assertions in the scenario fixtures
still require contextual evaluation; defining labels alone does not validate a reply.
All labels follow the entrypoint's evidence, consent and commercial boundaries.
The `required` and `forbidden` fields are behavior assertions awaiting execution, not results.
JSON parsing and vocabulary audits do not execute them; actual model replies need separate
evaluation and recorded evidence before any behavioral pass can be claimed.

### acknowledge_and_own_action
- Use when: an existing issue needs owned follow-through, or a correction provides enough information to select a verification action, with no confirmed update time yet.
- Observable behavior: acknowledge the issue or misunderstanding, reuse known information, and offer a specific action within the user's responsibility; stop acting on the replaced assumption.
- Counterexample: comfort without fulfilling duties, requesting known details again, or admitting an error without changing the action.
- Boundary: never invent authority, service scope, repair time or completed execution; existing update commitments still apply.

### answer_with_evidence_limits
- Use when: a concept can be explained now or the customer makes an unverified performance inference, without actual measurements.
- Observable behavior: answer directly in plain language, separate principles, conditions and unknowns, and explain needed verification; analogies aid understanding only.
- Counterexample: evade an answer with questions, treat an analogy as a benchmark, or use jargon to hide uncertainty.
- Boundary: never invent measurements, compatibility conclusions, returns or a definite improvement magnitude.

### acknowledge_and_own_next_checkpoint
- Observable behavior: acknowledge the stated fact and own a feasible update checkpoint.
- Counterexample: a bare “received” or an unverified outcome/resolution promise.

### acknowledge_impact_then_own_checkpoint
- Observable behavior: acknowledge the already stated impact, then own a response checkpoint.
- Counterexample: minimize harm or skip directly to excuses or solutions.

### align_criteria_and_sequence
- Observable behavior: list confirmed evaluation criteria and ask for their priority/sequence.
- Counterexample: decide weights for the customer or hide conflicting criteria.

### brief_orientation_then_discovery
- Observable behavior: briefly state relevant identity/capability, then ask one scene-setting question.
- Counterexample: long introduction, multiple questions or invented case credentials.

### clarify_and_route
- Observable behavior: clarify the decisive fact and hand off project verification.
- Counterexample: issue an unverified configuration, quote or delivery commitment in chat.

### clarify_basis
- Observable behavior: state the known comparison scope and assumptions, then clarify one decisive benchmark or cost input; accurately calculate any subtotal already supported by the inputs.
- Counterexample: immediately argue, disparage competitors or discount; treat omitted costs as zero, assumed labor value as cash savings, or incomplete inputs as proof of complete TCO, payback or returns.

### clarify_one_fact
- Observable behavior: clarify or request one fact that changes the next decision. If customer content is inaccessible, state the access limit and request one user-selected excerpt.
- Counterexample: a questionnaire or using questions to evade an answer already supported by evidence.

### clarify_review_criterion_or_node
- Observable behavior: ask for one internal review criterion or checkpoint.
- Counterexample: simultaneously interrogate budget, criteria and timing or pressure the process.

### clarify_risk_and_evidence
- Observable behavior: identify the stated risk and required proof/assessment basis.
- Counterexample: unconditional safety/compliance reassurance without evidence.

### close
- Observable behavior: close briefly; preserve an entry point only if welcome and useful. If an all-contact boundary was already acknowledged and no obligation remains, stop silently without another farewell.
- Counterexample: append a new pitch/question, invite contact after an explicit no-contact boundary, or bypass it through comments, reactions or another account.
  For a verified product mismatch, explain the gap and stop recommending that option, without ending ordinary contact or existing service duties. Unverified alternatives remain unknown.

### close_or_wait
- Observable behavior: stop business chasing or sales-meeting requests when only politeness is observed and no buying next step exists; close or wait without prohibiting genuine, appropriate and unrestricted social conversation.
- Counterexample: convert a polite response into buying interest, force a meeting, or refuse to respond to a voluntarily shared interest solely because no lead exists.

### confirm_and_route
- Observable behavior: acknowledge the specific requirements, own a feasible next update and use the project workflow.
- Counterexample: invent availability, price or delivery before verification.

### confirm_logistics
- Observable behavior: confirm agreed time, location/access and participants coherently.
- Counterexample: repeated fragmented requests or treating changes as accepted without agreement.

### confirm_purchase_next_step
- Observable behavior: when the necessary technical, commercial and purchasing conditions are confirmed and the customer explicitly wants to buy, use those terms to propose one specific action for the authorized person, such as a purchase request or purchase order, and state the seller's supporting task. Distinguish a proposed step from a completed order.
- Counterexample: repeat completed discovery, wait indefinitely, treat interest or silence as an order, or submit, sign, ship, invent approval or add unconfirmed conditions without authority.

### explore_backup_only
- Observable behavior: respect the existing supplier and explore one backup trigger if appropriate.
- Counterexample: attack that supplier or demand replacement.

### follow_up_on_new_value
- Observable behavior: with no applicable refusal or with renewed permission, contact with one verified new relevant fact and an optional next action.
- Counterexample: ask whether the quotation was read without a trigger, or fabricate one.

### identify_role_path
- Observable behavior: clarify the contact's scope and a voluntary introduction path.
- Counterexample: bypass the contact or pressure internal advocacy.

### map_remaining_decision_path
- Observable behavior: summarize known participants and ask which remaining steps need confirmation.
- Counterexample: assume only one approval remains or speculate about internal politics.

### natural_relationship_reply
- Observable behavior: respond naturally to a concrete, time-grounded detail voluntarily shared by the customer or appropriate to the existing relationship, without an applicable contact prohibition. A greeting, congratulations or curiosity need not include a question or business transition. Honor welcome interest conversation separately from a marketing opt-out.
- Counterexample: invent a shared experience, append a product or buying request to every exchange, infer purchase intent from hobby enthusiasm, describe an old post as current, bypass an all-contact boundary socially, or claim to have read inaccessible content.

### recap_commitments
- Observable behavior: recap agreed owners, actions and dates plus a checkpoint.
- Counterexample: recap only the seller's pitch or rewrite discussion as agreement.

### reduce_cost
- Observable behavior: propose one feasible reduction in effort, scope or process and explain the trade-off.
- Counterexample: hide consequences or demand commitment using unapproved/fabricated concessions.
  Real authorized exchanges follow negotiation rules.

### respect_boundary_and_enable_forwarding
- Observable behavior: accept the declined introduction; offer a neutral summary only if further material is welcome.
- Counterexample: repeat the request, send unwanted material or contact colleagues without consent.

### short_mode
- Observable behavior: give a concise decision and a reply only when a response is needed; for silent waiting, say not to send and omit the draft.
- Counterexample: long theory, multiple alternatives or tables when brevity was requested.

### support_internal_review
- Observable behavior: provide neutral, verifiable points for internal discussion while preserving unknown approvals.
- Counterexample: turn individual support into organizational approval or invent supporting cases.

### synthesize_then_clarify
- Observable behavior: synthesize verified information, then ask one priority question.
- Counterexample: question every detail or treat inference as confirmed fact.

### turn_intent_into_mutual_action
- Observable behavior: offer a concrete optional action and agree its timing rather than assume commitment.
- Counterexample: start production or dispatch based on vague interest.

### verify_authority
- Observable behavior: identify whose authority is missing. For a seller's unapproved discount, keep the current quote and verify approval for the actual scope before promising; for buyer authority, establish purchasing scope and process role.
- Counterexample: treat a requested discount as seller approval, confuse missing seller permission with missing buyer authority, or encourage either party to overcommit.

### wait
- Observable behavior: stop business chasing when asked to slow down or when there is no new business basis, due commitment or required service update. Acknowledge a live message only if needed; do not send another acknowledgment into silence. Retain only agreed or explicitly authorized business recontact conditions. Handle genuine, appropriate and unrestricted social conversation separately.
- Counterexample: resume the same sales chase the next day, bypass a restriction through another channel, or prohibit ordinary interest conversation solely because no purchasing information exists.
  Necessary safety, correction, risk and service updates continue under existing duties.
