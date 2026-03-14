# MYPCS.IN — Progress Log

## Session 1 — 01-Mar-2026

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T1 | Create Django project + content app | Done |
| T2 | Add content to INSTALLED_APPS | Done |
| T3 | Design 8-level hierarchy (Subject>Unit>Part>Chapter>Section>Topic>SubTopic>MicroTopic) | Done |
| T4 | Create Subject + Unit models | Done |
| T5 | Run makemigrations + migrate | Done |
| T6 | Create project documentation | Done |
| T7 | Clean rebuild with correct naming | Done |
| T8 | Create admin.py with SubjectAdmin + UnitInline | Done |
| T9 | Create load_subjects_units.py | Done |
| T10 | Load 11 subjects + 51 units | Done |

---

## Session 2 — 01-Mar-2026 (continued)

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T11 | Created superuser (ankit / ankit@mypcs.in) | Done |
| T12 | Added `code` field to Subject model (3-step custom migration) | Done |
| T13 | Created docs/MULTI_TENANT_NOTES.md (8 future-proofing rules) | Done |
| T14 | Added 5 new models: Exam, ExamSession, Paper, Competency, MainsPYQ | Done |
| T15 | Evolved MainsPYQ: renamed fields, added uid/q_no/state/tracking fields | Done |
| T16 | Created 1 test MainsPYQ with all FK relationships verified | Done |
| T17 | Populated 7 ExamSessions (2018-2024) with full dates/cutoffs/stats | Done |
| T18 | Populated 6 GS Papers (GS1-GS6) | Done |
| T19 | Populated 37 Competencies | Done |
| T20 | Enriched Paper model with 11 new fields (exam_stage, total_marks, etc.) | Done |
| T21 | Added 4 new papers (PRE1, PRE2, HINDI, ESSAY) — 10 total | Done |
| T22 | Updated admin.py for enriched Paper model | Done |
| T23 | Updated CLAUDE.md and PROGRESS_LOG.md | Done |

### Migrations Applied
| # | Migration | Description |
|---|---|---|
| 0002 | subject_code | Custom 3-step: add code field, populate via RunPython, add unique |
| 0003 | competency_exam_paper_examsession_mainspyq | 5 new model tables |
| 0004 | mainspyq_evolve | Custom: rename 5 fields, add 7 new fields, update ordering |
| 0005 | alter_mainspyq_legacy_code | Auto: help_text update |
| 0006 | paper_enrich | Add 11 enrichment fields to Paper |

### Database Counts
| Table | Count |
|---|---|
| content_subject | 11 |
| content_unit | 51 |
| content_exam | 1 |
| content_exam_session | 7 |
| content_paper | 10 |
| content_competency | 37 |
| content_mains_pyq | 1 (test) |

---

## Session 3 Audit — 01-Mar-2026

### Full Project Audit
| Check | Result |
|---|---|
| Django apps | 1 custom (content) + 4 built-in (admin, auth, contenttypes, sessions) |
| Content models | 7: Subject, Unit, Exam, ExamSession, Paper, Competency, MainsPYQ |
| Migrations | 6 content + 18 built-in — ALL applied, none pending |
| Superuser | ankit (ankit@mypcs.in) |
| models.py | 358 lines, 7 models, 4 choice sets, 2 @property methods |

### Record Counts (verified)
| Table | Count | Notes |
|---|---|---|
| content_subject | 11 | All with code + icon |
| content_unit | 51 | Linked to subjects |
| content_exam | 1 | UPPCS Mains |
| content_exam_session | 7 | 2018-2024, full dates/cutoffs/stats |
| content_paper | 10 | PRE1, PRE2, HINDI, ESSAY, GS1-GS6 (enriched) |
| content_competency | 37 | With Bloom's levels |
| content_mains_pyq | 1 | Test question |
| auth_user | 1 | Superuser: ankit |

