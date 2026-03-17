"""
content/models.py — MYPCS Production Models
Single content app. XLSX-driven. No Hindi fields (deferred).

TAXONOMY:  Subject → Part → Unit → Chapter → Topic → SubTopic → MicroTopic
CONTENT:   Fact, Site, TimelineEvent, GlossaryTerm, ExamIntelEntry,
           ComparisonMatrix, Visual, Exercise
EXAM:      Exam, ExamSession, Paper, PaperSection, Competency
QUESTIONS: PrelimsPYQ, MainsPYQ
TRACKING:  QuestionAppearance, ExamSource, FactQuestionLink, SiteQuestionLink
REFERENCE: State, SourceBook
"""
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# ─────────────────────────────────────────────
# REFERENCE
# ─────────────────────────────────────────────

class State(models.Model):
    """Indian states for multi-state content tagging."""
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    exam_name = models.CharField(max_length=50, blank=True, default='')
    exam_full = models.CharField(max_length=200, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'content_state'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.code} — {self.name}"


class SourceBook(models.Model):
    """Reference books (RS, ML, RT, TN, etc.)."""
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_sourcebook'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} — {self.title}"


# ─────────────────────────────────────────────
# TAXONOMY: Subject → Part → Unit → Chapter → Topic → SubTopic → MicroTopic
# ─────────────────────────────────────────────

class Subject(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    icon = models.CharField(max_length=5, blank=True, default='')
    description = models.TextField(blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_subject'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name


class Part(models.Model):
    """Taxonomy Part: Ancient India, Medieval India, Modern India, etc."""
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                related_name='parts')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_part'
        ordering = ['subject', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['subject', 'name'],
                                    name='unique_part_per_subject'),
        ]

    def __str__(self):
        return f"{self.subject.name} → {self.name}"


class Unit(models.Model):
    """Taxonomy Unit: Prehistoric India, Vedic Period, etc."""
    part = models.ForeignKey(Part, on_delete=models.PROTECT,
                             related_name='units')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_unit'
        ordering = ['part', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['part', 'name'],
                                    name='unique_unit_per_part'),
        ]

    def __str__(self):
        return f"{self.part.name} → {self.name}"


class Chapter(models.Model):
    """Chapter — one per XLSX file."""
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT,
                             related_name='chapters')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True, default='')
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, default='')
    chapter_number = models.PositiveIntegerField()
    sort_order = models.PositiveIntegerField(default=0)
    question_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_chapter'
        ordering = ['unit', 'sort_order', 'chapter_number']
        constraints = [
            models.UniqueConstraint(fields=['unit', 'chapter_number'],
                                    name='unique_chapter_number_per_unit'),
        ]

    def __str__(self):
        return f"{self.unit.name} → {self.name}"


class Topic(models.Model):
    """Maps to XLSX 'Topic' column."""
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='topics')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=150, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_topic'
        ordering = ['chapter', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['chapter', 'name'],
                                    name='unique_topic_per_chapter'),
        ]

    def __str__(self):
        return f"{self.chapter.name} → {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(f"{self.chapter.slug}-{self.name}")[:150]
        super().save(*args, **kwargs)


class SubTopic(models.Model):
    """Maps to XLSX 'MicroTopic' column (renamed for clarity)."""
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT,
                              related_name='subtopics')
    name = models.CharField(max_length=200)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_subtopic'
        ordering = ['topic', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['topic', 'name'],
                                    name='unique_subtopic_per_topic'),
        ]

    def __str__(self):
        return f"{self.topic.name} → {self.name}"


class MicroTopic(models.Model):
    """Finest-grained. For PYQ AI-Topic linking."""
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.PROTECT,
                                  related_name='microtopics')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_microtopic'
        ordering = ['sub_topic', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['sub_topic', 'name'],
                                    name='unique_microtopic_per_subtopic'),
        ]

    def __str__(self):
        return f"{self.sub_topic.name} → {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────
# CONTENT (one model per XLSX sheet type)
# ─────────────────────────────────────────────

