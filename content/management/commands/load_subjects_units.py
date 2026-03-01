import sys
import io

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from content.models import Subject, Unit


SUBJECTS_AND_UNITS = [
    ("Indian Polity & Governance", "⚖️", [
        "Constitutional Framework",
        "Federalism & Centre-State",
        "Parliament & State Legislature",
        "Elections & Political Process",
        "Judiciary",
        "Local Self-Government",
        "Rights & Duties",
    ]),
    ("History", "📜", [
        "Ancient & Medieval India",
        "Modern India (1757-1947)",
        "World History",
        "Art & Culture",
    ]),
    ("Geography", "🌍", [
        "Physical Geography",
        "Indian Geography",
        "Human Geography",
    ]),
    ("Economy", "💰", [
        "Indian Economy",
        "Agriculture & Food Security",
        "Inclusive Growth & Development",
        "Infrastructure & Energy",
        "Industry & MSME",
        "Fiscal & Monetary Policy",
    ]),
    ("Ethics", "🧭", [
        "Ethics & Human Values",
        "Ethics in Governance",
        "Ethical Concepts & Theories",
        "Attitude & Aptitude",
        "Emotional Intelligence",
        "Moral Thinkers & Philosophers",
        "Case Studies",
    ]),
    ("Society", "👥", [
        "Indian Society",
        "Social Empowerment",
        "Indian Culture & Heritage",
    ]),
    ("Internal Security", "🛡️", [
        "Internal Security",
        "Defence & Military",
        "Cyber Security",
        "Disaster Management",
    ]),
    ("International Relations", "🌐", [
        "India's Foreign Policy",
        "Bilateral & Multilateral Relations",
        "International Organizations",
        "Geopolitics & Strategy",
    ]),
    ("Science & Technology", "🔬", [
        "S&T Developments",
        "Emerging Technologies",
        "Biotechnology",
    ]),
    ("Environment & Ecology", "🌱", [
        "Environment & Ecology",
        "Conservation & Biodiversity",
    ]),
    ("Uttar Pradesh Special", "🏛️", [
        "UP History & Culture",
        "UP Geography",
        "UP Economy",
        "UP Governance & Polity",
        "UP Society",
        "UP Environment",
        "UP Science & Tech",
        "UP Law & Order",
    ]),
]


class Command(BaseCommand):
    help = 'Load initial Subjects and Units into the database'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Preview without saving')

    def handle(self, *args, **options):
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            self.stdout = self.stdout.__class__(sys.stdout)

        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('\n🔍 DRY RUN\n'))

        subjects_created = 0
        units_created = 0

        for order, (subj_name, icon, unit_names) in enumerate(SUBJECTS_AND_UNITS, 1):
            subj_slug = slugify(subj_name)

            if not dry_run:
                subject, created = Subject.objects.get_or_create(
                    slug=subj_slug,
                    defaults={'name': subj_name, 'icon': icon,
                              'sort_order': order, 'is_active': True},
                )
                if created:
                    subjects_created += 1
                    self.stdout.write(f'  ✅ Subject: {icon} {subj_name}')
                else:
                    self.stdout.write(f'  ⏭️  Subject exists: {subj_name}')
            else:
                self.stdout.write(f'  ✅ Would create Subject: {icon} {subj_name}')
                subjects_created += 1
                subject = None

            for u_order, unit_name in enumerate(unit_names, 1):
                unit_slug = slugify(unit_name)
                if not dry_run:
                    _, created = Unit.objects.get_or_create(
                        slug=unit_slug,
                        defaults={'subject': subject, 'name': unit_name,
                                  'sort_order': u_order, 'is_active': True},
                    )
                    if created:
                        units_created += 1
                        self.stdout.write(f'      → {unit_name}')
                else:
                    self.stdout.write(f'      → Would create: {unit_name}')
                    units_created += 1

        self.stdout.write(f'\n✅ Subjects: {subjects_created}, Units: {units_created}')
        if dry_run:
            self.stdout.write(self.style.WARNING(
                '\n💡 Run without --dry-run to save'))