### Model Field Summary
| Model | Fields | FKs | JSONFields | Properties |
|---|---|---|---|---|
| Subject | 10 | 0 | 0 | 0 |
| Unit | 10 | 1 (Subject) | 0 | 0 |
| Exam | 7 | 0 | 0 | 0 |
| ExamSession | 30+ | 1 (Exam) | 0 | 0 |
| Paper | 19 | 0 | 3 (syllabus_topics, mains_overlap, paper_data) | 0 |
| Competency | 7 | 0 | 0 | 0 |
| MainsPYQ | 25+ | 4 (ExamSession, Paper, Subject, Unit) + 1 (Competency) | 0 | 2 (full_code, short_code) |

### Tasks Completed (Session 3)
| # | Task | Status |
|---|---|---|
| T24 | Full project audit (models, migrations, record counts) | Done |
| T25 | Created Chapter model (12 fields, FK to Unit, UniqueConstraint) | Done |
| T26 | Added optional FK from MainsPYQ to Chapter | Done |
| T27 | Updated admin.py: ChapterAdmin, ChapterInline, chapter in raw_id_fields | Done |
| T28 | Migration 0007_chapter_model applied | Done |
| T29 | Updated CLAUDE.md and PROGRESS_LOG.md | Done |
| T30 | Created Topic model (10 fields, FK to Chapter, UniqueConstraint) | Done |
| T31 | Created SubTopic model (7 fields, FK to Topic, UniqueConstraint) | Done |
| T32 | Updated admin.py: TopicAdmin, SubTopicAdmin, TopicInline, SubTopicInline | Done |
| T33 | Migration 0008_topic_subtopic applied | Done |
| T34 | Updated CLAUDE.md and PROGRESS_LOG.md | Done |
| T35 | Created Part model (11 fields, FK to Paper, UniqueConstraint) | Done |
| T36 | Added optional FK from MainsPYQ to Part | Done |
| T37 | Updated admin.py: PartAdmin, PartInline on PaperAdmin, part in raw_id_fields | Done |
| T38 | Migration 0009_part_model applied | Done |
| T39 | Updated CLAUDE.md and PROGRESS_LOG.md | Done |
| T40 | Created PrelimsPYQ model (35+ fields, 6 FKs, validators, save() override) | Done |
| T41 | Updated admin.py: PrelimsPYQAdmin with stem_preview, readonly analytics | Done |
| T42 | Migration 0010_prelims_pyq applied | Done |
| T43 | Updated CLAUDE.md and PROGRESS_LOG.md | Done |

### Database Counts (updated)
| Table | Count |
|---|---|
| content_subject | 11 |
| content_unit | 51 |
| content_chapter | 0 (ready for data) |
| content_topic | 0 (ready for data) |
| content_subtopic | 0 (ready for data) |
| content_exam | 1 |
| content_exam_session | 7 |
| content_paper | 10 |
| content_part | 0 (ready for data) |
| content_competency | 37 |
| content_mains_pyq | 1 (test) |
| content_prelims_pyq | 0 (ready for data) |

### All Model Tables Created
```
Syllabus:  Subject (11) → Unit (51) → Chapter (0) → Topic (0) → SubTopic (0)
Paper:     Paper (10) → Part (0)
Exam:      Exam (1) → ExamSession (7)
Questions: MainsPYQ (1, subjective), PrelimsPYQ (0, MCQ)
Other:     Competency (37)
```

### PrelimsPYQ Field Layers
```
Layer A — Identity:     uid, question_id
Layer B — Content:      stem, stem_hi, option_a-d, correct_answer, explanation, teaching_note, mnemonic, common_mistake, exam_tip
Layer C — Auto-computed: stem_length, option_avg_length, estimated_time_seconds (set by save())
Layer D — Live Analytics: times_attempted, times_correct, avg_time_taken (updated by practice engine)
Linkage:  exam_session, paper, subject, unit, chapter, topic (6 FKs)
Classification: difficulty, exam_source, year, tags, blooms_level, concept_cluster, repeat_frequency
Admin:    review_status, batch_id, is_free, is_active
```

