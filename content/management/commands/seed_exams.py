"""
seed_exams.py — Create Exam, State, and Paper records for UPPCS + BPSC.
Safe to run multiple times (uses get_or_create).

Usage: python manage.py seed_exams
"""
from django.core.management.base import BaseCommand
from content.models import Exam, State, Paper, PrelimsPYQ


class Command(BaseCommand):
    help = "Seed UPPCS and BPSC exam data (states, exams, papers)"

    def handle(self, *args, **options):
        # ── States ──
        up, _ = State.objects.get_or_create(
            code='UP',
            defaults={
                'name': 'Uttar Pradesh',
                'exam_name': 'UPPCS',
                'exam_full': 'Uttar Pradesh Provincial Civil Service',
                'sort_order': 1,
            },
        )
        br, _ = State.objects.get_or_create(
            code='BR',
            defaults={
                'name': 'Bihar',
                'exam_name': 'BPSC',
                'exam_full': 'Bihar Public Service Commission',
                'sort_order': 2,
            },
        )
        self.stdout.write(f"  States: UP={up.id}, BR={br.id}")

        # ── Exams ──
        uppcs, _ = Exam.objects.get_or_create(
            short_name='UPPCS',
            defaults={
                'name': 'Uttar Pradesh Provincial Civil Service',
                'slug': 'uppcs',
                'state': up,
                'description': 'Combined State/Upper Subordinate Services exam conducted by UPPSC.',
                'is_target_exam': True,
            },
        )
        bpsc, _ = Exam.objects.get_or_create(
            short_name='BPSC',
            defaults={
                'name': 'Bihar Public Service Commission',
                'slug': 'bpsc',
                'state': br,
                'description': 'Combined Competitive Exam conducted by BPSC.',
                'is_target_exam': True,
            },
        )
        self.stdout.write(f"  Exams: UPPCS={uppcs.id}, BPSC={bpsc.id}")

        # ── Papers (UPPCS) ──
        uppcs_gs1, _ = Paper.objects.get_or_create(
            short_name='UPPCS-P-GS1',
            defaults={
                'exam': uppcs,
                'name': 'UPPCS Prelims General Studies Paper I',
                'slug': 'uppcs-prelims-gs1',
                'exam_stage': 'prelims',
                'total_marks': 200,
                'total_questions': 150,
                'duration_minutes': 120,
                'paper_type': 'objective',
                'negative_marking': True,
                'sort_order': 1,
            },
        )
        uppcs_gs2, _ = Paper.objects.get_or_create(
            short_name='UPPCS-P-GS2',
            defaults={
                'exam': uppcs,
                'name': 'UPPCS Prelims CSAT Paper II',
                'slug': 'uppcs-prelims-gs2',
                'exam_stage': 'prelims',
                'total_marks': 200,
                'total_questions': 100,
                'duration_minutes': 120,
                'paper_type': 'objective',
                'is_qualifying': True,
                'negative_marking': True,
                'sort_order': 2,
            },
        )
        self.stdout.write(f"  UPPCS Papers: GS1={uppcs_gs1.id}, GS2={uppcs_gs2.id}")

        # ── Papers (BPSC) ──
        bpsc_gs, _ = Paper.objects.get_or_create(
            short_name='BPSC-P-GS',
            defaults={
                'exam': bpsc,
                'name': 'BPSC Prelims General Studies',
                'slug': 'bpsc-prelims-gs',
                'exam_stage': 'prelims',
                'total_marks': 150,
                'total_questions': 150,
                'duration_minutes': 120,
                'paper_type': 'objective',
                'negative_marking': False,
                'sort_order': 1,
            },
        )
        self.stdout.write(f"  BPSC Papers: GS={bpsc_gs.id}")

        # ── Link existing PYQs to UPPCS exam ──
        linked = PrelimsPYQ.objects.filter(
            exam_source='UPPCS', exam__isnull=True
        ).update(exam=uppcs)
        self.stdout.write(f"  Linked {linked} existing UPPCS PYQs to exam record")

        self.stdout.write(self.style.SUCCESS("Done! Exam data seeded."))
