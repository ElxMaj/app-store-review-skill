# Rejection recovery playbook

Use this only after preserving Apple's exact message and the submitted build or metadata context. Apply `references/evidence-policy.md` to every claim.

## Contents

1. Build the case record
2. Map the rejection
3. Choose the response path
4. Guideline 4.3 playbook
5. Draft the reply
6. Escalation and resubmission
7. Prevent recurrence

## 1. Build the case record

Capture before advising:

- app version and build
- submission and rejection timestamps
- guideline number and exact Apple wording
- screenshots or attachments Apple supplied
- device and OS named by Apple, if any
- prior messages, resubmissions, and changes
- current binary, metadata, review notes, and demo credentials
- whether the issue is reproducible

Do not infer the rejected build from the current branch when they differ.

## 2. Map the rejection

| Apple wording or situation | Likely family | First investigation |
|---|---|---|
| Bug, crash, blank screen, or unable to proceed | 2.1 completeness | Reproduce the exact path, device, account, network, and backend state |
| Unable to sign in or information needed | Review access, often 2.1 | Credentials, region blocks, MFA, demo mode, setup, and reviewer notes |
| Screenshot, description, keyword, or platform mismatch | 2.3 metadata | Compare every claim and image with the rejected build |
| External payment or purchase method | 3.1 | Classify the good, storefront, entitlement, and exact purchase path |
| Subscription terms or restore issue | 3.1.2 | Inspect billed price, period, trial conversion, links, and restore behavior |
| Minimum functionality or web-wrapper concern | 4.2 | Identify native value, core depth, and whether product work is required |
| Similar binary, metadata, concept, or spam | 4.3 | Preserve the phrase and use the 4.3 playbook below |
| Commercialized template or generation service | 4.2.6 | Establish content-provider eligibility and code or template provenance |
| Login alternative | 4.8 | Check the current text and exceptions, then inspect all login choices |
| Collection, consent, deletion, or data sharing | 5.1 | Trace the exact data and user-control flow |
| Third-party AI data sharing | 5.1.2(i) | Identify data, provider, disclosure, permission, and call order |
| UGC, chat, reporting, or abuse | 1.2 | Exercise filtering, report, block, contact, and moderation operations |

If the wording is ambiguous, ask one precise interpretation question. Do not make several unrelated changes in the hope that one satisfies Apple.

## 3. Choose the response path

### FIX

Choose when the finding is correct or the submitted evidence cannot satisfy the rule.

Provide:

- root cause
- exact change
- build number containing the change
- verification steps
- attachment showing the corrected route when helpful

### CLARIFY

Choose when the feature exists but Apple could not find, access, or understand it.

Provide:

- numbered tap path using exact screen and control names
- working credentials and codes
- region or hardware setup
- a short screenshot sequence or recording when it reduces search cost

`DOCUMENTED CASE`: Developers have reported approvals after exact navigation and visual evidence clarified a paywall or purchase route. This supports the tactic, not a guaranteed outcome.

### APPEAL

Choose only when:

- the build complies with the current rule
- the reviewer has the required access and evidence
- clarification failed or the dispute concerns the guideline's application
- the developer can make a concise, factual case

An appeal is not a substitute for fixing a clear crash, purchase, consent, or access defect. Do not promise a specific Board timeline.

### REQUEST INTERPRETATION

Choose when Apple's message does not identify the capability, comparator, or expected change well enough to act safely.

Ask one concrete question, for example:

> Could you identify the specific capability or screen that does not satisfy Guideline 4.2 so we can address the issue directly?

Use a Resolution Center call request or Meet with Apple to understand the rule's application, not as an approval shortcut.

## 4. Guideline 4.3 playbook

### Calibrated model

`OFFICIAL`: Apple's public wording covers multiple Bundle IDs of the same app and apps that are indistinguishable from what is already widely available. Apple and its forum guidance also discuss source, assets, templates, metadata, and concept in spam cases.

`OBSERVED PATTERN`: Very fast 4.3 decisions are consistent with automated or assisted similarity triage.

`INFERENCE`: Public evidence does not reveal Apple's classifier, feature weights, comparison corpus, or whether a particular decision was fully automated. Never present symbol hashing, metadata embeddings, device graphs, or asset hashing as confirmed implementation details.

### Separate 4.3(a) from 4.3(b)

- 4.3(a): portfolio duplication, repeated Bundle IDs, white-label variants, shared template or lineage concerns.
- 4.3(b): an app or category entry is not meaningfully different or improved, or reads as mediocre, low-quality, or low-effort under the current text.

The remedy differs. 4.3(a) often requires consolidation or provenance evidence. 4.3(b) often requires stronger product distinction, not a longer appeal.

