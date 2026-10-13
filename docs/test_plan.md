# Edge Case Test Plan — Hardware QA Chatbot

Test plan covering all rubric categories: exact match,
acronym mapping, typo tolerance, synonym handling, empty
input safety, and out-of-scope rejection.

## Test Cases

| # | Input | Expected | Actual | Pass/Fail |
|---|-------|----------|--------|-----------|
| 1 | cpu | correct → Central Processing Unit | matches screenshot | Pass |
| 2 | CPU | correct → Central Processing Unit | matches screenshot | Pass |
| 3 | ram | correct → Random Access Memory | matches screenshot | Pass |
| 4 | psu | correct → Power Supply Unit | matches screenshot | Pass |
| 5 | gpu | correct → Graphics Processing Unit | matches screenshot | Pass |
| 6 | ssd | correct → Storage Drive | matches screenshot | Pass |
| 7 | hdd | correct → Storage Drive | matches screenshot | Pass |
| 8 | monitor | correct → Monitor | matches screenshot | Pass |
| 9 | keyboard | correct → Keyboard | matches screenshot | Pass |
| 10 | mouse | correct → Mouse | matches screenshot | Pass |
| 11 | keybord | correct → Keyboard (typo tolerance) | matches screenshot | Pass |
| 12 | motherbord | correct → Motherboard (typo tolerance) | matches screenshot | Pass |
| 13 | procesor | correct → Central Processing Unit (typo) | matches screenshot | Pass |
| 14 | brain of the computer | correct → CPU (synonym) | matches screenshot | Pass |
| 15 | screen | correct → Monitor (synonym) | matches screenshot | Pass |
| 16 | (empty string) | empty status → prompt user | matches screenshot | Pass |
| 17 | (spaces only) | empty status → prompt user | matches screenshot | Pass |
| 18 | ??? | unrecognized → rejection message | matches screenshot | Pass |
| 19 | how to cook adobo | unrecognized → rejection message | matches screenshot | Pass |
| 20 | what is the weather today | unrecognized → rejection message | matches screenshot | Pass |

## Summary

- Total test cases: 20
- Passed: 20
- Failed: 0
- Pass rate: 100%

## Notes

- Evidence for "Actual" column: see screenshots in PR #1
- All tests verified via src/test_model.py (25 cases) and the Streamlit UI at http://localhost:8501
- Algorithm: GloVe 100d + cosine similarity + Levenshtein fuzzy fallback + threshold-based decision logic
