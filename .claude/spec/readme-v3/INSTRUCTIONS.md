# Instructions for Updating dbt-conceptual README

## Overview

This document provides instructions for updating the README.md and generating visual assets for the dbt-conceptual repository. The goal is to improve messaging and add visual assets while preserving accurate technical content.

---

## Part 1: Generate Visual Assets

### Source File
Open `readme-assets.html` in a browser. This file contains four render targets.

### Assets to Generate

| Asset | Filename | Dimensions | Description |
|-------|----------|------------|-------------|
| 1 | `assets/logo-banner-dark.png` | 800×140 | Logo + wordmark + tagline on dark background |
| 2 | `assets/logo-banner-light.png` | 800×140 | Logo + wordmark + tagline on light background (backup) |
| 3 | `assets/canvas-example.png` | 900×400 | Canvas showing concepts with relationships, complete/draft/stub states |
| 4 | `assets/ui-screenshot.png` | 1100×600 | Full app UI with canvas, selected concept, and property panel |
| 5 | `assets/coverage-status.png` | 600×350 | Terminal-style coverage report showing domains and status |

### Steps

1. Open `readme-assets.html` in Chrome/Firefox
2. For each asset section:
   - Use browser dev tools or screenshot tool
   - Capture at the specified dimensions (or close to it)
   - Save to `assets/` directory with exact filename
3. Ensure `assets/` directory exists in repo root

---

## Part 2: Update README.md

### Approach: HYBRID

Merge the new structure/messaging from `README-v3.md` with accurate technical content from the current README.

### What to KEEP from new version (README-v3.md / README.md in outputs):

1. **Opening section:**
   - Logo banner image reference
   - Tagline: "The whiteboard sketch that doesn't get erased."
   - Subline: "Conceptual modeling without the ceremony..."

2. **"The Problem" section** with three parts:
   - What Died (the old architect workflow)
   - What Replaced It (engineer autonomy, dbt)
   - What That Created (chaos, drift, lost vocabulary)

3. **"The Solution" section:**
   - "The boxes were never the problem" framing
   - Canvas example image
   - Bullet points about what the tool does

4. **Quote block:**
   ```
   > "Just enough architecture to stay sane."
   > "What Erwin would be if it had to survive a sprint."
   > "Architecture that ships with the code."
   ```

5. **"Who This Is For" section:**
   ```markdown
   ## Who This Is For

   **For architects who write code and engineers who think in systems.**

   - The player-coach who advises without blocking
   - The senior engineer everyone asks "what does this table mean?"
   - The data lead who notices drift before it compounds

   If you've ever drawn boxes on a whiteboard and wished they stayed current — this is for you.
   ```

6. **"What This Isn't" section** (honest scoping)

7. **Improved "Opinionated by Design" section** (softer framing)

8. **UI screenshot** in the Interactive Web UI section

9. **Acknowledgments** (updated version):
   ```markdown
   Built from lived experience. Decades watching the old paradigm fail — beautiful models nobody used. Then watching the new paradigm fail differently — fast delivery, mounting chaos.

   This tool encodes what survives: embedded architectural thinking, lightweight enough to survive contact with reality, opinionated enough to provide value.
   ```

10. **Closing quotes:**
    ```
    > "The minimum viable conceptual model."
    > "Lightweight structure for teams who actually deliver."
    ```

### What to KEEP from current README (preserve accuracy):

1. **Badges** — Use current accurate badges:
   - PyPI version ✓
   - Python ≥3.11 (NOT pyversions showing all)
   - License MIT ✓
   - CI ✓
   - codecov ✓
   - NO downloads badge

2. **CLI Reference** — Use current accurate commands:
   - `init`, `status`, `validate`, `serve`, `sync`, `export`, `diff`
   - Do NOT include `list concepts` or `list concepts --status` (these don't exist)

3. **Pull Request Integration section** — This is critical, keep it:
   ```markdown
   ### 🔀 Pull Request Integration

   See what changed in your conceptual model:

   \`\`\`bash
   # Compare current branch to main
   dbt-conceptual diff --base main

   # Output:
   # Concepts:
   #   + refund (added)
   #   ~ customer (modified: definition changed)
   # 
   # Relationships:
   #   + customer:requests:refund (added)
   \`\`\`
   ```

4. **Documentation section** — Remove or simplify:
   - Do NOT link to readthedocs (doesn't exist)
   - Do NOT link to docs/*.md files (don't exist)
   - Either remove section entirely or replace with:
     ```markdown
     ## Documentation

     See the [examples](examples/) directory for sample projects.
     ```

5. **Layer Model table** — Keep current accurate version

6. **Configuration section** — Keep current accurate version

---

## Part 3: Final Structure

The final README should have this structure:

```
1. Logo banner (image)
2. Tagline + subline
3. Badges (accurate ones only)
4. ---
5. ## The Problem
   - What Died
   - What Replaced It  
   - What That Created
6. ---
7. ## The Solution
   - Canvas example (image)
8. Quote block
9. ---
10. ## Who This Is For
11. ---
12. ## What This Isn't
13. ---
14. ## ⚠️ Opinionated by Design
15. ---
16. ## Installation
17. ---
18. ## Quick Start
19. ---
20. ## How It Works
    - 1. Define Concepts
    - 2. Tag dbt Models
    - 3. Validate & Visualize
21. ---
22. ## Features
    - 📊 Coverage Tracking
    - 🎨 Interactive Web UI (with screenshot)
    - ✅ CI Validation
    - 🔀 Pull Request Integration (IMPORTANT - don't forget!)
    - 🔄 Bi-Directional Sync
    - 📤 Export Formats
23. ---
24. ## Layer Model
25. ---
26. ## Configuration
27. ---
28. ## CLI Reference (accurate commands only)
29. ---
30. ## Documentation (simplified or removed)
31. ---
32. ## Contributing
33. ---
34. ## License
35. ---
36. ## Acknowledgments
37. Closing quotes
38. "Works on my machine..."
```

---

## Part 4: Verification Checklist

Before committing, verify:

- [ ] `assets/logo-banner-dark.png` exists and displays correctly
- [ ] `assets/canvas-example.png` exists and displays correctly
- [ ] `assets/ui-screenshot.png` exists and displays correctly
- [ ] `assets/coverage-status.png` exists and displays correctly
- [ ] No `[![Downloads]` badge
- [ ] Python badge shows `≥3.11` not all versions
- [ ] CLI Reference has accurate commands (no `list` commands)
- [ ] Pull Request Integration / diff section is present
- [ ] No links to non-existent documentation (readthedocs, docs/*.md)
- [ ] All image references resolve correctly

---

## Summary

**Goal:** Better messaging + visual assets + accurate technical content

**Key principle:** When in doubt, trust the CURRENT README for technical accuracy, and the NEW README for structure/messaging.

The new narrative ("What Died / What Replaced It / What That Created") is the main improvement. The technical details (CLI commands, badges, features) should come from what actually exists in the codebase.
