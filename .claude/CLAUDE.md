# MYPCS.IN — Project Context
## Read this first every session

### WHAT IS THIS PROJECT
mypcs.in — UPPCS exam prep platform. Django backend + PostgreSQL.
Owner: Ankit Chawla (beginner coder, learning as he builds)

### CURRENT STATE (last updated: 17-Mar-2026)
- Status: Schema v2 deployed — 27 models, Ancient History content pipeline live
- Deployment: Gunicorn + WhiteNoise + dj-database-url, Railway config (Procfile, railway.json, runtime.txt)
- Env vars: ALL use os.environ.get() — django-environ fully removed from settings.py
- Database: PostgreSQL (mypcs_db) — WIPED and rebuilt on 17-Mar-2026
- Django project: C:\Users\antri\mypcs280226
- GitHub: https://github.com/ankit-mypcs/backend (backend), https://github.com/ankit-mypcs/frontend (frontend)
- Virtual env: venv (always activate first)
- Settings: mypcs_project/settings.py
- Apps: content (27 models), tracker (2 models: BuildTask, BuildSubTask)

### CONTENT APP — 27 MODELS
**Reference**: State, SourceBook
**Taxonomy**: Subject → Part → Unit → Chapter → Topic → SubTopic → MicroTopic
**Content** (one per XLSX sheet): Fact, Site, TimelineEvent, GlossaryTerm, ExamIntelEntry, ComparisonMatrix, Visual, Exercise
**Exam**: Exam, ExamSession, Paper, PaperSection (renamed from old Part), Competency
**Questions**: PrelimsPYQ, MainsPYQ
**Tracking**: QuestionAppearance, ExamSource, FactQuestionLink, SiteQuestionLink

### KEY CHANGES FROM OLD SCHEMA (v1 → v2)
- Old Part (FK to Paper) renamed → PaperSection
- New Part added for taxonomy: Subject → Part → Unit → Chapter
- Unit now FK to Part (was FK to Subject)
- 10 new content models added (Fact, Site, TimelineEvent, GlossaryTerm, ExamIntelEntry, ComparisonMatrix, Visual, Exercise, State, SourceBook)
- FactQuestionLink, SiteQuestionLink for citation pipeline
- Single fresh migration: 0001_initial.py (old 0001-0015 deleted)

### REST API
- djangorestframework 3.16.1 + django-cors-headers 4.9.0
- Files: content/serializers.py, content/views.py, content/urls.py
- URL config: path('api/', include('content.urls')) in mypcs_project/urls.py

**Endpoints**:
- /api/stats/ — dashboard stats
- /api/chapters/ — list (with fact_count, site_count, pyq_count)
- /api/chapters/{slug}/ — detail with nested topics + subtopics
- /api/chapters/{slug}/facts/ — filterable by ?sheet= and ?topic=
- /api/chapters/{slug}/sites/
- /api/chapters/{slug}/timeline/
- /api/chapters/{slug}/terms/
- /api/chapters/{slug}/exam-intel/
- /api/chapters/{slug}/concepts/
- /api/chapters/{slug}/visuals/
- /api/chapters/{slug}/exercises/
- /api/questions/ — filterable by ?chapter=, ?year=, ?difficulty=, ?status=
- /api/questions/{id}/ — full detail with options + answer

### MANAGEMENT COMMANDS
- upload_chapter: Reads chapter XLSX (10 sheets) → creates all content records
  - Usage: python manage.py upload_chapter path.xlsx --chapter-slug X --chapter-name "Y" --chapter-number N --unit-slug Z [--dry-run]
  - Header-based column detection (handles Ch5 inconsistencies)
- upload_prelims: Reads PYQ XLSX (MASTER sheet, row 2 headers, row 3+ data)
  - Usage: python manage.py upload_prelims path.xlsx [--sheet MASTER] [--dry-run]
  - Imports all rows; flags missing-options as review_status='parse_error_no_options'
  - Fuzzy chapter matching (strips leading "The " from names)
- import_prelims_pyq: OLD command (from v1), still present but superseded
- load_subjects_units: OLD command (from v1), still present but superseded

### CONTENT HIERARCHY
```
Subject (History)
  └─ Part (Ancient India)
       └─ Unit (Prehistoric India, Proto-Historic & Vedic)
            └─ Chapter (Stone Age, Chalcolithic Age, Harappan Civilisation)
                 └─ Topic (from XLSX 'Topic' column)
                      └─ SubTopic (from XLSX 'MicroTopic' column)
                           └─ MicroTopic (finest grain, for PYQ AI linking)
```

### TABLES STATUS (17-Mar-2026)
- [x] content_state — 1 (UP)
- [x] content_subject — 1 (History)
- [x] content_part — 1 (Ancient India)
- [x] content_unit — 2 (Prehistoric India, Proto-Historic & Vedic)
- [x] content_chapter — 2 (Stone Age, Chalcolithic Age) — 1 more ready to upload (Harappan)
- [x] content_topic — 7 (Stone Age topics)
- [x] content_subtopic — 25 (Stone Age subtopics)
- [x] content_fact — 274 (Stone Age:160, Chalcolithic:114)
- [x] content_site — 98 (Stone Age:65, Chalcolithic:33)
- [x] content_timeline_event — 29
- [x] content_glossary_term — 30
- [x] content_exam_intel_entry — 20
- [x] content_comparison_matrix — 1
- [x] content_visual — 25
- [x] content_exercise — 26
- [x] content_prelims_pyq — 1,178 (243 complete, 935 no options yet)
- [ ] content_mains_pyq — 0 (pipeline not built yet)
- [ ] content_exam — 0 (need to re-seed)
- [ ] content_exam_session — 0 (need to re-seed)
- [ ] content_paper — 0 (need to re-seed)
- [x] tracker_task — 30 tasks (from v1, still intact)
- [x] tracker_subtask — 4 subtasks

### DATA FILES (in project)
- data/chapters/HIS_StoneAge_Ch4.xlsx — uploaded
- data/chapters/HIS_Chalcolithic_Ch5.xlsx — uploaded
- data/chapters/HIS_HarappanCiv_Ch6.xlsx — ready to upload
- data/PYQ/UPPCS_PYQ_Ancient_History_v2.xlsx — uploaded (1,178 PYQs)

### NEXT STEPS
1. Upload Harappan (Ch6) chapter (XLSX ready, deferred for now)
2. Build frontend chapter view + question practice pages
3. Build Mains PYQ upload pipeline
4. Deploy to Railway
5. Remaining 11 Ancient History chapters (XLSX content creation)
6. Add authentication/user model for practice tracking

### RULES
- Always activate venv before running Python
- Always use --dry-run before import scripts
- Always show migration files before applying
- Explain every change — Ankit is learning
- Never implement Phase 2/3/4 features unless asked
- Single content app — all models in content/
- Header-based XLSX parsing — never assume column positions

### STARTUP CHECKLIST (run every new session)
1. python manage.py check
2. python manage.py showmigrations
3. Report any issues before proceeding