---

## Session 4 — 01-Mar-2026

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T44 | Added topic FK to MainsPYQ (related_name='mains_pyqs_by_topic') | Done |
| T45 | Added fact_code (CharField max_length=20) to MainsPYQ | Done |
| T46 | Added tag_code (CharField max_length=50) to MainsPYQ | Done |
| T47 | Updated chapter FK related_name: 'mains_pyqs' → 'mains_pyqs_by_chapter' | Done |
| T48 | Updated part FK related_name: 'questions' → 'mains_pyqs_by_part' | Done |
| T49 | Updated admin.py: topic in raw_id_fields, fact_code/tag_code in search_fields | Done |
| T50 | Migration 0011_mainspyq_topic_factcode_tagcode applied | Done |
| T51 | Updated CLAUDE.md and PROGRESS_LOG.md | Done |
| T29B | Created tracker app (BuildTask + BuildSubTask models) | Done |
| T29B | Created BuildTaskAdmin + BuildSubTaskAdmin + inline | Done |
| T29B | Created seed_tasks management command (30 tasks, 4 subtasks) | Done |
| T29B | Migration tracker/0001_initial applied | Done |

### Migrations Applied
| # | Migration | Description |
|---|---|---|
| 0011 | mainspyq_topic_factcode_tagcode | Add topic FK, fact_code, tag_code; alter chapter/part related_names |
| tracker 0001 | initial | Create BuildTask + BuildSubTask tables |

### MainsPYQ FKs (updated)
```
exam_session → ExamSession (PROTECT, related_name='questions')
paper        → Paper       (PROTECT, related_name='questions')
part         → Part        (PROTECT, null, related_name='mains_pyqs_by_part')
subject      → Subject     (PROTECT, related_name='mains_pyqs')
unit         → Unit        (PROTECT, null, related_name='mains_pyqs')
chapter      → Chapter     (PROTECT, null, related_name='mains_pyqs_by_chapter')
topic        → Topic       (PROTECT, null, related_name='mains_pyqs_by_topic')
competency   → Competency  (PROTECT, null, related_name='questions')
```

### Tracker Data Seeded
```
Session 2: 13 tasks (all done)
Session 3: 17 tasks (6 done, 11 pending)
Subtasks: 4 total
  T28B: Upgrade PrelimsPYQ 8-layer (pending)
  T28C: Cascading Admin dropdowns (pending)
  T29B: BuildTask tracker (done)
  T29C: Test import 10+10 (pending)
```

### T43: Audit + Seed Chapter (Stone Age)
- Audited Chapter model: 12 fields, FK to Unit, 0 rows before seed
- Subject "History" already existed (id=2)
- Unit "Ancient & Medieval India" already existed (id=8)
- Chapter "Stone Age" created (id=1, code=STONE, slug=stone-age)
- Chain: History > Ancient & Medieval India > Stone Age

### T44: QuestionAppearance bridge table + repeat_count
- Audited PrelimsPYQ: 41 fields, repeat_count missing, repeat_frequency existed
- Added `repeat_count` (PositiveIntegerField, default=1) to PrelimsPYQ
- Created `QuestionAppearance` model (7 fields):
  - question (FK→PrelimsPYQ, CASCADE, related_name='appearances')
  - exam_source, exam_name, year, question_number, is_primary, created_at
  - UniqueConstraint: (question, year, exam_source)
- Migration 0012_add_question_appearance_bridge_table applied
- Admin: QuestionAppearanceInline on PrelimsPYQAdmin + standalone QuestionAppearanceAdmin
- Content app now has 13 models, 14 ModelAdmin classes, 7 inlines

### T44b: Topic auto-slug save()
- Added `save()` override to Topic model — auto-generates slug from name if empty
- No migration needed (Python logic only)

