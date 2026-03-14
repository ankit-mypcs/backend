import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Subject(models.Model):
    code = models.CharField(max_length=4, unique=True,
                            help_text="Short code e.g. PY, HY, GY")
    name = models.CharField(max_length=40, unique=True,
                            help_text="Display name in English")
    name_hi = models.CharField(max_length=60, blank=True, default='',
                               help_text="Display name in Hindi")
    slug = models.SlugField(max_length=50, unique=True,
                            help_text="URL-safe identifier")
    icon = models.CharField(max_length=5, blank=True, default='',
                            help_text="Emoji icon")
    description = models.TextField(blank=True, default='',
                                   help_text="1-2 sentence description")
    sort_order = models.PositiveIntegerField(default=0,
                                            help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True,
                                    help_text="Show to students?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_subject'
        ordering = ['sort_order', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name


class Unit(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                related_name='units',
                                help_text="Parent subject")
    name = models.CharField(max_length=50,
                            help_text="Display name in English")
    name_hi = models.CharField(max_length=80, blank=True, default='',
                               help_text="Display name in Hindi")
    slug = models.SlugField(max_length=60, unique=True,
                            help_text="URL-safe identifier")
    icon = models.CharField(max_length=5, blank=True, default='',
                            help_text="Emoji icon")
    description = models.TextField(blank=True, default='',
                                   help_text="1-2 sentence description")
    sort_order = models.PositiveIntegerField(default=0,
                                            help_text="Display order within subject")
    is_active = models.BooleanField(default=True,
                                    help_text="Show to students?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_unit'
        ordering = ['subject', 'sort_order', 'name']
        constraints = [
            models.UniqueConstraint(fields=['subject', 'name'],
                                    name='unique_unit_per_subject'),
        ]
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        return f"{self.subject.name} → {self.name}"


class Chapter(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT,
                             related_name='chapters',
                             help_text="Parent unit")
    name = models.CharField(max_length=200,
                            help_text="e.g. Fundamental Rights")
    name_hi = models.CharField(max_length=300, blank=True, default='',
                               help_text="Display name in Hindi")
    code = models.CharField(max_length=20,
                            help_text="Short code e.g. FR, DPSP, CA")
    slug = models.SlugField(max_length=120, unique=True,
                            help_text="URL-safe identifier")
    description = models.TextField(blank=True, default='',
                                   help_text="1-2 sentence description")
    sort_order = models.PositiveIntegerField(default=0,
                                            help_text="Display order within unit")
    question_count = models.PositiveIntegerField(default=0,
                                                 help_text="Denormalized count for speed")
    is_active = models.BooleanField(default=True,
                                    help_text="Show to students?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_chapter'
        ordering = ['unit', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['unit', 'name'],
                                    name='unique_chapter_per_unit'),
        ]
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return f"{self.unit.name} → {self.name}"


class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                related_name='topics',
                                help_text="Parent chapter")
    name = models.CharField(max_length=200,
                            help_text="e.g. Right to Equality (Art. 14-18)")
    name_hi = models.CharField(max_length=300, blank=True, default='',
                               help_text="Display name in Hindi")
    code = models.CharField(max_length=20, blank=True, default='',
                            help_text="Short code")
    slug = models.SlugField(max_length=150, unique=True,
                            help_text="URL-safe identifier")
    description = models.TextField(blank=True, default='',
                                   help_text="1-2 sentence description")
    sort_order = models.PositiveIntegerField(default=0,
                                            help_text="Display order within chapter")
    is_active = models.BooleanField(default=True,
                                    help_text="Show to students?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_topic'
        ordering = ['chapter', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['chapter', 'name'],
                                    name='unique_topic_per_chapter'),
        ]
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def __str__(self):
        return f"{self.chapter.name} → {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT,
                              related_name='subtopics',
                              help_text="Parent topic")
    name = models.CharField(max_length=200,
                            help_text="e.g. Abolition of Untouchability (Art. 17)")
    name_hi = models.CharField(max_length=300, blank=True, default='',
                               help_text="Display name in Hindi")
    sort_order = models.PositiveIntegerField(default=0,
                                            help_text="Display order within topic")
    is_active = models.BooleanField(default=True,
                                    help_text="Show to students?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_subtopic'
        ordering = ['topic', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['topic', 'name'],
                                    name='unique_subtopic_per_topic'),
        ]
        verbose_name = 'Sub-Topic'
        verbose_name_plural = 'Sub-Topics'

    def __str__(self):
        return f"{self.topic.name} → {self.name}"


class MicroTopic(models.Model):
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.PROTECT,
                                  related_name='microtopics',
                                  help_text="Parent sub-topic")
    name = models.CharField(max_length=200)
    name_hi = models.CharField(max_length=200, blank=True, default='')
    slug = models.SlugField(max_length=220, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_microtopic'
        ordering = ['sub_topic', 'sort_order', 'name']
        constraints = [
            models.UniqueConstraint(fields=['sub_topic', 'name'],
                                    name='unique_subtopic_microtopic'),
        ]
        verbose_name = 'Micro-Topic'
        verbose_name_plural = 'Micro-Topics'

    def __str__(self):
        return f"{self.sub_topic.name} → {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Exam(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            help_text="e.g. UPPCS Mains, UPPCS Prelims")
    short_name = models.CharField(max_length=10, unique=True,
                                  help_text="e.g. UPM, UPP")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_exam'
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def __str__(self):
        return self.name


class ExamSession(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT,
                             related_name='sessions')
    year = models.PositiveIntegerField()

    # Key dates
    notification_date = models.DateField(null=True, blank=True)
    prelims_date = models.DateField(null=True, blank=True)
    prelims_result_date = models.DateField(null=True, blank=True)
    mains_date = models.DateField(null=True, blank=True)
    mains_result_date = models.DateField(null=True, blank=True)
    interview_start_date = models.DateField(null=True, blank=True)
    final_result_date = models.DateField(null=True, blank=True)

    # Exam structure
    total_papers = models.PositiveIntegerField(default=4)
    total_questions_prelims = models.PositiveIntegerField(null=True, blank=True)
    total_questions_mains = models.PositiveIntegerField(null=True, blank=True)

    # Marking scheme
    positive_marks_prelims = models.DecimalField(
        max_digits=4, decimal_places=2, default=2.00)
    negative_marks_prelims = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.66)

    # Cutoffs — Prelims
    cutoff_prelims_general = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_prelims_obc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_prelims_sc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_prelims_st = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    # Cutoffs — Mains
    cutoff_mains_general = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_mains_obc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_mains_sc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    cutoff_mains_st = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    # Topper marks
    topper_marks_prelims = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    topper_marks_mains = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    topper_marks_final = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    # Statistics
    students_applied = models.PositiveIntegerField(null=True, blank=True)
    students_appeared_prelims = models.PositiveIntegerField(null=True, blank=True)
    students_appeared_mains = models.PositiveIntegerField(null=True, blank=True)
    students_cleared_prelims = models.PositiveIntegerField(null=True, blank=True)
    students_cleared_mains = models.PositiveIntegerField(null=True, blank=True)
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
        verbose_name = 'Exam Session'
        verbose_name_plural = 'Exam Sessions'

    def __str__(self):
        return f"{self.exam.name} {self.year}"