class Fact(models.Model):
    """Sheet 4 (KeyFacts) + Sheet 5 (State_Specific) + Sheet 6 (Society)."""
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='facts')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='facts')
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='facts')
    text = models.TextField()
    citation = models.CharField(max_length=200, blank=True, default='')
    source_sheet = models.CharField(max_length=30, blank=True, default='',
                                    help_text="Which sheet: KeyFacts, State_Specific, Society")
    state_relevance = models.ManyToManyField(State, blank=True,
                                             related_name='facts')
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_fact'
        ordering = ['chapter', 'topic', 'sort_order']

    def __str__(self):
        return f"{self.text[:60]}"


class Site(models.Model):
    """Sheet 3 (Sites)."""
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='sites')
    name = models.CharField(max_length=200)
    state_region = models.CharField(max_length=200, blank=True, default='')
    state_code = models.CharField(max_length=5, blank=True, default='')
    period = models.CharField(max_length=100, blank=True, default='')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='sites')
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='sites')
    key_findings = models.TextField(blank=True, default='')
    citation = models.CharField(max_length=200, blank=True, default='')
    state_relevance = models.ManyToManyField(State, blank=True,
                                             related_name='sites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_site'
        ordering = ['chapter', 'name']

    def __str__(self):
        return f"{self.name} ({self.state_region})"


class TimelineEvent(models.Model):
    """Sheet 1 (Timeline)."""
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='timeline_events')
    date_text = models.CharField(max_length=100)
    event = models.TextField()
    citation = models.CharField(max_length=200, blank=True, default='')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='timeline_events')
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_timeline_event'
        ordering = ['chapter', 'sort_order']

    def __str__(self):
        return f"{self.date_text}: {self.event[:60]}"


class GlossaryTerm(models.Model):
    """Sheet 8 (Terms)."""
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='glossary_terms')
    term = models.CharField(max_length=200)
    definition = models.TextField()
    citation = models.CharField(max_length=200, blank=True, default='')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='glossary_terms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_glossary_term'
        ordering = ['chapter', 'term']
        constraints = [
            models.UniqueConstraint(fields=['chapter', 'term'],
                                    name='unique_term_per_chapter'),
        ]

    def __str__(self):
        return self.term


class ExamIntelEntry(models.Model):
    """Sheet 9 (ExamAnalysis)."""
    CATEGORY_CHOICES = [
        ('Most Tested Fact', 'Most Tested Fact'),
        ('Common MCQ Pattern', 'Common MCQ Pattern'),
        ('Typical Mains Question', 'Typical Mains Question'),
        ('Trick Question', 'Trick Question'),
        ('Fact Check', 'Fact Check'),
        ('Trend', 'Trend'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='exam_intel_entries')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='exam_intel_entries')
    detail = models.TextField()
    citation = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_exam_intel_entry'
        ordering = ['chapter', 'category']

    def __str__(self):
        return f"{self.category} — {self.chapter.name}"


class ComparisonMatrix(models.Model):
    """Sheet 2 (Concepts)."""
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='comparison_matrices')
    title = models.CharField(max_length=200)
    parameters = models.JSONField(default=list)
    columns = models.JSONField(default=list)
    data = models.JSONField(default=dict)
    citation = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_comparison_matrix'

    def __str__(self):
        return f"{self.chapter.name} — {self.title}"


class Visual(models.Model):
    """Sheet 7 (Images)."""
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='visuals')
    ref_code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500)
    source_book = models.CharField(max_length=100, blank=True, default='')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='visuals')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_visual'
        ordering = ['chapter', 'ref_code']

    def __str__(self):
        return f"{self.ref_code} — {self.description[:60]}"


class Exercise(models.Model):
    """Sheet 10 (Exercises)."""
    TYPE_CHOICES = [
        ('Book Exercise', 'Book Exercise'),
        ('UPPCS Prelims Pattern', 'UPPCS Prelims Pattern'),
        ('UPPCS Mains Pattern', 'UPPCS Mains Pattern'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='exercises')
    exercise_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='exercises')
    question = models.TextField()
    source = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_exercise'
        ordering = ['chapter', 'exercise_type']

    def __str__(self):
        return f"[{self.exercise_type}] {self.question[:60]}"


