from django.db import models


class Subject(models.Model):
    CATEGORY_CHOICES = [
        ('foundation', 'Foundation'),
        ('advanced', 'Advanced'),
        ('up_special', 'UP Special'),
        ('csat', 'CSAT'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    number = models.IntegerField()
    title = models.CharField(max_length=300)
    code = models.CharField(max_length=50, unique=True, help_text='e.g., POL-SRC')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['subject', 'number']
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return f"{self.code} - {self.title}"


class Question(models.Model):
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    QUESTION_TYPE_CHOICES = [
        ('factual', 'Factual'),
        ('conceptual', 'Conceptual'),
        ('application', 'Application'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='questions')
    question_id = models.CharField(max_length=50, unique=True, help_text='e.g., POL-SRC-001')
    stem = models.TextField(verbose_name='Question Text')
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    explanation = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    exam_source = models.CharField(max_length=200)
    year = models.IntegerField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f"{self.question_id} - {self.stem[:50]}..."


class KeyTerm(models.Model):
    term = models.CharField(max_length=200)
    definition = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='key_terms')
    related_questions = models.ManyToManyField(Question, blank=True, related_name='key_terms')

    class Meta:
        ordering = ['term']
        verbose_name_plural = 'Key Terms'

    def __str__(self):
        return self.term
