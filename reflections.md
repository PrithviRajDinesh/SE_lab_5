1. Which issues were the easiest to fix, and which were the hardest? Why?
Ans: Easiest: The style fixes were easiest, like removing the unused import logging or renaming functions to snake_case. These were simple, mechanical changes.
Hardest: Removing the global stock_data variable was the hardest. This was a complex fix that required changing the code for almost every function.
2. Did the static analysis tools report any false positives?
Ans: No, there were no false positives. Every issue was a real problem. The eval() warning was a major security risk, the logs=[] warning was a subtle bug, and the bare except: was hiding all errors.
3. How would you integrate static analysis tools into your development workflow?
Ans: In my editor (Local): Use a plugin to see errors as I type.
Before Committing (Local): Use Git "pre-commit hooks" to automatically run tools and block bad commits.
In the Pipeline (CI): Use GitHub Actions to run checks on every pull request, preventing merges if the tools fail.
4. What tangible improvements did you observe after applying the fixes?
Ans: Readability: The code is much easier to read with docstrings and proper snake_case names.
Robustness: The app is more stable. Fixing the logs=[] bug and the bare except: prevents crashes and unexpected behavior.
Security & Maintenance: The code is safer. Removing eval() fixed a major security hole, and removing the global variable makes the code more predictable.
