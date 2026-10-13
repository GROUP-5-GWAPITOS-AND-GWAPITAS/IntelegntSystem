# 🖥️ Intelligent Hardware QA Chatbot

A **text-recognition chatbot** that identifies which of the 11 PC hardware components a user is asking about, using **GloVe word embeddings** and **cosine similarity**.

> **Course:** CS for Intelligent Systems  
> **Group 5 · GWAPITOS AND GWAPITAS**  
> **Assigned Algorithm:** #5 — GloVe / Word2Vec (Static Dense Vectors)

---

## 📌 What It Does

Given a user's query, the chatbot:

1. **Preprocesses** the text (lowercasing, punctuation removal, tokenization, stopword removal)
2. **Tries exact/alias matching** — catches acronyms like `cpu`, `psu`, `gpu`, `ram`, and typos via Levenshtein fuzzy matching
3. **Falls back to GloVe** — averages word vectors and computes a similarity **"Matrix"** across all 11 answer-key items
4. **Applies thresholds** to decide: `correct` / `partial` / `unrecognized`
5. **Returns** the matched item plus a short description in the chat UI

### Example Interactions

| User Query              | Bot Response                                                    |
| ----------------------- | --------------------------------------------------------------- |
| `cpu`                   | ✅ **Central Processing Unit** (confidence: 1.00) + description |
| `brain of the computer` | ✅ **Central Processing Unit** (via synonym)                    |
| `keybord` (typo)        | ✅ **Keyboard** (via fuzzy match)                               |
| `psu`                   | ✅ **Power Supply Unit**                                        |
| `screen`                | ✅ **Monitor**                                                  |
| `how to cook adobo`     | ❌ Sorry, that doesn't match any of the 11 hardware items.      |
| ` ` (whitespace only)   | ⚠️ Please type a question about PC hardware parts.              |

---

## 🧠 How the Algorithm Works

**Assigned algorithm:** GloVe (Global Vectors for Word Representation) — a static word embedding model.

### The Three-Layer Pipeline

1. **Exact / alias lookup** — Normalized query compared against a curated alias list per item. Catches acronyms (`psu`, `ssd`) that GloVe may not know.

2. **Levenshtein fuzzy match** — `difflib.SequenceMatcher` compares the query against every alias character-by-character. Ratio ≥ 0.80 = treated as a typo match.

3. **GloVe cosine similarity** — Tokenized query → averaged word vectors → cosine similarity against 11 precomputed item vectors. Produces the **"Matrix"** of scores.

### Similarity Matrix

The final decision comes from an **11×1 column vector** — the **"Matrix"** of cosine similarity scores:

```
         ┌─────────────────────┐
         │ CPU:          0.6851 │
         │ Motherboard:  0.5805 │
         │ RAM:          0.6155 │
query →  │ Storage:      0.5711 │  →  argmax → best match
         │ PSU:          0.4973 │
         │ GPU:          0.5930 │
         │ Case:         0.6841 │
         │ Cooling:      0.5574 │
         │ Monitor:      0.4145 │
         │ Keyboard:     0.5292 │
         │ Mouse:        0.5347 │
         └─────────────────────┘
```

### Decision Thresholds (Empirically Calibrated)

| Score Range | Decision                                  |
| ----------- | ----------------------------------------- |
| ≥ 0.68      | ✅ **Correct** — item confidently matched |
| 0.55 – 0.68 | 🤔 **Partial** — "Did you mean...?"       |
| < 0.55      | ❌ **Unrecognized** — out of scope        |

---

## 📁 Project Structure

```
IntelegntSystem/
├── docs/
│   ├── reflection.md      # Individual reflection paper (iMuck)
│   ├── test_plan.md       # Edge case test plan (123jgeelo-sudo)
│   └── ui_review.md       # UI/UX review report (criza09)
├── src/
│   ├── __init__.py
│   ├── answer_key.py      # 11 hardware items + aliases + descriptions
│   ├── preprocess.py      # Text normalization & tokenization
│   ├── model.py           # GloVe + similarity Matrix + classify()
│   ├── test_model.py      # 25 edge-case tests
│   └── app.py             # Streamlit chatbot UI
├── models/                # Cached GloVe (gitignored)
├── outputs/logs/          # Runtime logs (gitignored)
├── flowchart.jpg          # System flowchart (dionesiodesu-blip)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/GROUP-5-GWAPITOS-AND-GWAPITAS/IntelegntSystem.git
cd IntelegntSystem

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1     # Windows PowerShell
# source venv/bin/activate       # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the test suite
cd src
python test_model.py
# Expected: 25 passed, 0 failed, 25 total

# 5. Launch the chatbot UI
streamlit run app.py
# Opens at http://localhost:8501
```

