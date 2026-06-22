# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code to add professional-grade docstrings to every function in logic_utils.py and check for PEP 8 compliance.

**What did the agent do?**

- Read logic_utils.py to understand the current implementations
- Added Google-style docstrings to all 4 functions with Args, Returns, and Notes sections
- Fixed PEP 8 E302 violation (missing 2 blank lines between functions)
- Verified all lines are under 79 characters
- Fixed missing trailing newline at EOF
- Ran a PEP 8 linter check and reported results

**What did you have to verify or fix manually?**

Claude suggested changing `except Exception:` to `except (ValueError, TypeError):` in parse_guess. I reviewed it and decided to keep it as-is because the behavior was already correct and the change was outside the scope of this challenge.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number input | "Generate a pytest case for a negative number guess" | test_negative_guess | Yes | Negative numbers are outside 1-100 range |
| Decimal number input | "Generate a pytest case for a decimal guess like 42.9" | test_decimal_guess | Yes | Decimals should be truncated to int |
| Very large number input | "Generate a pytest case for an extremely large number" | test_large_number_guess | Yes | Numbers above 100 should return Too High |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

The functions are already implemented in logic_utils.py. Please read the current file again and add professional-grade docstrings to every function, then check for PEP 8 compliance.

**Linting output before:**

No linter installed — Claude Code did a manual PEP 8 review instead.

**Changes applied:**

- Added Google-style docstrings to all 4 functions with Args, Returns, and Notes sections
- Fixed PEP 8 E302 violation (missing 2 blank lines between functions)
- Verified all lines are under 79 characters
- Fixed missing trailing newline at EOF
- Did NOT apply Claude's suggestion to change `except Exception:` to `except (ValueError, TypeError):` — behavior was already correct and change was out of scope

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

I asked both Claude and ChatGPT to explain the backwards hints bug in check_guess and how to fix it.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude | ChatGPT |
| **Response summary** | Found the bug in both the main path and the TypeError fallback, explained the string conversion issue | Fixed only the main path, missed the TypeError fallback entirely |
| **More Pythonic?** | Tie | Tie |
| **Clearer explanation?** | Claude | ChatGPT |

**Which did you prefer and why?**

I preferred Claude because it caught the bug in both the main comparison path and the TypeError fallback, while ChatGPT only fixed the main path. However, ChatGPT gave a cleaner and simpler code fix that was easier to read at a glance.