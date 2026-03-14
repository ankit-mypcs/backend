import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_competency_exam_paper_examsession_mainspyq'),
    ]

    operations = [
        # Renames
        migrations.RenameField('MainsPYQ', 'code', 'legacy_code'),
        migrations.RenameField('MainsPYQ', 'chapter', 'chapter_name'),
        migrations.RenameField('MainsPYQ', 'topic', 'topic_name'),
        migrations.RenameField('MainsPYQ', 'sub_topic', 'sub_topic_text'),
        migrations.RenameField('MainsPYQ', 'micro_topic', 'micro_topic_text'),

        # New fields
        migrations.AddField(
            model_name='mainspyq',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='mainspyq',
            name='q_no',
            field=models.PositiveIntegerField(default=0,
                                              help_text='Question number within paper/section'),
        ),
        migrations.AddField(
            model_name='mainspyq',
            name='state',
            field=models.CharField(blank=True, default='', max_length=5,
                                   help_text='State code e.g. UP'),
        ),
        migrations.AddField(
            model_name='mainspyq',
            name='times_asked',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mainspyq',
            name='last_asked_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mainspyq',
            name='review_status',
            field=models.CharField(
                choices=[('draft', 'Draft'), ('reviewed', 'Reviewed'),
                         ('approved', 'Approved')],
                default='draft', max_length=10),
        ),
        migrations.AddField(
            model_name='mainspyq',
            name='batch_id',
            field=models.CharField(blank=True, default='', max_length=20),
        ),

        # Update ordering
        migrations.AlterModelOptions(
            name='mainspyq',
            options={
                'db_table': 'content_mains_pyq',
                'ordering': ['exam_session', 'paper', 'section', 'q_no'],
                'verbose_name': 'Mains PYQ',
                'verbose_name_plural': 'Mains PYQs',
            },
        ),
    ]
