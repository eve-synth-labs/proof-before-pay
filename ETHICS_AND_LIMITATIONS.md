# Responsible AI, privacy and limitations

ProofBeforePay is an **educational decision-support prototype**. It does not verify whether an organization exists, prove fraud, or authenticate claims. It must never be used as the sole basis for accusing a specific person or company of a crime.

## Why local ML

We designed for students who may not want to paste personal opportunity messages into third-party cloud services. The website downloads a public model file, and all risk inference operates inside the browser. It does not make paid API calls, log message text, use analytics, or collect accounts.

## Risks and mitigations

- **False negatives**: a sophisticated scam could be scored as lower risk. Every result directs the user to verify through independently obtained institutional channels.
- **False positives**: official warnings and urgent campus notices can resemble scam language. The interface consistently labels results as a signal, not proof.
- **Model overconfidence**: outputs are uncalibrated; UI explicitly says the percentages are not scam probabilities.
- **Bilingual fairness**: testing includes both languages but with only 14 holdout cases per language, insufficient for population-level fairness conclusions. Do not interpret the sample results as subgroup fairness certification.
- **PII leakage**: users are instructed not to share private credentials. Copying reports uses only basic regex masking; they must review the result before forwarding it.
- **Prompt injection**: the model does not execute instructions found inside analyzed text or visit links.
- **Data provenance**: all model training examples are original synthetic scenarios; none are real individuals' private messages.
- **Outdated signals**: tactics evolve. No ongoing external validation or retraining is claimed.

## Human agency

The user has control over what is scanned and whether a report is copied. The application makes no autonomous reports, complaints, payments or security decisions. It emphasizes the concrete, safer action: navigate to an official site independently and verify using published channels.

## Disclosures in submission

Explicitly state: generative AI assisted product development; ML inference is TF-IDF + logistic regression, **not a large language model**; observed-evidence cards are rules, not feature attribution; synthetic-only evaluation; site contains no paid AI dependencies.