### T45+T46: MicroTopic + ExamSource models
- Created MicroTopic model (8 fields, FK→SubTopic PROTECT, auto-slug save(), UniqueConstraint)
- Created ExamSource model (8 fields, standalone lookup, exam_family + exam_stage choices)
- Migration 0013_add_microtopic_and_examsource applied
- Admin: MicroTopicAdmin + ExamSourceAdmin registered
- Content app now has 15 models, 16 ModelAdmin classes, 7 inlines

### Database Counts (updated)
| Table | Count |
|---|---|
| content_chapter | 1 (Stone Age) |
| content_question_appearance | 0 (bridge table ready) |
| content_microtopic | 0 (table ready) |
| content_exam_source | 0 (lookup table ready) |

### T47: Seed hierarchy + Import 5 Stone Age PrelimsPYQs
- **Step 1 (Audit)**: Audited PrelimsPYQ — 43 fields, topic FK exists, sub_topic/micro_topic FKs do NOT exist
- **Step 2 (Seed hierarchy)**: Created via Python shell:
  - 1 Exam: UPPCS Prelims (short_name=UPP)
  - 6 ExamSessions: 2004, 2006, 2008, 2010, 2015, 2016
  - 3 ExamSources: U.P.P.C.S. (Prelims), U.P. Lower Subordinate (Prelims), U.P.C.S. (Mains)
  - 4 Topics: Prehistoric Pioneers, Palaeolithic Age, Mesolithic Age, Neolithic Age
  - 5 SubTopics: Palaeolithic Discoveries, Classification Systems, Animal Domestication, Burial Practices, Agriculture Origin
  - 5 MicroTopics: Robert Bruce Foote, Christian Jurgensen Thomsen, Adamgarh & Bagor, Damdama Triple Burial, Lahuradeva
- **Step 3 (Import)**: Ran `scripts/import_5_stone_age.py`:
  - 5/5 questions created (HIST-SA-006 through HIST-SA-010)
  - 6 QuestionAppearance records (5 primary + 1 repeat)
  - 0 errors
  - Bridge table verified: HIST-SA-010 has 2 appearances (2004 primary, 2008 repeat)

### Database Counts (updated after T47)
| Table | Count |
|---|---|
| content_subject | 11 |
| content_unit | 51 |
| content_chapter | 1 (Stone Age) |
| content_topic | 4 |
| content_subtopic | 5 |
| content_microtopic | 5 |
| content_exam | 2 (UPPCS Mains + UPPCS Prelims) |
| content_exam_session | 13 (7 mains + 6 prelims) |
| content_paper | 10 |
| content_part | 0 |
| content_competency | 37 |
| content_mains_pyq | 1 (test) |
| content_prelims_pyq | 5 |
| content_question_appearance | 6 |
| content_exam_source | 3 |

### Cleanup: Clear test data for proper import
- Deleted in FK order: QuestionAppearance(6), PrelimsPYQ(5), MicroTopic(5), SubTopic(5), Topic(4), ExamSource(3)
- Foundation tables kept: Subject(11), Unit(51), Chapter(1)
- Exam(2) and ExamSession(13) kept

### Database Counts (after cleanup)
| Table | Count |
|---|---|
| content_subject | 11 |
| content_unit | 51 |
| content_chapter | 1 (Stone Age) |
| content_topic | 0 |
| content_subtopic | 0 |
| content_microtopic | 0 |
| content_exam | 2 |
| content_exam_session | 13 |
| content_paper | 10 |
| content_part | 0 |
| content_competency | 37 |
| content_mains_pyq | 1 (test) |
| content_prelims_pyq | 0 |
| content_question_appearance | 0 |
| content_exam_source | 0 |

