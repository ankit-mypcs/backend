from django.db import migrations, models

SLUG_TO_CODE = {
    'indian-polity-governance': 'PG',
    'history': 'HY',
    'geography': 'GY',
    'economy': 'EY',
    'ethics': 'ES',
    'society': 'SY',
    'internal-security': 'IS',
    'international-relations': 'IR',
    'science-technology': 'ST',
    'environment-ecology': 'EE',
    'uttar-pradesh-special': 'UP',
}

SLUG_TO_ICON = {
    'indian-polity-governance': '\u2696\ufe0f',
    'history': '\U0001f3db\ufe0f',
    'geography': '\U0001f30f',
    'economy': '\U0001f4ca',
    'ethics': '\U0001f9ed',
    'society': '\U0001f465',
    'internal-security': '\U0001f6e1\ufe0f',
    'international-relations': '\U0001f310',
    'science-technology': '\U0001f4a1',
    'environment-ecology': '\U0001f33f',
    'uttar-pradesh-special': '\U0001f536',
}


def populate_codes(apps, schema_editor):
    Subject = apps.get_model('content', 'Subject')
    for subj in Subject.objects.all():
        subj.code = SLUG_TO_CODE.get(subj.slug, subj.slug[:4].upper())
        subj.icon = SLUG_TO_ICON.get(subj.slug, subj.icon)
        subj.save(update_fields=['code', 'icon'])


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        # Step 1: Add code field, nullable, no unique yet
        migrations.AddField(
            model_name='subject',
            name='code',
            field=models.CharField(default='', max_length=4),
            preserve_default=False,
        ),
        # Step 2: Populate codes and update icons
        migrations.RunPython(populate_codes, migrations.RunPython.noop),
        # Step 3: Now make it unique
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(
                help_text='Short code e.g. PY, HY, GY',
                max_length=4,
                unique=True,
            ),
        ),
    ]
