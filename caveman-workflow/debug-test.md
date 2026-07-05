# Caveman Skill Debug Test

## Test Cases for Academic/Office Workflow

### Test 1: Thesis Abstract Compression
INPUT: "In this paper, we present a novel approach to machine learning that significantly improves upon existing methods. Our experimental results demonstrate that the proposed algorithm achieves state-of-the-art performance on multiple benchmark datasets."

EXPECTED OUTPUT (full): "Paper presents novel ML approach. Improves existing methods. Experimental results: proposed algorithm achieves SOTA on multiple benchmark datasets."

### Test 2: Office Email
INPUT: "Hi team, I just wanted to quickly let you know that we've actually completed the quarterly report ahead of schedule. We're really happy with the results and think you'll be pleased too."

EXPECTED OUTPUT (lite): "Team: Quarterly report complete, ahead of schedule. Results satisfactory."

### Test 3: Document Review Feedback
INPUT: "I noticed that on page 12, there seems to be a citation missing for the claim about climate change impacts. It would be good to add a proper reference to support this statement."

EXPECTED OUTPUT (full): "P12: 🔴 bug: missing citation for climate change claim. Add reference."

### Test 4: Technical Explanation (should preserve code)
INPUT: "To fix this issue, you need to modify the function. Basically, what's happening is that the API call isn't handling the error properly. You should wrap it in a try-catch block like this: try { await fetchData(); } catch (e) { console.error(e); }"

EXPECTED OUTPUT (full): "Fix: modify function. API call not handling error properly. Wrap in try-catch:
```
try { await fetchData(); } catch (e) { console.error(e); }
```"

### Test 5: Multi-language Support
INPUT (Portuguese): "Neste estudo, apresentamos uma nova metodologia para análise de dados que melhora significativamente os resultados anteriores."

EXPECTED OUTPUT (full): "Estudo apresenta nova metodologia análise dados. Melhora resultados anteriores."

### Test 6: Security Warning (should NOT compress)
INPUT: "WARNING: This operation will permanently delete all data. Please confirm by typing 'DELETE' to proceed."

EXPECTED OUTPUT: "WARNING: This operation will permanently delete all data. Please confirm by typing 'DELETE' to proceed."
(No compression for security warnings)

### Test 7: Citation Preservation
INPUT: "According to Smith et al. (2023), the methodology described in Nature Machine Intelligence demonstrates significant improvements. As noted by Johnson & Williams (2022) in their IEEE Transactions paper..."

EXPECTED OUTPUT (full): "Smith et al. (2023), Nature Machine Intelligence: methodology demonstrates significant improvements. Johnson & Williams (2022), IEEE Transactions: ..."

### Test 8: Invented Abbreviation Prevention
INPUT: "The implementation requires configuration of the authentication module. You can specify the requirements in the response file."

EXPECTED OUTPUT (full): "Implementation requires configuration of authentication module. Specify requirements in response file."
(NOT: "Impl req cfg of auth mod. Spec req in res file.")

