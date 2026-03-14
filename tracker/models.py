from django.db import models


class BuildTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('blocked', 'Blocked'),
        ('skipped', 'Skipped'),
    ]

    task_id = models.CharField(max_length=10, unique=True,
                               help_text="e.g. T24, T28")
    title = models.CharField(max_length=200)
    session = models.CharField(max_length=10,
                               help_text="e.g. S2, S3")
    group = models.CharField(max_length=100,
                             help_text="e.g. Group A: Syllabus Hierarchy")
    module = models.CharField(max_length=10, blank=True, default='',
                              help_text="e.g. M1, M2")
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='pending')
    priority = models.PositiveIntegerField(default=0,
                                           help_text="Lower = higher priority")
    depends_on = models.CharField(max_length=200, blank=True, default='',
                                  help_text="e.g. T25,T26")
    models_created = models.TextField(blank=True, default='',
                                      help_text="e.g. Chapter, Topic, SubTopic")
    files_changed = models.TextField(blank=True, default='',
                                     help_text="e.g. content/models.py, content/admin.py")
    notes = models.TextField(blank=True, default='')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tracker_task'
        ordering = ['session', 'task_id']
        verbose_name = 'Build Task'
        verbose_name_plural = 'Build Tasks'

    def __str__(self):
        return f"{self.task_id}: {self.title} [{self.status}]"


class BuildSubTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('blocked', 'Blocked'),
        ('skipped', 'Skipped'),
    ]

    task = models.ForeignKey(BuildTask, on_delete=models.CASCADE,
                             related_name='subtasks')
    subtask_id = models.CharField(max_length=10, unique=True,
                                  help_text="e.g. T28B, T28C")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='pending')
    depends_on = models.CharField(max_length=200, blank=True, default='',
                                  help_text="e.g. T28B,T28C")
    notes = models.TextField(blank=True, default='')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tracker_subtask'
        ordering = ['task', 'subtask_id']
        verbose_name = 'Build Sub-Task'
        verbose_name_plural = 'Build Sub-Tasks'

    def __str__(self):
        return f"{self.subtask_id}: {self.title} [{self.status}]"