class Paper(models.Model):
    STAGE_CHOICES = [
        ('prelims', 'Prelims'),
        ('mains', 'Mains'),
        ('both', 'Both'),
    ]
    PAPER_TYPE_CHOICES = [
        ('objective', 'Objective'),
        ('subjective', 'Subjective'),
        ('essay', 'Essay'),
        ('language', 'Language'),
    ]

    name = models.CharField(max_length=50,
                            help_text="e.g. GS-I (History, Society, Geo)")
    short_name = models.CharField(max_length=10, unique=True,
                                  help_text="e.g. GS-I, GS-II")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # New enrichment fields
    exam_stage = models.CharField(max_length=10, choices=STAGE_CHOICES,
                                  default='mains',
                                  help_text="Prelims / Mains / Both")
    total_marks = models.PositiveIntegerField(default=0,
                                              help_text="Maximum marks for this paper")
    total_questions = models.PositiveIntegerField(default=0,
                                                  help_text="Total questions in paper")
    duration_minutes = models.PositiveIntegerField(default=180,
                                                   help_text="Exam duration in minutes")
    paper_type = models.CharField(max_length=12, choices=PAPER_TYPE_CHOICES,
                                  default='subjective',
                                  help_text="Objective / Subjective / Essay / Language")
    is_qualifying = models.BooleanField(default=False,
                                        help_text="Is this a qualifying paper?")
    negative_marking = models.BooleanField(default=False,
                                           help_text="Does this paper have negative marking?")
    introduced_year = models.PositiveIntegerField(null=True, blank=True,
                                                  help_text="Year this paper was introduced")
    syllabus_topics = models.JSONField(default=list, blank=True,
                                       help_text="List of syllabus topics")
    mains_overlap = models.JSONField(default=list, blank=True,
                                     help_text="List of related mains paper short_names")
    paper_data = models.JSONField(default=dict, blank=True,
                                  help_text="Flexible metadata (sections, marks breakup, etc.)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_paper'
        ordering = ['sort_order']
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'

    def __str__(self):
        return self.short_name


class Part(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT,
                              related_name='parts',
                              help_text="Parent paper")
    name = models.CharField(max_length=100,
                            help_text="e.g. Section A, Part I - Indian History")
    short_name = models.CharField(max_length=20,
                                  help_text="e.g. SEC-A")
    slug = models.SlugField(unique=True,
                            help_text="URL-safe identifier")
    description = models.TextField(blank=True, default='',
                                   help_text="1-2 sentence description")
    sort_order = models.PositiveIntegerField(default=0,
                                            help_text="Display order within paper")
    marks = models.PositiveIntegerField(default=0,
                                        help_text="Total marks for this part")
    question_count = models.PositiveIntegerField(default=0,
                                                 help_text="Denormalized count for speed")
    is_active = models.BooleanField(default=True,
                                    help_text="Show to students?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_part'
        ordering = ['paper', 'sort_order']
        constraints = [
            models.UniqueConstraint(fields=['paper', 'name'],
                                    name='unique_part_per_paper'),
        ]
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

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

    name = models.CharField(max_length=30, unique=True,
                            help_text="e.g. Discuss, Explain, Examine")
    description = models.TextField(blank=True, default='',
                                   help_text="What this verb asks students to do")
    blooms_level = models.CharField(max_length=12, choices=BLOOMS_CHOICES,
                                    blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_competency'
        ordering = ['sort_order', 'name']
        verbose_name = 'Competency'
        verbose_name_plural = 'Competencies'

    def __str__(self):
        return self.name


class MainsPYQ(models.Model):
    SECTION_CHOICES = [
        ('A', 'Section A'),
        ('B', 'Section B'),
    ]
    BLOOMS_CHOICES = [
        ('Remember', 'Remember'),
        ('Understand', 'Understand'),
        ('Apply', 'Apply'),
        ('Analyze', 'Analyze'),
        ('Evaluate', 'Evaluate'),
        ('Unknown', 'Unknown'),
    ]
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        ('Unknown', 'Unknown'),
    ]
    REVIEW_CHOICES = [
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
    ]

    # Identity
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    legacy_code = models.CharField(max_length=30, unique=True,
                                   help_text="e.g. UPM24-GS1-HIST-IN-R-Q01")
    question_text = models.TextField()

    # Exam linkage
    exam_session = models.ForeignKey(ExamSession, on_delete=models.PROTECT,
                                     related_name='questions')
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT,
                              related_name='questions')
    part = models.ForeignKey('Part', on_delete=models.PROTECT,
                             null=True, blank=True,
                             related_name='mains_pyqs_by_part',
                             help_text="Linked part/section (optional)")
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    marks = models.PositiveIntegerField(default=8)
    q_no = models.PositiveIntegerField(default=0,
                                       help_text="Question number within paper/section")
    state = models.CharField(max_length=5, blank=True, default='',
                             help_text="State code e.g. UP")

    # Content hierarchy
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                related_name='mains_pyqs')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT,
                             null=True, blank=True,
                             related_name='mains_pyqs')
    chapter = models.ForeignKey('Chapter', on_delete=models.PROTECT,
                                null=True, blank=True,
                                related_name='mains_pyqs_by_chapter',
                                help_text="Linked chapter (optional)")
    topic = models.ForeignKey('Topic', on_delete=models.PROTECT,
                              null=True, blank=True,
                              related_name='mains_pyqs_by_topic',
                              help_text="Linked topic (optional)")
    chapter_name = models.CharField(max_length=60, blank=True, default='')
    chapter_code = models.CharField(max_length=10, blank=True, default='')
    topic_name = models.CharField(max_length=100, blank=True, default='')
    sub_topic_text = models.CharField(max_length=100, blank=True, default='')
    micro_topic_text = models.CharField(max_length=200, blank=True, default='')

    # Classification
    competency = models.ForeignKey(Competency, on_delete=models.PROTECT,
                                   null=True, blank=True,
                                   related_name='questions')
    blooms_level = models.CharField(max_length=12, choices=BLOOMS_CHOICES,
                                    default='Understand')
    difficulty = models.CharField(max_length=8, choices=DIFFICULTY_CHOICES,
                                  default='Medium')
    is_up_specific = models.BooleanField(default=False)
    concept_cluster = models.CharField(max_length=50, blank=True, default='')
    cross_link = models.CharField(max_length=30, blank=True, default='')
    fact_code = models.CharField(max_length=20, blank=True, default='',
                                 help_text="Fact classification code")
    tag_code = models.CharField(max_length=50, blank=True, default='',
                                help_text="Tag classification code")

    # Tracking
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

    @property
    def short_code(self):
        yr = self.exam_session.year % 100
        return f"{self.exam_session.exam.short_name}{yr:02d}-Q{self.q_no:02d}"


