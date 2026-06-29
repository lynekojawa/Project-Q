# Project Q — Local LLM Study Engine

## Why I Built This

I was trying to study algorithms for technical assessments and wanted to move faster than traditional reading allows. I tried feeding 100+ pages of Jeff Erickson's *Algorithms* to GPT — the output was generic, truncated, and occasionally wrong. Free-tier token limits, context overflow, and hallucination made it unreliable for dense technical material.

So I built my own. A local pipeline that runs on my machine, costs nothing per query, works offline, and is designed specifically for technical textbook ingestion. The goal was simple: feed it a book, get structured summaries, then answer questions until the material sticks.

It turned out to be the hardest thing I've built so far.

---

## What It Does

Project Q is a local LLM-powered study engine. It ingests technical textbooks, generates structured summaries chapter by chapter, and serves spaced-repetition quiz sessions to reinforce learning.

Non-technical version: you give it a textbook, it reads it, summarizes each section, and quizzes you on it — adapting the review schedule based on what you're getting wrong.

Technical version: a multi-phase pipeline combining PDF ingestion and sanitization, a relational SQLite ledger with SM-2 spaced repetition scheduling, Pydantic-validated LLM generation via Ollama, and a Streamlit skill tree UI for session management.

---

## Architecture & Phases

### Phase 1 — Ingestion, AST Cleaning & DAG Editor
PDF ingestion via `marker` pipeline producing raw markdown. A custom regex and markdown linter sanitizes LaTeX artifacts, broken headers, and pseudocode indentation issues. A programmatic TOC parser converts the chapter hierarchy into `concept_map.json`. A human-in-the-loop DAG editor in Streamlit allows manual correction of the parsed structure before seeding the database.

**Key decision:** After several days of fighting PDF parsing edge cases, I made an architectural call to hand-write `concept_map.json` for the current book and build LLM-assisted TOC verification as a later feature. Generalization was the goal but not worth blocking the pipeline.

### Phase 2 — Relational SQLite Ledger & SM-2 Spine
Three-table SQLite schema: `concept_nodes` (mastery tracking per section), `dependency_edges` (prerequisite DAG), `cognitive_error_logs` (per-question failure logging for Socratic review). SM-2 spaced repetition implemented from scratch — ease factor mutation, interval calculation, quadratic EF decay on failure.

### Phase 3 — Pydantic Validation & Ollama Generation Engine
Ollama local inference (Llama 3.1 8B / Mistral 7B) with structured output enforced via Pydantic schema contracts. `ConceptQuizPackage` defines MCQ and code-tracing question formats. Temperature set to 0 to suppress hallucination. Socratic mentor fires when session score drops below mastery threshold θ = 0.80 — presents a leading question instead of the answer.

### Phase 4 — Streamlit Skill Tree UI & System Orchestrator
Visual skill tree with node locking based on prerequisite mastery. Split assessment console: summary and LaTeX complexity proofs on the left, quiz interface on the right. Single-command bootloader verifies Ollama connectivity, validates schema, and launches the app.

### Phase 5 — PDF Ingestion & Auto-Summary *(current, paused)*
LLM-generated structured summaries per chapter: core thesis, time complexity, space complexity, critical invariants, clean markdown summary. Pipeline reached 91 of 114 study nodes before hitting the hallucination boundary described below.

### Phase 6 — Dynamic MCQ & Short-Answer Generation *(planned)*
Reads Phase 5 summaries to generate structured quiz packages. TOC-to-JSON curriculum engine to generalize the pipeline to any book.

---

## Technical Stack

| Layer | Tools |
|---|---|
| Local Inference | Ollama (Llama 3.1 8B / Mistral 7B Instruct) |
| Data Validation | Pydantic |
| Database | SQLite via Python `sqlite3` |
| Ingestion | `marker`, custom regex sanitizer |
| UI | Streamlit, `streamlit-agraph` |
| Language | Python |
| Spaced Repetition | SuperMemo-2 (SM-2), implemented from scratch |

---

## What I Learned

**PDF parsing is genuinely hard.** The book I used has 14–16 pre-pages before page 1 — so printed page numbers and PDF page indices are offset throughout. My agents kept suggesting "just fix the offset to 14" and I kept saying no: I'm not building a tool that only works on one book. Generalization requires solving the problem properly, not patching it for one case.

**LLMs hallucinate in specific, diagnosable patterns** — and the patterns differ by context.During development I observed two distinct failure modes from different sources.From my AI coding agents (Gemini/Claude) during architecture and code review sessions:

- They avoid admitting uncertainty by producing something plausible-sounding instead
- They fix broken code by changing variable names while keeping the same flawed structure
- They generalize aggressively from two or three examples — "instant answer" behavior that looks correct and isn't
**From the local LLM (Llama) during summary generation**:
- Section 0.5 produced a summary of a traditional British drinking song embedded in Erickson's text. The model grabbed the most salient content in the chunk, which happened to be a folk poem, not the algorithm being described. Core thesis returned: "A health to the barley-mow, my brave boys."