# ─────────────────────────────────────────────
# EXAM INFRASTRUCTURE
# ─────────────────────────────────────────────

class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='exams')
    description = models.TextField(blank=True, default='')
    is_target_exam = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_exam'
        ordering = ['name']

    def __str__(self):
        return self.short_name


class ExamSession(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT,
                             related_name='sessions')
    year = models.PositiveIntegerField()

    notification_date = models.DateField(null=True, blank=True)
    prelims_date = models.DateField(null=True, blank=True)
    mains_date = models.DateField(null=True, blank=True)
    final_result_date = models.DateField(null=True, blank=True)

    total_questions_prelims = models.PositiveIntegerField(null=True, blank=True)
    positive_marks_prelims = models.DecimalField(
        max_digits=4, decimal_places=2, default=2.00)
    negative_marks_prelims = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.66)

    cutoff_prelims_general = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_prelims_obc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_prelims_sc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_prelims_st = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_mains_general = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_mains_obc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_mains_sc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_mains_st = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    students_applied = models.PositiveIntegerField(null=True, blank=True)
    students_final_selected = models.PositiveIntegerField(null=True, blank=True)
    posts_advertised = models.PositiveIntegerField(null=True, blank=True)

    notes = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_exam_session'
        unique_together = ['exam', 'year']
        ordering = ['-year', 'exam']

    def __str__(self):
        return f"{self.exam.short_name} {self.year}"


class Paper(models.Model):
    STAGE_CHOICES = [
        ('prelims', 'Prelims'),
        ('mains', 'Mains'),
        ('both', 'Both'),
    ]
    TYPE_CHOICES = [
        ('objective', 'Objective'),
        ('subjective', 'Subjective'),
        ('essay', 'Essay'),
        ('language', 'Language'),
    ]

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    exam_stage = models.CharField(max_length=10, choices=STAGE_CHOICES,
                                  default='mains')
    total_marks = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=180)
    paper_type = models.CharField(max_length=12, choices=TYPE_CHOICES,
                                  default='subjective')
    is_qualifying = models.BooleanField(default=False)
    negative_marking = models.BooleanField(default=False)
    syllabus_topics = models.JSONField(default=list, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_paper'
        ordering = ['sort_order']

    def __str__(self):
        return self.short_name


class PaperSection(models.Model):
    """Section within a paper (was 'Part' in old schema)."""
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT,
                              related_name='sections')
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    marks = models.PositiveIntegerField(default=0)
    question_count = models.PositiveIntegerField(default=0)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_paper_section'
        ordering = ['paper', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['paper', 'name'],
                                    name='unique_section_per_paper'),
        ]

    def __str__(self):
        return f"{self.paper.short_name} → {self.name}"