class PrelimsPYQ(models.Model):
    ANSWER_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
    ]
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        ('Unknown', 'Unknown'),
    ]
    REVIEW_CHOICES = [
        ('draft', 'Draft'),
        ('ok', 'OK'),
        ('needs_review', 'Needs Review'),
        ('parse_error_no_options', 'Parse Error (No Options)'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
    ]

    # ── Identity ──
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    question_id = models.CharField(max_length=30, unique=True,
                                   help_text="e.g. UP-PRE-POL-2024-042")

    # ── Question content ──
    stem = models.TextField(help_text="Question text")
    stem_hi = models.TextField(blank=True, default='',
                               help_text="Question text in Hindi")
    option_a = models.CharField(max_length=1000)
    option_b = models.CharField(max_length=1000)
    option_c = models.CharField(max_length=1000)
    option_d = models.CharField(max_length=1000)
    correct_answer = models.CharField(
        max_length=1, choices=ANSWER_CHOICES,
        help_text="Correct option: A, B, C, or D")

    # ── Explanation content ──
    explanation = models.TextField(blank=True, default='',
                                   help_text="Why the answer is correct")
    explanation_hi = models.TextField(blank=True, default='',
                                      help_text="Explanation in Hindi")
    teaching_note = models.TextField(blank=True, default='',
                                     help_text="Deeper context for learning")
    mnemonic = models.TextField(blank=True, default='',
                                help_text="Memory aid")
    common_mistake = models.TextField(blank=True, default='',
                                      help_text="Common wrong reasoning")
    exam_tip = models.TextField(blank=True, default='',
                                help_text="Exam strategy tip")

    # ── Linkage ──
    exam_session = models.ForeignKey(ExamSession, on_delete=models.PROTECT,
                                     null=True, blank=True,
                                     related_name='prelims_questions')
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT,
                              null=True, blank=True,
                              related_name='prelims_questions')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                null=True, blank=True,
                                related_name='prelims_pyqs')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT,
                             null=True, blank=True,
                             related_name='prelims_pyqs')
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT,
                                null=True, blank=True,
                                related_name='prelims_pyqs')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT,
                              null=True, blank=True,
                              related_name='prelims_pyqs')

    # ── Classification ──
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES,
                                  default='Medium')
    exam_source = models.CharField(max_length=50, default='UPPCS',
                                   help_text="e.g. UPPCS, BPSC, UPSC")
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2026)],
        help_text="Year the question appeared")
    tags = models.TextField(blank=True, default='',
                            help_text="Comma-separated tags")
    blooms_level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        help_text="Bloom's taxonomy level 1-6")
    concept_cluster = models.CharField(max_length=100, blank=True, default='')
    repeat_frequency = models.PositiveIntegerField(default=0,
                                                   help_text="How many times repeated")
    repeat_count = models.PositiveIntegerField(default=1,
                                               help_text="How many times this question appeared across exams")
    is_free = models.BooleanField(default=True,
                                  help_text="Available to free-tier users?")
    is_active = models.BooleanField(default=True,
                                    help_text="Show to students?")

    # ── Auto-computed (Layer C) ──
    stem_length = models.PositiveIntegerField(default=0,
                                              help_text="Character count of stem")
    option_avg_length = models.PositiveIntegerField(default=0,
                                                    help_text="Average char count of options")
    estimated_time_seconds = models.PositiveIntegerField(default=72,
                                                         help_text="Estimated solve time")

    # ── Live Analytics (Layer D) ──
    times_attempted = models.PositiveIntegerField(default=0)
    times_correct = models.PositiveIntegerField(default=0)
    avg_time_taken = models.FloatField(default=0.0,
                                       help_text="Average time in seconds")

    # ── Admin ──
    review_status = models.CharField(max_length=25, choices=REVIEW_CHOICES,
                                     default='draft')
    batch_id = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_prelims_pyq'
        ordering = ['exam_session', 'subject', 'question_id']
        verbose_name = 'Prelims PYQ'
        verbose_name_plural = 'Prelims PYQs'

    def __str__(self):
        return f"{self.question_id} — {self.stem[:60]}"

    def save(self, *args, **kwargs):
        self.stem_length = len(self.stem)
        opts = [self.option_a, self.option_b, self.option_c, self.option_d]
        self.option_avg_length = sum(len(o) for o in opts) // 4 if opts else 0
        super().save(*args, **kwargs)