### Set up django-import-export for PrelimsPYQ
- Installed `django-import-export 4.4.0` + `tablib 3.9.0`
- Added `import_export` to INSTALLED_APPS
- Made 3 FKs nullable on PrelimsPYQ: exam_session, paper, subject (migration 0014)
- Created `content/resources.py` with PrelimsPYQResource:
  - Maps Excel columns (Q.No., Question, Option (a)-(d), Answer, Exam Name, Year, Review_Status)
  - `import_id_fields = ['question_id']` for upsert by question_id
  - `before_import_row`: cleans answer format, defaults empty options, handles year parsing
  - `skip_row`: skips blank_question rows
- Updated PrelimsPYQAdmin: extends ImportExportModelAdmin with resource_classes
- All existing admin config preserved (inlines, raw_id_fields, readonly_fields)

### Management command: import_prelims_pyq
- Created `content/management/commands/import_prelims_pyq.py`
- Supports TWO Excel formats (auto-detects from headers):
  - **Format A (Flat)**: Single sheet with `question_id`, `stem`, `option_a`-`d`, `correct_answer`, `explanation`, `difficulty`, `exam_source`, `year`, `tags`
  - **Format B (Multi-tab)**: `MCQs - Ch1 CDoI` tabs with `Q.No.`, `Question`, `Option (a)`-`(d)`, `Answer`, `Exam Name`, `Exam Stage`, `Year`, `Review_Status`
- Features: `--dry-run`, `--batch-id`, `--subject` (partial match), `update_or_create` for idempotency, `QuestionAppearance` auto-creation
- Dry-run tested: `polity_import_ready.xlsx` — 560 questions, 0 skipped, 0 errors
- Subject partial match: `--subject Polity` resolves to "Indian Polity & Governance"

### Migration 0015: Widen PrelimsPYQ fields
- `option_a/b/c/d`: max_length 500 → 1000 (some GC Excel options exceeded 500 chars)
- `review_status`: max_length 10 → 25 (Excel values like `parse_error_no_options` = 22 chars)
- Added REVIEW_CHOICES: ok, needs_review, parse_error_no_options (to match Excel data)

### Prelims PYQ Import (GC Cleaned files)
Imported 3 Excel files using `import_prelims_pyq` command (multi-tab format, batch-id GC):

| File | Subject | Tabs | Imported | Skipped | Errors |
|---|---|---|---|---|---|
| PY_GC_Prelims_v2_cleaned.xlsx | Indian Polity & Governance | 42 | 2,484 | 4 | 0 |
| HIST_GC_Prelims_v2_cleaned.xlsx | History | 94 | 4,697 | 8 | 0 |
| GEO_GC_Prelims_v2_cleaned.xlsx | Geography | 72 | 3,492 | 4 | 0 |
| **TOTAL** | | **208** | **10,673** | **16** | **0** |

QuestionAppearance records: 10,127

Review status breakdown:
- ok: 9,907
- parse_error_no_options: 480
- needs_review: 286

### Database Counts (after import)
| Table | Count |
|---|---|
| content_subject | 11 |
| content_unit | 51 |
| content_chapter | 1 (Stone Age) |
| content_prelims_pyq | 10,673 |
| content_question_appearance | 10,127 |
| content_mains_pyq | 1 (test) |

---

## Session 6 — 15-Mar-2026

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T56 | Install DRF 3.16.1 + django-cors-headers 4.9.0 + django-filter 25.2 | Done |
| T57 | Configure REST_FRAMEWORK, CORS_ALLOWED_ORIGINS, MIDDLEWARE in settings | Done |
| T58 | Create content/serializers.py (7 serializers) | Done |
| T59 | Create content/api_views.py (3 ViewSets + 1 function view) | Done |
| T60 | Create content/api_urls.py with DefaultRouter | Done |
| T61 | Wire /api/ into mypcs_project/urls.py | Done |
| T62 | Test all 6 endpoints (stats, subjects, questions list/detail, check_answer, random_set) | Done |
| T63 | Save CODING_STANDARDS.md to project root | Done |

