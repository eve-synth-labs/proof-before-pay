# Model card — ProofBeforePay-charTFIDF-logistic-v1

**Release:** 2026-11-25. **Prototype** / not real-world validated. **Primary user:** a student evaluating scholarships, internships or part-time work invitations.

## Intended use

Help users pause before sending deposits, identity documents or credentials by offering a **non-authoritative ML risk signal**. Use alongside independently verified official contact information. No message is sent to an external AI inference service.

## Method

- Character TF-IDF n-grams, sizes 2–4, with smooth IDF, sublinear term frequency and L2 normalization.
- L2-regularized binary logistic regression trained via scikit-learn 1.8.0.
- Browser inference: original JavaScript implementation with exported weights and IDF.
- Score: logistic model output scaled to 0–100; **not calibrated against any real fraud prevalence**.
- Human-interpretable detection: a **distinct** transparent, regex-based evidence layer; rules and ML can disagree.

## Dataset and split

- All messages are **fictional and originally authored synthetic examples**, not scraped correspondence or real fraud reports.
- Original base messages span deposits, jobs, scholarships, OTPs, privacy, urgency and genuine school announcements in English and Traditional Chinese.
- 276 training examples (base phrases plus contextual prefix variants) from 92 base groups.
- 28 test examples from 28 **disjoint base groups**: 7 positive / 7 negative for each of two languages.
- No copies of test base messages are in training. The scenarios still share common vocabulary, and the corpus is balanced and artificial.

## Evaluation on synthetic holdout only

| Metric | Value |
|---|---:|
| Accuracy | 0.857 (24 / 28) |
| Precision | 0.857 |
| Recall | 0.857 |
| F1 | 0.857 |
| True negative | 12 |
| False positive | 2 |
| False negative | 2 |
| True positive | 12 |

The numbers above **must not be portrayed as deployment accuracy, real-world fraud detection rate, or an anti-scam guarantee**. Refer to `model/evaluation.json` for all scored holdout messages and to `scripts/train_model.py` for reproducibility.

## Limitations and foreseeable errors

1. No externally sourced examples or independent real-world validation; high domain shift risk.
2. English and Traditional Chinese evaluated; mixed-language and adversarial obfuscation not separately measured.
3. Similar vocabulary appears in legitimate warnings and malicious messages, causing possible false positives.
4. High-quality professional phishing and brand impersonation may receive a low score.
5. URLs are not visited or checked against threat feeds; sender identity is not checked.
6. The 0–100 value is not a calibrated probability. Thresholds are UI triage heuristics, not a medical, legal or criminal finding.
7. Rules-based evidence may contain false positives and does not explain the full mathematical model.
8. The model is most relevant to student opportunities; it is not appropriate as a general financial fraud adjudicator.

## Human oversight and recourse

The application does not block messages or report a sender automatically. Users are encouraged to cross-check through an independently found institutional site or phone number before making decisions. Low risk means "fewer signals detected" rather than "safe". Avoid uploading actual student records, bank details or identity documents to public code repositories.

## Privacy and security

The classifier runs in the client. `model.json` is loaded as a local static resource. No user message is transmitted by this application. Standard hosting logs may capture IP addresses, and malicious browser extensions or compromised hosts are outside its control. The optional report copying feature includes *basic pattern-based redaction*, not guaranteed anonymization.

## Provenance / AI disclosure

The entrant commissioned the creation of this project with substantial generative AI assistance (OpenAI GPT-6) for design, code, synthetic examples, model training scripts, tests and submission writing. The entrant must validate the outputs, inspect the code, and ensure eligibility and truthful final submission. No false claim of individually hand-writing all code is made.
