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

### I-04: Pushed both projects to GitHub
- Backend: https://github.com/ankit-mypcs/backend (commit 7767cab)
- Frontend: https://github.com/ankit-mypcs/frontend (commit eb1446a)
- Updated .gitignore: added *.xlsx, *.csv, media/, staticfiles/
- Credential manager switched from ankit-chawla03 to ankit-mypcs

### I-04b: Production deployment config (commit fdb6afc)
- Installed: gunicorn 25.1.0, whitenoise 6.12.0, dj-database-url 3.1.2, psycopg2-binary 2.9.11
- Created requirements.txt (20 packages)
- Created Procfile: `gunicorn mypcs_project.wsgi --bind 0.0.0.0:$PORT`
- Created runtime.txt: `python-3.12` (Railway doesn't support 3.14 yet)
- Created railway.json: Nixpacks builder, migrate-on-deploy, restart on failure
- Updated settings.py:
  - WhiteNoise middleware (after SecurityMiddleware) — serves static files without nginx
  - STATIC_ROOT = staticfiles/ + CompressedManifestStaticFilesStorage
  - ALLOWED_HOSTS from env var (falls back to localhost)
  - CORS: added Vercel production URL + CORS_ALLOW_ALL toggle via env
- collectstatic: 170 files → staticfiles/ (gitignored)

### Railway env vars needed
| Variable | Example | Notes |
|---|---|---|
| DATABASE_URL | postgres://user:pass@host:5432/db | Railway provides this |
| SECRET_KEY | random-string-here | Generate a new one |
| DEBUG | False | Must be False in production |
| ALLOWED_HOSTS | your-app.railway.app | Comma-separated |
| CORS_ALLOW_ALL | True | Optional, for Vercel previews |

### Fix: DATABASE_URL cleanup (commit 3269f58)
- Renamed `DATABASE_URL` variable to `_db_url` to avoid shadowing env key name
- Removed old WHY comment (redundant)
- Confirmed: zero `env.db` or `env('DATABASE_URL')` calls remain
- Only reference: `_db_url = os.environ.get('DATABASE_URL', '')` with SQLite fallback
- `python manage.py check` passes clean

### Fix: Remove django-environ completely (commit db0e8ad)
- Removed `import environ`, `env = environ.Env()`, `environ.Env.read_env('.env')`
- Replaced `env('SECRET_KEY')` → `os.environ.get('SECRET_KEY', 'dev-insecure-key-change-in-production')`
- Replaced `env.bool('DEBUG', default=False)` → `os.environ.get('DEBUG', 'False') == 'True'`
- All 5 env var reads now use `os.environ.get()` with safe defaults
- Zero `env(` calls remain in settings.py — grep confirmed
- `python manage.py check` passes clean
- **Why**: django-environ crashes on Railway when .env file doesn't exist during build

---

## Session 10 — 15-Mar-2026 (v7 Homepage)

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T76 | Convert homepage to v7 dark design with saffron accent | Done |

### v7 Homepage Design (commit 7b41e86)
- **Theme**: Dark #0A0A0F background, saffron #E07A2F accent
- **Fonts**: Satoshi (Fontshare, UI headings), JetBrains Mono (Google, stats/numbers)
- **CSS**: homepage.module.css (CSS modules, ~580 lines)
- **Component**: 'use client' with IntersectionObserver scroll reveals
- **Tricolor**: 2px stripe fixed at top (saffron 33% / white 33% / green 33%)
- **Footer**: 36px tricolor micro-line
- **CTA divider**: gradient saffron → green
- **Nav**: Glass effect (backdrop-blur + rgba bg), saffron hover on links
- **Hero**: Gradient mesh + grid overlay, saffron glow CTA button
- **Features**: Bento grid cards, saffron top accent, hover lift + shadow
- **Stats**: JetBrains Mono numbers in saffron
- **Badges**: Free = green-soft (#34D399), Premium = saffron (#E07A2F)
- **Pricing**: Premium card has saffron border, free has subtle border
- **Scroll reveals**: fade-up with cubic-bezier(0.4,0,0.2,1), 0.6s
- **Color system**: --bg, --bg-surface, --bg-elevated, --text-1/2/3/4, --saffron, --green-soft
- **Old Nav.tsx + Footer.tsx**: Still exist for /subjects and /practice pages (light theme)

### Files Created/Modified
| File | Action |
|---|---|
| src/app/homepage.module.css | Created — all v7 dark theme styles (~580 lines) |
| src/app/page.tsx | Rewritten — v7 dark homepage, 'use client', scroll reveals |
| src/app/layout.tsx | Modified — added Satoshi (Fontshare), JetBrains Mono, dark body bg |

### Next Tasks
| # | Task | Status |
|---|---|---|
| T52 | Populate remaining Chapters, Topics, SubTopics, Parts | Done (via S11) |
| T53 | Import 639 Mains PYQs | Pending |
| T75 | Add authentication/user model for practice tracking | Pending |
| T77 | Update /subjects and /practice pages to match dark theme | Pending |

### Architecture (updated)
### Architecture (S10)
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
        ├── layout.tsx         (root layout, fonts: Satoshi/JetBrains Mono/Outfit/Lexend/Noto)
        ├── homepage.module.css (v7 dark theme styles, CSS modules)
        ├── page.tsx           (v7 dark homepage, 'use client', scroll reveals)
        ├── subjects/
        │   └── page.tsx       (subjects listing, server-side)
        └── practice/
            └── page.tsx       (interactive practice, client-side)
```

---

## Session 11 — 17-Mar-2026 (Schema v2 + Ancient History Pipeline)

### Summary
Complete schema rebuild from 15 models to 27 models. Wiped all old data (10,673 prelims).
Built XLSX-driven content pipeline. Deployed Stone Age chapter end-to-end with 13 working API endpoints.
Work split: Cowork Claude (strategy/blueprinting/file creation) → VS Code Claude (execution against production).

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T78 | Design production models.py — 27 models, single content app, no Hindi | Done |
| T79 | Create upload_chapter.py — header-based XLSX parser, all 10 sheets | Done |
| T80 | Create upload_prelims.py — PYQ XLSX parser, row 2 headers, fuzzy chapter matching | Done |
| T81 | Sandbox test — full pipeline: migrate, seed, upload, verify, API | Done |
| T82 | Delete old migrations 0001-0015, create fresh 0001_initial.py | Done |
| T83 | Drop all old content_ tables, apply fresh migration (30 tables) | Done |
| T84 | Seed taxonomy: History → Ancient India → 2 Units + UP State | Done |
| T85 | Upload Stone Age chapter: 356 content records across 10 sheets | Done |
| T86 | Upload 1,178 Prelims PYQs (243 complete + 935 flagged no-options) | Done |
| T87 | Deploy serializers.py, views.py, urls.py — 13 API endpoints | Done |
| T88 | Deploy admin.py — custom admin classes for all 27 models | Done |
| T89 | Test all API endpoints — all passing | Done |
| T90 | Create COWORK_SYSTEM.md — persistent role/context/architecture doc | Done |
| T91 | Update CLAUDE.md + PROGRESS_LOG.md | Done |

### Schema Changes (v1 → v2)
- Old Part (FK to Paper) renamed → PaperSection
- New Part for taxonomy: Subject → Part → Unit → Chapter
- Unit FK changed: Subject → Part
- 12 new content models: State, SourceBook, Fact, Site, TimelineEvent, GlossaryTerm, ExamIntelEntry, ComparisonMatrix, Visual, Exercise, FactQuestionLink, SiteQuestionLink
- Fresh migration 0001_initial.py (old 0001-0015 deleted)

### Files Created/Replaced
| File | Action |
|---|---|
| content/models.py | Replaced — 27 models (was 15) |
| content/serializers.py | Replaced — new serializers for all content + PYQ |
| content/views.py | Replaced — ChapterViewSet (8 sub-endpoints), PrelimsViewSet, stats_view |
| content/urls.py | Created — DRF router wiring |
| content/admin.py | Replaced — custom admin for all 27 models |
| content/management/commands/upload_chapter.py | Created — XLSX 10-sheet parser |
| content/management/commands/upload_prelims.py | Created — PYQ XLSX parser |
| data/chapters/HIS_StoneAge_Ch4.xlsx | Copied — ready |
| data/chapters/HIS_Chalcolithic_Ch5.xlsx | Copied — ready |
| data/chapters/HIS_HarappanCiv_Ch6.xlsx | Copied — ready |
| data/PYQ/UPPCS_PYQ_Ancient_History_v2.xlsx | Copied — uploaded |

### API Endpoints (13 total, all tested)
| Method | URL | Response |
|---|---|---|
| GET | /api/stats/ | chapters:1, facts:160, prelims_pyqs:1178, prelims_complete:243 |
| GET | /api/chapters/ | 1 chapter with counts |
| GET | /api/chapters/stone-age/ | Detail with 7 topics + subtopics |
| GET | /api/chapters/stone-age/facts/ | 160 facts |
| GET | /api/chapters/stone-age/sites/ | 65 sites |
| GET | /api/chapters/stone-age/timeline/ | 29 events |
| GET | /api/chapters/stone-age/terms/ | 30 terms |
| GET | /api/chapters/stone-age/exam-intel/ | 20 entries |
| GET | /api/chapters/stone-age/concepts/ | 1 matrix |
| GET | /api/chapters/stone-age/visuals/ | 25 visuals |
| GET | /api/chapters/stone-age/exercises/ | 26 exercises |
| GET | /api/questions/?chapter=stone-age | 46 PYQs |
| GET | /api/questions/{id}/ | Full question detail |

### Database Counts (17-Mar-2026)
| Table | Count |
|---|---|
| content_state | 1 |
| content_subject | 1 |
| content_part | 1 |
| content_unit | 2 |
| content_chapter | 1 (Stone Age) |
| content_topic | 7 |
| content_subtopic | 25 |
| content_fact | 160 |
| content_site | 65 |
| content_timeline_event | 29 |
| content_glossary_term | 30 |
| content_exam_intel_entry | 20 |
| content_comparison_matrix | 1 |
| content_visual | 25 |
| content_exercise | 26 |
| content_prelims_pyq | 1,178 |

### Architecture (S11)
```
mypcs280226/
├── manage.py
├── mypcs_project/
│   ├── settings.py          (DRF, CORS configured)
│   └── urls.py              (admin/ + api/)
├── content/
│   ├── models.py            (27 models — v2 schema)
│   ├── admin.py             (custom admin for all 27 models)
│   ├── serializers.py       (13 serializers — taxonomy, content, PYQ, stats)
│   ├── views.py             (ChapterViewSet, PrelimsViewSet, stats_view)
│   ├── urls.py              (DRF router → /api/)
│   ├── api_views.py         (OLD — superseded by views.py)
│   ├── api_urls.py          (OLD — superseded by urls.py)
│   ├── resources.py         (OLD — import-export resource)
│   ├── management/commands/
│   │   ├── upload_chapter.py     (NEW — XLSX 10-sheet parser)
│   │   ├── upload_prelims.py     (NEW — PYQ XLSX parser)
│   │   ├── import_prelims_pyq.py (OLD — superseded)
│   │   └── load_subjects_units.py (OLD — superseded)
│   └── migrations/
│       └── 0001_initial.py  (fresh — 27 models, 30 tables)
├── data/
│   ├── chapters/            (3 XLSX files)
│   └── PYQ/                 (1 XLSX file)
├── tracker/                 (unchanged)
├── docs/
│   └── PROGRESS_LOG.md
└── .claude/
    └── CLAUDE.md
```

---

## Session 12 — 17-Mar-2026 (Ch5 + Ch6 Uploads)

### T92a: Upload Chalcolithic Age (Ch5)
- Dry run: 235 rows across 10 sheets — passed
- Real upload: 235 content records created
- Breakdown: Timeline:15, Concepts:9, Sites:33, KeyFacts:40, State_Specific:43, Society:31, Images:13, Terms:17, ExamAnalysis:17, Exercises:17
- Chapter: chalcolithic-age (number 5, unit: prehistoric-india)
- Running totals: 2 chapters, 274 facts, 98 sites

### Next Tasks
| # | Task | Status |
|---|---|---|
| T92a | Upload Chalcolithic (Ch5) | Done |
| T92b | Upload Harappan (Ch6) | Pending |
| T93 | Build frontend chapter view pages | Pending |
| T94 | Build Mains PYQ upload pipeline | Pending |
| T95 | Deploy to Railway | Done (S13) |
| T96 | Clean up OLD files (api_views.py, api_urls.py, resources.py, old commands) | Pending |

---

## Session 13 — 18-Mar-2026 (Railway Deployment + Seeding)

### Summary
Deployed Django backend to Railway with full seed data. Fixed GitHub auto-deploy connection, built JSON fixture pipeline from XLSX files, resolved two fixture bugs (missing timestamps, State model has no timestamp fields). Backend is live and serving 1,822 objects via REST API.

### Tasks Completed
| # | Task | Status |
|---|---|---|
| T95 | Deploy backend to Railway (thorough-nurturing project) | Done |
| T95a | Fix Railway GitHub App — installed on ankit-mypcs account, reconnected repo | Done |
| T95b | Create gen_fixture.py — generates Django-compatible JSON fixture from 3 XLSX files | Done |
| T95c | Create seed_if_empty management command — safe idempotent seeding on every deploy | Done |
| T95d | Update railway.json — collectstatic + migrate + seed_if_empty + gunicorn | Done |
| T95e | Fix seed.json — add created_at/updated_at timestamps (loaddata doesn't auto-populate auto_now_add) | Done |
| T95f | Fix seed.json — exclude State model from timestamps (State has no timestamp fields) | Done |
| T95g | Verify live API — /api/stats/ returns real counts (1,822 objects) | Done |
| T95h | Update CLAUDE.md with Railway deployment info | Done |

### Deployment Details
- **Railway project**: thorough-nurturing (production environment)
- **Live URL**: https://backend-production-a889.up.railway.app
- **Region**: asia-southeast1-eqsg3a
- **Builder**: Nixpacks (auto-detects Python/Django)
- **Auto-deploy**: GitHub push to main → Railway builds + deploys automatically
- **Start command**: `collectstatic --noinput && migrate && seed_if_empty && gunicorn`

### Fixture Pipeline
- **gen_fixture.py**: Reads 3 XLSX files → generates Django-compatible JSON fixture
  - Input: HIS_StoneAge_Ch4.xlsx, HIS_Chalcolithic_Ch5.xlsx, UPPCS_PYQ_Ancient_History_v2.xlsx
  - Output: data/seed.json (1,822 objects, ~2.0 MB)
  - Handles: taxonomy, 10 content sheet types, PrelimsPYQ with fuzzy chapter matching
  - Timestamps: Adds created_at/updated_at per model (skips State which has no timestamp fields)
- **seed_if_empty command**: Loads seed.json ONLY if no chapters exist in DB (safe for repeated deploys)

### Bugs Fixed
| Bug | Root Cause | Fix |
|---|---|---|
| IntegrityError: null created_at | Django loaddata ignores auto_now_add fields | Added explicit timestamps to gen_fixture.py |
| DeserializationError: State has no field 'created_at' | State model has no timestamp fields | Added MODELS_NO_TIMESTAMPS exclusion set |

### Live API Verification (18-Mar-2026)
| Endpoint | Response |
|---|---|
| /api/stats/ | chapters:2, topics:12, facts:274, sites:98, timeline_events:44, glossary_terms:47, visuals:38, exercises:43, prelims_pyqs:1178, prelims_complete:243 |

### Files Created
| File | Description |
|---|---|
| content/management/commands/seed_if_empty.py | Idempotent seeding command |
| data/seed.json | Django fixture (1,822 objects) |
| gen_fixture.py | XLSX → JSON fixture generator (not committed, project root) |

### Files Modified
| File | Change |
|---|---|
| railway.json | Added collectstatic + seed_if_empty to start command |
| .claude/CLAUDE.md | Updated with Railway deployment info, seed_if_empty command, data files |

### Commits
| Hash | Message |
|---|---|
| c895a27 | add seed fixture and seed_if_empty command for Railway |
| e8d71bb | fix: add created_at/updated_at timestamps to seed.json |
| 00b8ffe | fix: exclude State model from timestamps in seed.json |
| e6f9798 | docs: update CLAUDE.md — Railway deployment live with seeded data |

### Next Tasks
| # | Task | Status |
|---|---|---|
| T92b | Upload Harappan (Ch6) chapter | Pending |
| T93 | Build frontend chapter view + question practice pages | Pending |
| T97 | Deploy frontend to Vercel | Pending |
| T94 | Build Mains PYQ upload pipeline | Pending |
| T96 | Clean up OLD files (api_views.py, api_urls.py, resources.py, old commands) | Pending |
| T98 | Delete old thorough-warmth Railway project (stale DB) | Pending |