class Competency(models.Model):
    BLOOMS_CHOICES = [
        ('Remember', 'Remember'),
        ('Understand', 'Understand'),
        ('Apply', 'Apply'),
        ('Analyze', 'Analyze'),
        ('Evaluate', 'Evaluate'),
        ('Create', 'Create'),
    ]

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, default='')
    blooms_level = models.CharField(max_length=12, choices=BLOOMS_CHOICES,
                                    blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_competency'
        ordering = ['sort_order', 'name']
        verbose_name_plural = 'Competencies'

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
# QUESTIONS
# ─────────────────────────────────────────────

class PrelimsPYQ(models.Model):
    ANSWER_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'), ('Medium', 'Medium'),
        ('Hard', 'Hard'), ('Unknown', 'Unknown'),
    ]
    REVIEW_CHOICES = [
        ('draft', 'Draft'), ('ok', 'OK'),
        ('needs_review', 'Needs Review'),
        ('parse_error_no_options', 'Parse Error'),
        ('reviewed', 'Reviewed'), ('approved', 'Approved'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    question_id = models.CharField(max_length=30, unique=True)

    stem = models.TextField()
    option_a = models.CharField(max_length=1000)
    option_b = models.CharField(max_length=1000)
    option_c = models.CharField(max_length=1000)
    option_d = models.CharField(max_length=1000)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)

    explanation = models.TextField(blank=True, default='')
    teaching_note = models.TextField(blank=True, default='')
    common_mistake = models.TextField(blank=True, default='')
    exam_tip = models.TextField(blank=True, default='')

    exam_session = models.ForeignKey(ExamSession, on_delete=models.PROTECT,
                                     null=True, blank=True,
                                     related_name='prelims_questions')
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT,
                              null=True, blank=True,
                              related_name='prelims_questions')
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2030)])
    exam_source = models.CharField(max_length=50, default='UPPCS')

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                null=True, blank=True,
                                related_name='prelims_pyqs')
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                null=True, blank=True,
                                related_name='prelims_pyqs')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT,
                              null=True, blank=True,
                              related_name='prelims_pyqs')

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES,
                                  default='Medium')
    blooms_level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)])
    concept_cluster = models.CharField(max_length=100, blank=True, default='')
    tags = models.TextField(blank=True, default='')
    repeat_count = models.PositiveIntegerField(default=1)
    is_free = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    stem_length = models.PositiveIntegerField(default=0)
    option_avg_length = models.PositiveIntegerField(default=0)
    estimated_time_seconds = models.PositiveIntegerField(default=72)

    times_attempted = models.PositiveIntegerField(default=0)
    times_correct = models.PositiveIntegerField(default=0)
    avg_time_taken = models.FloatField(default=0.0)

    review_status = models.CharField(max_length=25, choices=REVIEW_CHOICES,
                                     default='draft')
    batch_id = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_prelims_pyq'
        ordering = ['exam_source', 'year', 'question_id']
        verbose_name = 'Prelims PYQ'
        verbose_name_plural = 'Prelims PYQs'

    def __str__(self):
        return f"{self.question_id} — {self.stem[:60]}"

    def save(self, *args, **kwargs):
        self.stem_length = len(self.stem)
        opts = [self.option_a, self.option_b, self.option_c, self.option_d]
        self.option_avg_length = sum(len(o) for o in opts) // 4
        super().save(*args, **kwargs)


