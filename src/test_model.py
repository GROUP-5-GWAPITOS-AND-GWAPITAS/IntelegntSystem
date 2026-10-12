# src/test_model.py
from model import classify

TESTS = [
    # Exact / acronym (should be correct via alias)
    ("cpu", "correct"),
    ("ram", "correct"),
    ("gpu", "correct"),
    ("psu", "correct"),
    ("motherboard", "correct"),
    ("keyboard", "correct"),
    ("mouse", "correct"),
    ("monitor", "correct"),
    ("ssd", "correct"),
    ("hdd", "correct"),
    # Full names
    ("random access memory", "correct"),
    ("central processing unit", "correct"),
    ("graphics processing unit", "correct"),
    ("power supply unit", "correct"),
    # Typos (Levenshtein fuzzy)
    ("keybord", "correct"),
    ("motherbord", "correct"),
    ("procesor", "correct"),
    ("moniter", "correct"),
    # Synonyms (GloVe)
    ("brain of the computer", "correct"),
    ("screen", "correct"),
    # Edge cases
    ("", "empty"),
    ("   ", "empty"),
    ("???", "unrecognized"),
    ("how do i cook adobo", "unrecognized"),
    ("what is the weather today", "unrecognized"),
]

passed = 0
failed = 0
for query, expected in TESTS:
    result = classify(query)
    ok = result["status"] == expected
    mark = "✅" if ok else "❌"
    print(f"{mark} Q={query!r:45s} status={result['status']:12s} "
          f"best={result['matched'] or '-':25s} score={result['score']:.3f}")
    if ok:
        passed += 1
    else:
        failed += 1

print(f"\n{passed} passed, {failed} failed, {passed + failed} total")