### API Endpoints
| Method | URL | Description |
|---|---|---|
| GET | /api/stats/ | Platform totals + breakdowns |
| GET | /api/subjects/ | 11 subjects with question/chapter counts |
| GET | /api/chapters/ | Chapters, filterable by ?unit__subject=id |
| GET | /api/chapters/{id}/topics/ | Topics for a chapter |
| GET | /api/questions/ | Paginated list (no correct_answer), filterable |
| GET | /api/questions/{id}/ | Detail with correct_answer + explanations + appearances |
| POST | /api/questions/{id}/check_answer/ | Submit {"answer":"A"}, get marks (+2.0/-0.66) |
| GET | /api/questions/random_set/?count=N | Random questions (max 50) |
| GET | /api/questions/by_chapter/?code=XX | Filter by chapter code |

### Serializers (content/serializers.py)
- SubjectSerializer: id, name, name_hi, code, slug, question_count, chapter_count
- ChapterSerializer: id, name, name_hi, code, slug, subject_name, unit_name, question_count
- TopicSerializer: id, name, name_hi, slug, sort_order
- AppearanceSerializer: exam_source, exam_name, year, is_primary
- QuestionListSerializer: NO correct_answer (student-facing list)
- QuestionDetailSerializer: WITH correct_answer + all teaching fields + appearances
- StatsSerializer: total counts + breakdowns

### Packages Installed
- djangorestframework 3.16.1
- django-cors-headers 4.9.0
- django-filter 25.2

### Settings Changes
- INSTALLED_APPS: added rest_framework, corsheaders, django_filters
- MIDDLEWARE: added corsheaders.middleware.CorsMiddleware (before SessionMiddleware)
- REST_FRAMEWORK: PageNumberPagination (20/page), DjangoFilterBackend, SearchFilter, OrderingFilter
- CORS_ALLOWED_ORIGINS: localhost:3000, 127.0.0.1:3000

---

## Session 7 — 15-Mar-2026 (I-02)

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T63 | Save CODING_STANDARDS.md to project root | Done |
| T64 | Create Next.js 16 project (TypeScript, Tailwind v4, App Router, src/ dir) | Done |
| T65 | Install next-pwa for PWA support | Done |
| T66 | Configure tricolor design tokens (saffron/green/navy) in Tailwind v4 @theme | Done |
| T67 | Set up custom fonts: Outfit (UI), Lexend (reading), Noto Sans Devanagari (Hindi) | Done |
| T68 | Create typed API client src/lib/api.ts (all endpoints + TypeScript interfaces) | Done |
| T69 | Create .env.local with NEXT_PUBLIC_API_URL | Done |
| T70 | Build home page with live stats from Django API | Done |
| T71 | Verify frontend-backend connection (10,673 questions, 11 subjects rendered) | Done |

### Frontend Stack
- Next.js 16.1.6 + React 19.2.3
- TypeScript 5.x
- Tailwind CSS v4 (CSS-based @theme, not tailwind.config.ts)
- next-pwa 5.6.0
- Location: C:\Users\antri\mypcs-frontend

### Design Tokens (Tailwind v4 @theme)
| Token | Hex | Usage |
|---|---|---|
| saffron | #E07020 | Primary accent, CTA buttons |
| saffron-glow | #F08830 | Hover states |
| saffron-pale | #FFF6EE | Light backgrounds |
| green | #046A38 | Success, correct answers |
| green-soft | #0A8A4C | Hover states |
| green-pale | #EDF8F1 | Light backgrounds |
| navy | #000080 | Secondary accent, links |
| navy-soft | #1A1A94 | Hover states |
| navy-pale | #F0F0FA | Light backgrounds |
| ivory | #FAF8F5 | Page background |
| cream | #F5F2ED | Card backgrounds |
| ink | #1A1714 | Primary text |
| ink-muted | #7A7168 | Secondary text |
| danger | #C0392B | Wrong answers, errors |
| gold | #B8860B | Badges, highlights |

