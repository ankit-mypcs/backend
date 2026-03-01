# MYPCS.IN — Project Context
## Read this first every session

### WHAT IS THIS PROJECT
mypcs.in — UPPCS exam prep platform. Django backend + PostgreSQL.
Owner: Ankit Chawla (beginner coder, learning as he builds)

### CURRENT STATE (last updated: 01-Mar-2026)
- Status: Building content hierarchy tables
- Database: PostgreSQL (mypcs_db)
- Django project: C:\Users\antri\mypcs280226
- Virtual env: venv (always activate first)
- Settings: mypcs_project/settings.py

### CONTENT HIERARCHY (8 levels)
Level 1 — SUBJECT (table) "History" ~11 rows - DONE
Level 2 — UNIT (table) "Ancient History" ~51 rows - DONE
Level 3 — PART (table) future
Level 4 — CHAPTER (table) future
Level 5 — SECTION (table) future
Level 6 — TOPIC (table) future
Level 7 — SUB-TOPIC (text field on question)
Level 8 — MICRO-TOPIC (text field on question)

### TABLES STATUS
- [x] content_subject — 11 subjects loaded
- [x] content_unit — 51 units loaded
- [ ] content_part — not started
- [ ] content_chapter — not started
- [ ] content_section — not started
- [ ] content_topic — not started
- [ ] content_mains_pyq — 639 questions ready to import
- [ ] content_question — 559 prelims ready to import

### RULES
- Always activate venv before running Python
- Always use --dry-run before import scripts
- Always show migration files before applying
- Explain every change — Ankit is learning
- Never implement Phase 2/3/4 features unless asked

### STARTUP CHECKLIST (run every new session)
1. python manage.py check
2. python manage.py showmigrations
3. Report any issues before proceeding
