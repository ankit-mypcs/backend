# MYPCS.IN — Content Hierarchy Map

## 8-Level Structure

```
Level   Model/Field       Example                          DB Table / Storage
─────   ──────────────    ───────────────────────────────   ──────────────────
  1     Subject           "History"                        content_subject (11 rows)
  2     └─ Unit           "Ancient & Medieval India"       content_unit (51 rows)
  3        └─ Part        "Ancient India"                  content_part (future)
  4           └─ Chapter  "Indus Valley Civilization"      content_chapter (future)
  5              └─ Section "Town Planning & Architecture" content_section (future)
  6                 └─ Topic "Great Bath of Mohenjo-Daro"  content_topic (future)
  7                    └─ Sub-Topic                        text field on question
  8                       └─ Micro-Topic                   text field on question
```

Levels 1–6 = separate database tables (ForeignKey chain)
Levels 7–8 = text fields on the question model (no separate tables)

---

## Example: History

```
📜 History (Subject)
├── Ancient & Medieval India (Unit)
│   ├── Ancient India (Part)
│   │   ├── Indus Valley Civilization (Chapter)
│   │   │   ├── Town Planning & Architecture (Section)
│   │   │   │   └── Great Bath of Mohenjo-Daro (Topic)
│   │   │   ├── Economic Life & Trade (Section)
│   │   │   └── Script & Seals (Section)
│   │   ├── Vedic Period (Chapter)
│   │   ├── Mahajanapadas & Rise of Buddhism (Chapter)
│   │   ├── Mauryan Empire (Chapter)
│   │   └── Gupta Empire & Post-Gupta (Chapter)
│   └── Medieval India (Part)
│       ├── Delhi Sultanate (Chapter)
│       ├── Mughal Empire (Chapter)
│       └── Bhakti & Sufi Movements (Chapter)
├── Modern India (1757-1947) (Unit)
│   ├── British Expansion & Consolidation (Part)
│   ├── Socio-Religious Reform Movements (Part)
│   ├── Freedom Struggle (Part)
│   └── Post-1919 Movements (Part)
├── World History (Unit)
│   ├── Industrial Revolution (Part)
│   ├── World Wars (Part)
│   └── Decolonization (Part)
└── Art & Culture (Unit)
    ├── Architecture (Part)
    ├── Paintings & Sculpture (Part)
    └── Performing Arts & Literature (Part)
```

## Example: Indian Polity & Governance

```
⚖️ Indian Polity & Governance (Subject)
├── Constitutional Framework (Unit)
│   ├── Making of the Constitution (Part)
│   │   ├── Constituent Assembly (Chapter)
│   │   │   ├── Composition & Committees (Section)
│   │   │   │   └── Drafting Committee (Topic)
│   │   │   └── Key Debates (Section)
│   │   └── Preamble (Chapter)
│   ├── Fundamental Features (Part)
│   │   ├── Salient Features of the Constitution (Chapter)
│   │   ├── Sources of the Constitution (Chapter)
│   │   └── Schedules & Articles Overview (Chapter)
│   └── Amendment Process (Part)
├── Federalism & Centre-State (Unit)
│   ├── Division of Powers (Part)
│   ├── Centre-State Relations (Part)
│   └── Inter-State Relations (Part)
├── Parliament & State Legislature (Unit)
│   ├── Structure & Composition (Part)
│   ├── Legislative Process (Part)
│   └── Parliamentary Committees (Part)
├── Elections & Political Process (Unit)
│   ├── Election Commission (Part)
│   ├── Electoral Reforms (Part)
│   └── Political Parties (Part)
├── Judiciary (Unit)
│   ├── Supreme Court (Part)
│   ├── High Courts (Part)
│   └── Judicial Review & PIL (Part)
├── Local Self-Government (Unit)
│   ├── Panchayati Raj (73rd Amendment) (Part)
│   └── Urban Local Bodies (74th Amendment) (Part)
└── Rights & Duties (Unit)
    ├── Fundamental Rights (Part)
    ├── Directive Principles (Part)
    └── Fundamental Duties (Part)
```

---

## Complete Subject → Unit Map

### 1. ⚖️ Indian Polity & Governance (7 units)
1. Constitutional Framework
2. Federalism & Centre-State
3. Parliament & State Legislature
4. Elections & Political Process
5. Judiciary
6. Local Self-Government
7. Rights & Duties

### 2. 📜 History (4 units)
1. Ancient & Medieval India
2. Modern India (1757-1947)
3. World History
4. Art & Culture

### 3. 🌍 Geography (3 units)
1. Physical Geography
2. Indian Geography
3. Human Geography

### 4. 💰 Economy (6 units)
1. Indian Economy
2. Agriculture & Food Security
3. Inclusive Growth & Development
4. Infrastructure & Energy
5. Industry & MSME
6. Fiscal & Monetary Policy

### 5. 🧭 Ethics (7 units)
1. Ethics & Human Values
2. Ethics in Governance
3. Ethical Concepts & Theories
4. Attitude & Aptitude
5. Emotional Intelligence
6. Moral Thinkers & Philosophers
7. Case Studies

### 6. 👥 Society (3 units)
1. Indian Society
2. Social Empowerment
3. Indian Culture & Heritage

### 7. 🛡️ Internal Security (4 units)
1. Internal Security
2. Defence & Military
3. Cyber Security
4. Disaster Management

### 8. 🌐 International Relations (4 units)
1. India's Foreign Policy
2. Bilateral & Multilateral Relations
3. International Organizations
4. Geopolitics & Strategy

### 9. 🔬 Science & Technology (3 units)
1. S&T Developments
2. Emerging Technologies
3. Biotechnology

### 10. 🌱 Environment & Ecology (2 units)
1. Environment & Ecology
2. Conservation & Biodiversity

### 11. 🏛️ Uttar Pradesh Special (8 units)
1. UP History & Culture
2. UP Geography
3. UP Economy
4. UP Governance & Polity
5. UP Society
6. UP Environment
7. UP Science & Tech
8. UP Law & Order

---

**Totals:** 11 Subjects → 51 Units → Parts (next step)
