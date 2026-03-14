# MYPCS.IN — Project Context
## Read this first every session

### WHAT IS THIS PROJECT
mypcs.in — UPPCS exam prep platform. Django backend + PostgreSQL.
Owner: Ankit Chawla (beginner coder, learning as he builds)

### CURRENT STATE (last updated: 15-Mar-2026)
- Status: REST API live + Next.js frontend connected, 10,673 prelims questions
- Database: PostgreSQL (mypcs_db)
- Django project: C:\Users\antri\mypcs280226
- GitHub: https://github.com/ankit-mypcs/backend (backend), https://github.com/ankit-mypcs/frontend (frontend)
- Virtual env: venv (always activate first)
- Settings: mypcs_project/settings.py
- Apps: content (15 models), tracker (2 models: BuildTask, BuildSubTask)
- Content models (15): Subject, Unit, Chapter, Topic, SubTopic, MicroTopic, Exam, ExamSession, Paper, Part, Competency, MainsPYQ, PrelimsPYQ, QuestionAppearance, ExamSource
- Syllabus hierarchy: Subject > Unit > Chapter > Topic > SubTopic > MicroTopic
- ExamSource (lookup table) — normalizes exam names (UPPCS, MPPCS, etc.)
- Paper hierarchy: Paper > Part
- MainsPYQ (subjective mains) — FKs: ExamSession, Paper, Part, Subject, Unit, Chapter, Topic, Competency + fact_code, tag_code
- PrelimsPYQ (MCQ prelims) — FKs: ExamSession(null), Paper(null), Subject(null), Unit, Chapter, Topic + repeat_count
  - option_a-d: max_length=1000, review_status: max_length=25
  - review_status choices: draft, ok, needs_review, parse_error_no_options, reviewed, approved
- QuestionAppearance (bridge table) — FK: PrelimsPYQ (CASCADE) + UniqueConstraint(question, year, exam_source)
- django-import-export 4.4.0 installed — PrelimsPYQ has Import/Export in admin
- Management command: import_prelims_pyq (supports flat + multi-tab Excel formats)
  - Usage: python manage.py import_prelims_pyq file.xlsx --dry-run --batch-id POL --subject Polity
  - Imported: Polity (2,484), History (4,697), Geography (3,492) = 10,673 total
- REST API: djangorestframework 3.16.1 + django-cors-headers 4.9.0 + django-filter 25.2
  - Endpoints: /api/subjects/, /api/chapters/, /api/questions/, /api/stats/
  - Extra actions: check_answer (POST), random_set, by_chapter, chapters/{id}/topics/
  - Files: content/serializers.py, content/api_views.py, content/api_urls.py
  - Pagination: 20 per page, filterable by subject/difficulty/year/exam_source
- Content migrations: 0001 through 0015 applied
- Tracker migrations: 0001 applied
- Tracker data: 30 tasks (S2: 13 done, S3: 17), 4 subtasks
- Frontend: Next.js 16 + Tailwind v4 at C:\Users\antri\mypcs-frontend
  - Stack: TypeScript, App Router, src/ dir, next-pwa
  - Tricolor design tokens: saffron/green/navy + ivory/cream/sandstone + ink family
  - Fonts: Outfit (UI), Lexend (reading), Noto Sans Devanagari (Hindi)
  - Typed API client: src/lib/api.ts (all endpoints typed)
  - T72 DONE: Full homepage with Nav, Footer, hero, stats, problem, features, subjects, pricing, CTA
  - T73+S3-01 DONE: /subjects listing page + /practice interactive question page
  - Components: Nav.tsx, Footer.tsx, page.tsx (homepage with 9 sections)
  - Pages: /subjects (server-side, lists all subjects with PYQ counts), /practice?subject_id=X&subject_name=Y (client-side, UPPCS marking +2/-0.66)
  - Dev: npm run dev on :3000, Django on :8000
  - .env.local: NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api

### CONTENT HIERARCHY (8 levels)
Level 1 — SUBJECT (table) "History" ~11 rows - DONE
Level 2 — UNIT (table) "Ancient History" ~51 rows - DONE
Level 3 — PART (table) 0 rows - DONE (FK to Paper, MainsPYQ has optional FK)
Level 4 — CHAPTER (table) 1 row - T43: Stone Age seeded (FK to Unit)
Level 5 — TOPIC (table) 0 rows - DONE (model created, FK to Chapter, auto-slug save())
Level 6 — SUB-TOPIC (table) 0 rows - DONE (model created, FK to Topic)
Level 7 — SUB-TOPIC text (text field on MainsPYQ — sub_topic_text)
Level 8 — MICRO-TOPIC text (text field on MainsPYQ — micro_topic_text)

### TABLES STATUS
- [x] content_subject — 11 subjects loaded
- [x] content_unit — 51 units loaded
- [x] content_exam — 2 exams (UPPCS Mains + UPPCS Prelims)
- [x] content_exam_session — 13 sessions (7 mains 2018-2024 + 6 prelims 2004-2016)
- [x] content_paper — 10 papers (PRE1, PRE2, HINDI, ESSAY, GS1-GS6)
- [x] content_competency — 37 competencies
- [ ] content_mains_pyq — 1 test question (639 ready to import)
- [x] content_chapter — 1 row (Stone Age under History > Ancient & Medieval India)
- [x] content_topic — 0 rows (cleared, ready for proper import)
- [x] content_subtopic — 0 rows (cleared, ready for proper import)
- [x] content_part — 0 rows (ready for data)
- [x] content_prelims_pyq — 10,673 rows (Polity 2,484 + History 4,697 + Geography 3,492)
- [x] content_question_appearance — 10,127 rows
- [x] content_microtopic — 0 rows (cleared, ready for proper import)
- [x] content_exam_source — 0 rows (cleared, ready for proper import)
- [x] Import prelims PYQs — DONE (10,673 from 3 GC cleaned Excel files)
- [x] tracker_task — 30 tasks seeded (S2: 13 done, S3: 6 done + 11 pending)
- [x] tracker_subtask — 4 subtasks (T28B, T28C, T29B done, T29C)

### NEXT STEPS
1. Populate Chapter, Topic, SubTopic, Part tables with data
2. Import 639 Mains PYQs (MainsPYQ now has topic FK + fact_code + tag_code)
3. Import polity_import_ready.xlsx (560 flat-format Polity questions) if needed
4. Build practice page with question cards + answer checking
5. Add authentication/user model for practice tracking
4. Build practice page with question cards + answer checking
5. Add authentication/user model for practice tracking

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