class MainsPYQ(models.Model):
    SECTION_CHOICES = [('A', 'Section A'), ('B', 'Section B')]
    BLOOMS_CHOICES = [
        ('Remember', 'Remember'), ('Understand', 'Understand'),
        ('Apply', 'Apply'), ('Analyze', 'Analyze'),
        ('Evaluate', 'Evaluate'), ('Unknown', 'Unknown'),
    ]
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'), ('Medium', 'Medium'),
        ('Hard', 'Hard'), ('Unknown', 'Unknown'),
    ]
    REVIEW_CHOICES = [
        ('draft', 'Draft'), ('reviewed', 'Reviewed'), ('approved', 'Approved'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    legacy_code = models.CharField(max_length=30, unique=True)
    question_text = models.TextField()

    exam_session = models.ForeignKey(ExamSession, on_delete=models.PROTECT,
                                     related_name='mains_questions')
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT,
                              related_name='mains_questions')
    paper_section = models.ForeignKey(PaperSection, on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name='mains_questions')
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    marks = models.PositiveIntegerField(default=8)
    q_no = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=5, blank=True, default='')

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                related_name='mains_pyqs')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='mains_pyqs')
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='mains_pyqs')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='mains_pyqs')
    chapter_name = models.CharField(max_length=60, blank=True, default='')
    chapter_code = models.CharField(max_length=10, blank=True, default='')
    topic_name = models.CharField(max_length=100, blank=True, default='')
    sub_topic_text = models.CharField(max_length=100, blank=True, default='')
    micro_topic_text = models.CharField(max_length=200, blank=True, default='')

    competency = models.ForeignKey(Competency, on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='mains_questions')
    blooms_level = models.CharField(max_length=12, choices=BLOOMS_CHOICES,
                                    default='Understand')
    difficulty = models.CharField(max_length=8, choices=DIFFICULTY_CHOICES,
                                  default='Medium')
    is_state_specific = models.BooleanField(default=False)
    concept_cluster = models.CharField(max_length=50, blank=True, default='')
    cross_link = models.CharField(max_length=30, blank=True, default='')
    fact_code = models.CharField(max_length=20, blank=True, default='')
    tag_code = models.CharField(max_length=50, blank=True, default='')

    times_asked = models.PositiveIntegerField(default=0)
    last_asked_year = models.PositiveIntegerField(null=True, blank=True)
    review_status = models.CharField(max_length=10, choices=REVIEW_CHOICES,
                                     default='draft')
    batch_id = models.CharField(max_length=20, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_mains_pyq'
        ordering = ['exam_session', 'paper', 'section', 'q_no']
        verbose_name = 'Mains PYQ'
        verbose_name_plural = 'Mains PYQs'

    def __str__(self):
        return f"{self.legacy_code} — {self.question_text[:60]}"

    @property
    def full_code(self):
        yr = self.exam_session.year % 100
        paper = self.paper.short_name.replace('-', '')
        blooms = self.blooms_level[0] if self.blooms_level else 'U'
        return (f"{self.exam_session.exam.short_name}{yr:02d}-{paper}"
                f"-{self.subject.code}-{self.section}-{blooms}-Q{self.q_no:02d}")


# ─────────────────────────────────────────────
# TRACKING & LINKS
# ─────────────────────────────────────────────

class QuestionAppearance(models.Model):
    question = models.ForeignKey(PrelimsPYQ, on_delete=models.CASCADE,
                                 related_name='appearances')
    exam_source = models.CharField(max_length=50)
    exam_name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    question_number = models.PositiveIntegerField(null=True, blank=True)
    is_primary = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_question_appearance'
        ordering = ['year']
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'year', 'exam_source'],
                name='unique_question_exam_year'),
        ]

    def __str__(self):
        return f"{self.question.question_id} → {self.exam_name} {self.year}"


class ExamSource(models.Model):
    FAMILY_CHOICES = [
        ('UPPCS', 'UP PCS'), ('UKPCS', 'Uttarakhand PCS'),
        ('MPPCS', 'MP PCS'), ('BPSC', 'Bihar PCS'),
        ('RAS', 'Rajasthan RAS'), ('CGPCS', 'CG PCS'),
        ('IAS', 'UPSC IAS'), ('OTHER', 'Other'),
    ]
    STAGE_CHOICES = [
        ('prelims', 'Prelims'), ('mains', 'Mains'),
    ]

    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=30)
    exam_family = models.CharField(max_length=20, choices=FAMILY_CHOICES)
    exam_stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    state = models.CharField(max_length=30, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_exam_source'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.short_name} ({self.get_exam_family_display()})"


class FactQuestionLink(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE,
                             related_name='question_links')
    prelims_question = models.ForeignKey(PrelimsPYQ, on_delete=models.CASCADE,
                                         null=True, blank=True,
                                         related_name='fact_links')
    mains_question = models.ForeignKey(MainsPYQ, on_delete=models.CASCADE,
                                       null=True, blank=True,
                                       related_name='fact_links')
    is_direct = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_fact_question_link'

    def __str__(self):
        q = self.prelims_question or self.mains_question
        return f"Fact → {q}"


class SiteQuestionLink(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE,
                             related_name='question_links')
    prelims_question = models.ForeignKey(PrelimsPYQ, on_delete=models.CASCADE,
                                         null=True, blank=True,
                                         related_name='site_links')
    mains_question = models.ForeignKey(MainsPYQ, on_delete=models.CASCADE,
                                       null=True, blank=True,
                                       related_name='site_links')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_site_question_link'

    def __str__(self):
        q = self.prelims_question or self.mains_question
        return f"{self.site.name} → {q}"
