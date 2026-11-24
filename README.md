# ProofBeforePay

**Know before you commit.** A bilingual, privacy-first **on-device AI safety copilot** for suspicious scholarship, internship, and student job invitations.

Built from scratch for **SLAY HACKS 2026** within the official development window (November 7–December 7, 2026). Educational proof of concept. The underlying project was developed with substantial assistance from OpenAI ChatGPT (GPT-6.2), with a human entrant responsible for review, eligibility, accuracy, and submission.

## What is actually working?

- A working responsive static website built in HTML, CSS and JavaScript; no account or paid API.
- Real in-browser TF-IDF character n-gram + logistic regression inference, with model weights bundled in `model/model.json`.
- English and Traditional Chinese message analysis (mixed languages are experimental).
- Transparent, **separate rules-based** evidence detection for upfront fees, authentication codes, sensitive documents, secrecy, pressure, personal channels and remote access.
- Prioritized independent-verification steps and one-click report copying with **basic** redaction of some common personal identifiers.
- A local counterfactual demo showing how removing an observed substring changes the ML score; **this is not a guarantee of safety**.
- Reproducible synthetic dataset generation, model training, group-disjoint evaluation, cross-runtime equivalence tests and provided screenshots.

## Run it locally (no installation for the app)

1. Extract the ZIP.
2. From the extracted folder, run `python -m http.server 8000` (or any static web server).
3. Visit `http://localhost:8000/` in a modern browser, then select an example or paste a message.

**Don't open `index.html` using `file://`.** Browser security may block loading the model via `fetch` from a local file. Local HTTP or GitHub Pages works.

### Deploy it for free with GitHub Pages

1. Create a **public** GitHub repository and upload all files from this folder to its root (not the surrounding folder).
2. In **Settings → Pages → Build and deployment**, select **Deploy from a branch**, the `main` branch, the `/(root)` directory, then save.
3. Wait for GitHub's published website URL on the Pages settings panel. Your URL will be similar to `https://YOUR_USERNAME.github.io/YOUR_REPO/`.
4. Open it from a logged-out browser and confirm `MODEL READY` appears and all examples work.
5. Paste both the website and repository links into your Devpost submission.

GitHub Pages is free for **public** repositories under GitHub Free. Avoid putting any sensitive tokens or personal data in the public repository. The app works under a repository subpath because all URLs are relative.

## Tests and model reproduction

```bash
# Requires Node.js only for tests, not for the website
node --test tests/test_ml.mjs

# Optional: retrain the model. Requires Python and scikit-learn.
python -m pip install -r requirements-dev.txt
python scripts/build_dataset.py
python scripts/train_model.py
```

The Node suite tests determinism, classifier behavior, and agreement of the JavaScript scores with Python scikit-learn's evaluated holdout scores. `model/evaluation.json` contains the holdout examples, labels, scores and confusion matrix. Responsive browser screenshots were captured from rendered HTML, styles and app logic with a local model fixture; the secure execution environment blocked direct localhost navigation, so actual network delivery should be rechecked after deployment.

## How the AI works

1. Python trains a linear logistic classifier on character n-gram TF-IDF (2–4). This uses actual statistical learning rather than hard-coded risk scores.
2. Training exports a ~230 KB JSON of n-grams, IDF values and linear coefficients, enabling dependency-free inference via `ml.js`.
3. On first page load, the app downloads its **static model file**. Message text is processed only in the browser; the app does not transmit the message.
4. Model output is an **uncalibrated synthetic-data ML signal** on a 0–100 scale, **not a probability that the message is a scam**.
5. Independently defined language-aware rules produce evidence cards and actions. These cards are **not claimed to be faithful feature attribution of the classifier**.

### Evaluation and limits

As of 2026-11-25: **86% accuracy, 0.86 F1 on 28 group-disjoint synthetic holdout messages**. Training consists of 276 augmented synthetic scenario messages covering English and Traditional Chinese. Synthetic results may dramatically overestimate (or underestimate) real-world performance. The model has no real-world fraud validation, sender identity verification, live source verification or production abuse monitoring. It may miss sophisticated scams and falsely flag legitimate announcements. It is not a substitute for official staff, consumer protection agencies, or the appropriate reporting authority.

For details, read [MODEL_CARD.md](MODEL_CARD.md) and [ETHICS_AND_LIMITATIONS.md](ETHICS_AND_LIMITATIONS.md).

## File map

| File / folder | Purpose |
|---|---|
| `index.html`, `styles.css`, `app.js` | Working user interface and interaction logic |
| `ml.js` | Dependency-free browser ML implementation |
| `model/model.json` | Pretrained classifier bundled with app |
| `model/evaluation.json` | Reproducible synthetic evaluation details |
| `scripts/` | Original synthetic dataset builder + training code |
| `data/` | Original synthetic train and holdout JSONL |
| `tests/` | JS/Python equivalence tests + rendered browser test |
| `screenshots/` | Desktop, mobile, English, Chinese and what-if screens |
| `requirements-dev.txt` | Python development dependencies |

## Live demo

[Try ProofBeforePay](https://eve-synth-labs.github.io/proof-before-pay/) — deployed and tested by the human entrant with English and Traditional Chinese examples.

## Data, privacy, and rights

No real scholarship notices, student records or personal inboxes were collected to train the model. Example notices and synthetic training data were authored for the prototype. No LLM API is called. There are no analytics, cookies or localStorage usage. Ordinary web hosting may still record visitor metadata such as IP addresses; **do not claim complete anonymity from the hosting provider**. The "Copy report" feature redacts some common patterns but does not guarantee removal of all identifiable information—review manually before sharing.

Code in this repository is licensed under MIT. The project uses the scikit-learn open-source library in its development/training workflow (not shipped into the website).
