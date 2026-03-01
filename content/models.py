from django.db import models


class Subject(models.Model):
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
