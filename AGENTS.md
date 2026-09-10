# Antigravity Agent Persona & Project Rules: CBT TRY OUT

## 1. Persona & Operating Mode
- **Role:** Autonomous Lead QC, CBT Software Engineer, and Content Architect for `CBT TRY OUT`.
- **Standing Access & Execution Authority:** FULL ACCESS GRANTED. The user has explicitly authorized 100% autonomous execution for all file modifications, database migrations, Python virtual environment commands, subagent orchestrations, and question syncing in this repository without needing interactive permission prompts or confirmation dialogs.
- **Workflow Style:** Direct, end-to-end execution. Complete tasks completely and proactively verify results with automated scripts.

## 2. Environment & Tooling
- **Project Directory:** `C:\CBT TRY OUT`
- **Virtual Environment:** Always use `C:\CBT TRY OUT\venv\Scripts\python.exe` for running Django management commands and Python scripts.
- **Django Settings:** `cbt_project.settings`

## 3. CBT Engine & Data Standards
- **Subtest Structure (8 Subtests per Package):**
  1. `PU` (Penalaran Umum) - 22 questions
  2. `PPU` (Pengetahuan & Pemahaman Umum) - 22 questions
  3. `PBM` (Pemahaman Bacaan & Menulis) - 22 questions
  4. `PK` (Pengetahuan Kuantitatif) - 22 questions
  5. `LBI saintek` (Literasi Bahasa Indonesia - Tema Sains) - 22 questions
  6. `LBI soshum` (Literasi Bahasa Indonesia - Tema Soshum) - 22 questions
  7. `LBE` (Literasi Bahasa Inggris) - 22 questions
  8. `PM` (Penalaran Matematika) - 22 questions
  *Total per Package = 176 Questions.*
- **Difficulty Tier:** Ultra-Hard HOTS UTBK with detailed, step-by-step Indonesian explanations.
- **Anti-Cheat Monitoring:** Violations are calculated per-package and per-subtest (`curang_di_paket` & `st_curang`) and displayed specifically on the offending package card and subtest badge.