### Build a fingerprint evidence table

| Dimension | What to establish | Confidence |
|---|---|---|
| Portfolio overlap | Sibling apps, Bundle IDs, shared features, white-label variations | OFFICIAL when it maps to 4.3(a) |
| Template provenance | Commercial template, generator, starter kit, content owner, license, transformation | OFFICIAL for 4.2.6; case-specific for 4.3 |
| Source lineage | Upstream project, inherited namespaces, dependencies, prior owners | DOCUMENTED CASE when supported by the app's history |
| Assets | Icon and major asset reuse across the portfolio or source kit | DOCUMENTED CASE as a remediation signal, not a universal trigger |
| Metadata and concept | Audience, first sentence, screenshots, first-run flow, category framing | OFFICIAL that metadata and concept matter in cited spam wording |
| Framework | How much behavior is unique beyond Flutter, React Native, Capacitor, Godot, or another engine | INFERENCE unless Apple's message or provenance supports it |
| Account association | Prior ownership, transfers, contractors, or an alleged terminated-account match | Case-specific; do not guess hidden identifiers |

### Remediation table

| Action | Recommendation | Evidence confidence |
|---|---|---|
| Consolidate near-identical apps into one configurable app | Strong when 4.3(a) concerns a portfolio of variants | OFFICIAL |
| Build a meaningfully different workflow for a specific audience | Strong when 4.3(b) is factually justified | OFFICIAL principle |
| Prove ownership and provenance | Strong for a false match or inherited project | DOCUMENTED CASE |
| Replace a reused or near-identical icon and key assets | Consider when asset overlap is real | DOCUMENTED CASE, isolated outcomes |
| Explain framework-common code and enumerate unique behavior | Use for a plausible framework false positive | DOCUMENTED CASE, limited sample |
| Rewrite generic metadata around a specific user and job | Useful for 4.3(b), but insufficient for a thin product | OFFICIAL principle plus OBSERVED PATTERN |
| Recolor screens or rename controls without product change | Do not treat as sufficient | OBSERVED PATTERN |
| Obfuscate code to evade similarity checks | Do not recommend | Unsupported and deceptive |
| Move an unchanged app to another account | Do not recommend | High enforcement risk and does not solve provenance |
| Repeatedly resubmit an unchanged build | Do not recommend | Adds no new evidence and can prolong the loop |

### 4.3 clarification or appeal packet

Include only evidence that exists:

1. one-sentence purpose and specific audience
2. comparison table of the app's concrete workflows, not marketing adjectives
3. ownership, license, or transformation evidence
4. explanation of shared framework code when relevant
5. product-page and first-run screenshots showing distinct value
6. changes in the new build
7. one precise request for re-review or clarification

Do not say "built from scratch" unless repository history and provenance support it.

## 5. Draft the Resolution Center reply

Apple's current App Store Connect Help confirms that developers can correspond with App Review and attach screenshots or supporting documents. It does not prescribe an ideal word count.

Use this shape:

```text
Thank you for the review of version <VERSION>, build <BUILD>, under Guideline <NUMBER>.

We <fixed the issue | would like to clarify the review path>:
1. <Exact screen and control>
2. <Next action>
3. <Expected result>

<For a fix: state the root cause and exact change.>
<For access: provide credential placeholders, region, setup, and attachment names.>
<For 4.3: summarize specific audience, unique workflow, and provenance evidence.>

Please let us know if you need <one specific missing detail>, or re-review build <BUILD> using the steps above.
```

Quality checks:

- factual and respectful
- exact navigation and build number
- no emotional argument or legal threat
- no promise to fix a known issue after approval
- no unverified claim
- attachments named in the message
- one requested next action

## 6. Escalation and resubmission

- Use a new build when the binary or bundled configuration changed.
- A metadata-only issue may permit resubmitting the same build after correcting the metadata, as Apple's current help explains.
- Use App Review Board appeal for a supported disagreement, not for a defect.
- Use expedited review only for a qualifying urgent circumstance. It changes queue priority, not the guideline result.
- Use Meet with Apple or a requested call to clarify interpretation or evidence expectations.
- Do not tell the user an escalation will complete within a specific number of days. Public anecdotes vary and Apple does not guarantee those case timelines.

## 7. Prevent recurrence

After resolution:

1. record the exact rejection trigger and evidence
2. add a regression check or manual checklist item
3. update App Review Notes for non-obvious access
4. preserve the approved reply and attachments
5. rerun Mode A on the release candidate
6. run Mode C when the issue touched 4.2 or 4.3

When contributing the case back to this skill, include the wording, changes, outcome, date, and URL. A case without an outcome belongs in an open-evidence queue, not the remediation table.