### Typed API Client (src/lib/api.ts)
Interfaces: Subject, Chapter, Topic, Appearance, QuestionListItem, QuestionDetail, CheckAnswerResult, PlatformStats, PaginatedResponse
Methods: getStats, getSubjects, getChapters, getChapterTopics, getQuestions, getQuestion, checkAnswer, getRandomSet, getQuestionsByChapter

### Tailwind v4 Note
Next.js 16 ships with Tailwind v4 which uses CSS-based config (`@theme` blocks in globals.css) instead of `tailwind.config.ts`. Design tokens are defined in `src/app/globals.css`.

---

## Session 8 — 15-Mar-2026 (T72)

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T71.5 | Create Nav.tsx — sticky nav with tricolor branding, auth buttons | Done |
| T71.6 | Create Footer.tsx — 4-column footer with tricolor accent bar | Done |
| T72.1 | Hero section — Hindi tagline, live question count, dual CTAs | Done |
| T72.2 | Stats bar — 4 metrics from Django API (questions, chapters, coverage, subjects) | Done |
| T72.3 | Problem section — 4 cards: Cost, Access, Material, Method | Done |
| T72.4 | Features section — 6 feature cards with badges (Free/Premium) | Done |
| T72.5 | Subjects section — 8 cards, 3 live + 5 coming soon | Done |
| T72.6 | How It Works — 4 numbered steps with Hindi translations | Done |
| T72.7 | Pricing section — Free vs Premium (₹999/year) side by side | Done |
| T72.8 | Final CTA — navy gradient with tricolor divider | Done |
| T72.9 | SectionLabel helper — reusable colored accent + label | Done |

### Homepage Sections (9 total)
1. Hero — "Your Pathway to Civil Services for ₹999/year" + Hindi tagline
2. Stats Bar — 10,673+ PYQs, 208 chapters, 30yr coverage, 3 subjects (live from API)
3. Problem — Coaching vs mypcs.in comparison grid
4. Features — 6 cards: PYQs, Notes, Practice Engine, Repeat Detector, Analytics, Mobile-first
5. Subjects — 3 live (Polity 2,484, History 4,697, Geography 3,492) + 5 coming soon
6. How It Works — 4 steps with tricolor numbered circles
7. Pricing — Free (₹0) vs Premium (₹999/year) with feature lists
8. Final CTA — Navy gradient, tricolor divider, "Ek smartphone. Do ghante. Ek sapna."
9. Footer — Brand, Product, Subjects, Connect columns

### Files Created/Modified
| File | Action |
|---|---|
| src/components/Nav.tsx | Created — sticky nav, tricolor logo, auth buttons |
| src/components/Footer.tsx | Created — 4-column footer, tricolor accent |
| src/app/page.tsx | Rewritten — 9-section homepage with live API data |

---

## Session 9 — 15-Mar-2026 (T73 + S3-01)

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T73 | Create /subjects listing page — server-side, shows all subjects with PYQ counts | Done |
| S3-01 | Create /practice interactive page — client-side UPPCS marking (+2/-0.66) | Done |
| — | Update Django random_set to support ?subject=ID filtering | Done |
| — | Update api.ts: add Question/AnswerResult type aliases, getRandomSet subject param | Done |
| — | Fix useSearchParams Suspense boundary for Next.js static export | Done |

### /subjects Page (src/app/subjects/page.tsx)
- Server-side async component (fetches subjects at build/request time)
- Grid of subject cards with PYQ count badge + chapter count
- Plain `<a>` tags (not Next.js Link) for guaranteed navigation
- Only shows subjects with question_count > 0
- Links to /practice?subject_id=ID&subject_name=NAME
- Empty state if API is down