> ⚠️ **First run:** GloVe model (~350 MB) will download once and cache to `~/gensim-data/`.

---

## ✅ Evaluation Coverage

| Rubric Category                         | Points  | Status                                                                                    |
| --------------------------------------- | ------- | ----------------------------------------------------------------------------------------- |
| Data preprocessing & input sanitization | 15      | ✅ Lowercase, punctuation removal, whitespace normalization, stopwords, empty-input guard |
| Exact matches                           | 10      | ✅ 100%                                                                                   |
| Abbreviation / acronym mapping          | 10      | ✅ Alias layer handles `cpu`, `psu`, `gpu`, `ram`, `ssd`, `hdd`                           |
| Typo tolerance                          | 10      | ✅ Levenshtein ratio ≥ 0.80                                                               |
| Synonym / paraphrase handling           | 10      | ✅ GloVe cosine similarity                                                                |
| Out-of-scope rejection                  | 5       | ✅ Threshold-calibrated                                                                   |
| Ambiguous / short input handling        | 5       | ✅ Rejected below 0.55                                                                    |
| Empty / whitespace input safety         | 5       | ✅ `is_valid_input()` guard                                                               |
| Threshold calibration                   | 10      | ✅ Empirically determined from the **"Matrix"**                                           |
| Chatbot UI & performance                | 15      | ✅ Streamlit, <1s inference, chat history, reset button                                   |
| **Total**                               | **100** | ✅                                                                                        |

**Test Results:** **25 / 25 passing.**

---

## 👥 Team — Group 5 · GWAPITOS AND GWAPITAS

| Member                | Role                       | Contribution                                           |
| --------------------- | -------------------------- | ------------------------------------------------------ |
| **iMuck**             | Admin / Team Leader        | Chatbot core (model, UI, tests), threshold calibration |
| **dionesiodesu-blip** | Maintain / Project Manager | System flowchart                                       |
| **123jgeelo-sudo**    | Triage / QA                | Edge case test plan                                    |
| **criza09**           | Triage / QA                | UI/UX review report                                    |
| **veamaesangcom**     | Write / Developer          | Answer key alias enrichment                            |

### Deliverables Map

| Deliverable                      | Where to find                 |
| -------------------------------- | ----------------------------- |
| 1. Chatbot UI with Trained Model | `src/app.py` + `src/model.py` |
| 2. Flowchart                     | `flowchart.jpg`               |
| 3. Reflection (softcopy)         | `docs/reflection.md`          |

---

## 🧪 Test Suite

`src/test_model.py` runs **25 automated tests** across all rubric categories:

- **Correct / exact** — 8 cases
- **Acronyms** — 2 cases
- **Typos** — 3 cases
- **Synonyms / paraphrases** — 2 cases
- **Empty / whitespace** — 2 cases
- **Out-of-scope** — 3 cases
- _(+ additional edge cases)_

Run with:

```bash
cd src
python test_model.py
```

---

## ⚠️ Known Limitations

1. **GloVe ignores word order.** A query like `"how is the weather today"` can score moderately against hardware items because some words share latent semantic dimensions. Mitigated by threshold calibration.

2. **Static embeddings don't learn context.** `"cpu"` has the same vector regardless of sentence context.

3. **Scope is limited to 11 items.** The chatbot recognizes hardware components from the answer key, not arbitrary PC questions. This is intentional per the assignment.

**Future work:** Replace GloVe with Sentence Transformers or a Cross-Encoder to handle paraphrase and negation more robustly.

---

## 📄 License

Educational project — CS for Intelligent Systems.

---

## 🔗 Links

- **Repository:** [GROUP-5-GWAPITOS-AND-GWAPITAS/IntelegntSystem](https://github.com/GROUP-5-GWAPITOS-AND-GWAPITAS/IntelegntSystem)
- **GloVe reference:** [nlp.stanford.edu/projects/glove](https://nlp.stanford.edu/projects/glove/)
- **Streamlit docs:** [docs.streamlit.io](https://docs.streamlit.io)