class QuestionAppearance(models.Model):
    question = models.ForeignKey(PrelimsPYQ, on_delete=models.CASCADE,
                                 related_name='appearances')
    exam_source = models.CharField(max_length=50,
                                   help_text="Exam family: UPPCS, MPPCS, UKPCS etc.")
    exam_name = models.CharField(max_length=100,
                                 help_text="Full name: U.P. Lower Sub. (Pre)")
    year = models.PositiveIntegerField()
    question_number = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Serial number in that paper: Q1, Q47 etc.")
    is_primary = models.BooleanField(default=True,
                                     help_text="True = first time this question appeared")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_question_appearance'
        ordering = ['question', 'year']
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'year', 'exam_source'],
                name='unique_question_exam_year',
            )
        ]
        verbose_name = 'Question Appearance'
        verbose_name_plural = 'Question Appearances'

    def __str__(self):
        return f"{self.question.question_id} → {self.exam_name} {self.year}"


EXAM_FAMILY_CHOICES = [
    ('UPPCS', 'UP PCS'),
    ('UKPCS', 'Uttarakhand PCS'),
    ('MPPCS', 'Madhya Pradesh PCS'),
    ('BPSC', 'Bihar PCS'),
    ('RAS', 'Rajasthan RAS'),
    ('IAS', 'UPSC IAS'),
    ('OTHER', 'Other'),
]

EXAM_STAGE_CHOICES = [
    ('prelims', 'Prelims'),
    ('mains', 'Mains'),
    ('interview', 'Interview'),
]


class ExamSource(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            help_text="Full name: U.P. Lower Subordinate (Prelims)")
    short_name = models.CharField(max_length=30,
                                  help_text="Short: UP Lower Sub Pre")
    exam_family = models.CharField(max_length=20, choices=EXAM_FAMILY_CHOICES,
                                   help_text="UPPCS, MPPCS etc.")
    exam_stage = models.CharField(max_length=20, choices=EXAM_STAGE_CHOICES,
                                  help_text="prelims, mains")
    state = models.CharField(max_length=30, blank=True, default='',
                             help_text="Uttar Pradesh, Madhya Pradesh etc.")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_exam_source'
        ordering = ['sort_order', 'name']
        verbose_name = 'Exam Source'
        verbose_name_plural = 'Exam Sources'

    def __str__(self):
        return f"{self.short_name} ({self.get_exam_family_display()})"