### /practice Page (src/app/practice/page.tsx)
- Client-side interactive page ("use client")
- Reads ?subject_id=ID&subject_name=NAME from URL search params
- Fetches 10 random questions via api.getRandomSet(10, subjectId)
- Shows one question at a time with A/B/C/D option buttons
- Submits answer via api.checkAnswer() — shows correct/wrong + marks
- Running score tracker with UPPCS marking (+2.0 correct, -0.66 wrong)
- Result banner with explanation after each answer
- Session complete screen: accuracy %, marks, correct/wrong, time
- Growth message based on accuracy (70%+, 40%+, <40%)
- Wrapped in Suspense boundary (required by Next.js for useSearchParams)

### Django API Change
- `random_set` action now accepts optional `?subject=ID` query param
- Filters questions by subject_id before random selection

### Files Created/Modified
| File | Action |
|---|---|
| content/api_views.py | Modified — random_set supports ?subject=ID |
| src/lib/api.ts | Modified — added Question/AnswerResult aliases, getRandomSet(count, subjectId?) |
| src/app/subjects/page.tsx | Created — subjects listing page (plain `<a>` tags) |
| src/app/practice/page.tsx | Created — interactive practice page |
| src/app/page.tsx | Modified — homepage subject cards now clickable `<a>` links to /practice |

### Next Tasks
| # | Task | Status |
|---|---|---|
| T52 | Populate remaining Chapters, Topics, SubTopics, Parts | Pending |
| T53 | Import 639 Mains PYQs | Pending |
| T75 | Add authentication/user model for practice tracking | Pending |

### Architecture (updated)
```
mypcs280226/
├── manage.py
├── CODING_STANDARDS.md
├── mypcs_project/
│   ├── settings.py          (DRF, CORS, django-filter configured)
│   ├── urls.py              (admin/ + api/)
│   ├── wsgi.py
│   └── asgi.py
├── content/
│   ├── models.py            (15 models)
│   ├── admin.py             (16 ModelAdmin + 7 inlines)
│   ├── management/
│   │   └── commands/
│   │       ├── load_subjects_units.py
│   │       └── import_prelims_pyq.py
│   ├── resources.py           (PrelimsPYQResource for import-export)
│   ├── serializers.py         (7 DRF serializers)
│   ├── api_views.py           (3 ViewSets + stats_view)
│   ├── api_urls.py            (DefaultRouter → /api/)
│   └── migrations/
│       ├── 0001–0013
│       ├── 0014_make_prelims_fks_nullable.py
│       └── 0015_widen_prelims_fields.py
├── tracker/
│   ├── models.py            (2 models: BuildTask, BuildSubTask)
│   ├── admin.py             (2 ModelAdmin + 1 inline)
│   ├── management/
│   │   └── commands/
│   │       └── seed_tasks.py
│   └── migrations/
│       └── 0001_initial.py
├── docs/
│   ├── PROGRESS_LOG.md
│   ├── HIERARCHY_MAP.md
│   └── MULTI_TENANT_NOTES.md
└── .claude/
    └── CLAUDE.md

mypcs-frontend/               (C:\Users\antri\mypcs-frontend)
├── package.json               (Next.js 16, React 19, Tailwind v4)
├── .env.local                 (NEXT_PUBLIC_API_URL)
└── src/
    ├── lib/
    │   └── api.ts             (typed API client, all endpoints)
    ├── components/
    │   ├── Nav.tsx            (sticky nav, tricolor logo, auth buttons)
    │   └── Footer.tsx         (4-column footer, tricolor accent)
    └── app/
        ├── globals.css        (Tailwind v4 @theme design tokens)
        ├── layout.tsx         (root layout, fonts: Outfit/Lexend/Noto)
        ├── page.tsx           (full homepage: 9 sections, live API data)
        ├── subjects/
        │   └── page.tsx       (subjects listing, server-side)
        └── practice/
            └── page.tsx       (interactive practice, client-side)
```