Section 0.5 produced a summary of a traditional British drinking song embedded in Erickson's text. The model grabbed the most salient content in the chunk, which happened to be a folk poem, not the algorithm being described. Core thesis returned: "A health to the barley-mow, my brave boys."
**Large multi-folder projects require explicit tracking infrastructure.** Previous projects had one engine, one UI, one database. Project Q has six folders and fifteen files. I built a dedicated function-tracking file mid-project to stay oriented — without it I was losing hours to context switching between files. That habit stays for every project going forward.

**Agent drift is a real engineering problem.** I described Project Q as "like Duolingo" during planning. My agents over-weighted the gamification layer and under-weighted the summary pipeline. I had to re-direct mid-project after noticing the plan had drifted from the original goal. The fix: be precise about what the core feature is, not what it resembles.

**The wrap decision.** I paused the project at Phase 5 with 91/114 summaries generated. The hallucination rate on connected UI output was not acceptable for a study tool. The correct next step is better chunking strategy and possibly a larger local model — both require hardware or architectural work I'm not ready to do yet. Pausing with documentation is better than shipping something unreliable.

Euclid said there is no royal road to geometry. I built this project trying to make one. There isn't. But I read the first chapter properly, learned how local LLM inference pipelines actually work, and built the most architecturally complex project I've done so far.

---

## Interesting Failure Artifacts

**Section 0.5 — "Describe Algorithms":** The chapter contains a traditional British folk song as a pedagogical example. The model summarized the song instead of the algorithmic concept. Core thesis returned: *"A health to the barley-mow, my brave boys."*

**Section 1.3 — Tower of Hanoi:** Passed correctly.

**Section 3.6 — Longest Increasing Subsequence:** Model confused chapter boundaries and summarized the wrong section.

**Page 118 raw parse output:**
```
'3.1. m¯atr¯avr.tta\nf2 f1\nf1 f0f1 f0\nf3\n...'
```
Sanskrit transliteration artifacts from the book's typesetting caused complete parse failure on this page. The model had nothing useful to work with.

These artifacts are documented in `/data/concept_map.json` and the summary output table below.

---

## Summary Output Table

| Page | Chapter | Title | Summary Generated | Hallucination Flag |
|---|---|---|---|---|
| 20 | 0.2 | Multiplication | Yes | No |
| 25 | 0.3 | Congressional Apportionment | Yes | No |
| 27 | 0.4 | A Bad Example | Yes | Potentially |
| 28 | 0.5 | Describe Algorithms | Yes | **Yes** — folk song |
| 31 | 0.6 | Analyzing Algorithms | Yes | Yes |
| 38 | 1.1 | Reductions | Yes | Maybe |
| 39 | 1.2 | Simplify and Delegate | Yes | Maybe |
| 41 | 1.3 | Tower of Hanoi | Yes | Yes |
| 43 | 1.4 | Mergesort | Yes | Potentially |

*Full output table with all 91 generated summaries available in `/data/`.*

---

## Project Structure

```
Project-Q/
├── data/
│   └── concept_map.json          # Knowledge hierarchy (Ground Truth)
├── db/
│   ├── db_setup.py               # Schema builder and reset utility
│   └── ledger_ops.py             # Atomic DB transaction operators
├── engine/
│   ├── evaluation.py             # Spaced repetition orchestration
│   ├── models.py                 # Pydantic data contracts
│   ├── sm2_engine.py             # SuperMemo-2 mathematical logic
│   └── socratic_mentor.py        # LLM-based pedagogical hint engine
├── ingestion/
│   ├── sanitizer.py              # Text cleaning and artifact removal
│   └── parser.py                 # TOC → JSON programmatic parser
├── scripts/
│   └── debug_ingestion.py        # Structural integrity audit tool
└── ui/
    └── skill_tree.py             # Streamlit visualization UI
```

---

## Current Status

**Paused at Phase 5.** Core pipeline functional. 91/114 study nodes summarized. Hallucination rate on UI-connected output exceeded acceptable threshold for a study tool.

Known issues:
- Chapter ordering in UI is alphabetical not sequential — requires manual cross-reference with `concept_map.json` to follow book order
- Summary generation time: 45 seconds to several minutes per section on local hardware
- PDF page offset problem unsolved for generalized book support

---

## Next Steps

This project resumes when one of the following is true:
- Access to better local hardware (larger model, faster inference)
- A better chunking strategy that preserves chapter boundary context across pages
- Human-in-the-loop TOC verification implemented before summary generation

The architecture is sound. The PDF parsing and hallucination problems are engineering problems, not design problems. They have solutions.

---

## Credits

| Role | Contributor | Responsibility |
|---|---|---|
| **Lead Architect** | lynekojawa (Human) | Core idea, architectural decisions, audit, mathematics |
| **Logic Orchestrator** | PODO (Gemini) | System design, logic review, code review |
| **Master Planner** | Orion (Gemini) | Strategic planning, phase roadmaps |
| **Code Partner** | Dante (Claude) | Implementation review, debugging, Git strategy |