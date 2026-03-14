import io
import sys
from django.core.management.base import BaseCommand
from tracker.models import BuildTask, BuildSubTask


class Command(BaseCommand):
    help = 'Seed BuildTask and BuildSubTask tables with project tasks'

    def handle(self, *args, **options):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        tasks_data = [
            # Session 2 (all done)
            {"task_id": "T11", "title": "Verify PostgreSQL connection",
             "session": "S2", "group": "Setup", "module": "M1", "status": "done"},
            {"task_id": "T12", "title": "Create Subject model",
             "session": "S2", "group": "Content Models", "module": "M1", "status": "done"},
            {"task_id": "T13", "title": "Create Unit model",
             "session": "S2", "group": "Content Models", "module": "M1", "status": "done"},
            {"task_id": "T14", "title": "Create Exam + ExamSession models",
             "session": "S2", "group": "Content Models", "module": "M1", "status": "done"},
            {"task_id": "T15", "title": "Create Paper model",
             "session": "S2", "group": "Content Models", "module": "M1", "status": "done"},
            {"task_id": "T16", "title": "Create Competency model",
             "session": "S2", "group": "Content Models", "module": "M1", "status": "done"},
            {"task_id": "T17", "title": "Create MainsPYQ model",
             "session": "S2", "group": "Content Models", "module": "M1", "status": "done"},
            {"task_id": "T18", "title": "Register all in Django Admin",
             "session": "S2", "group": "Admin", "module": "M1", "status": "done"},
            {"task_id": "T19", "title": "Seed Subject + Unit data",
             "session": "S2", "group": "Data Seeding", "module": "M1", "status": "done"},
            {"task_id": "T20", "title": "Seed Exam + ExamSession data",
             "session": "S2", "group": "Data Seeding", "module": "M1", "status": "done"},
            {"task_id": "T21", "title": "Seed Paper data",
             "session": "S2", "group": "Data Seeding", "module": "M1", "status": "done"},
            {"task_id": "T22", "title": "Seed Competency data",
             "session": "S2", "group": "Data Seeding", "module": "M1", "status": "done"},
            {"task_id": "T23", "title": "Enrich Paper model fields",
             "session": "S2", "group": "Content Models", "module": "M1", "status": "done"},

            # Session 3
            {"task_id": "T24", "title": "Audit all existing models and tables",
             "session": "S3", "group": "Group 0: Audit", "module": "M1", "status": "done"},
            {"task_id": "T25", "title": "Chapter model",
             "session": "S3", "group": "Group A: Syllabus Hierarchy", "module": "M1", "status": "done"},
            {"task_id": "T26", "title": "Topic + SubTopic models",
             "session": "S3", "group": "Group A: Syllabus Hierarchy", "module": "M1", "status": "done"},
            {"task_id": "T27", "title": "Part model (Paper sections)",
             "session": "S3", "group": "Group A: Syllabus Hierarchy", "module": "M1", "status": "done"},
            {"task_id": "T28", "title": "PrelimsPYQ model",
             "session": "S3", "group": "Group B: Question Models", "module": "M1", "status": "done",
             "models_created": "PrelimsPYQ"},
            {"task_id": "T29", "title": "Enrich MainsPYQ ForeignKeys",
             "session": "S3", "group": "Group B: Question Models", "module": "M1", "status": "done"},
            {"task_id": "T30", "title": "KeyTerm model (glossary)",
             "session": "S3", "group": "Group C: Teaching Content", "module": "M1", "status": "pending"},
            {"task_id": "T31", "title": "ContentBlock model (notes)",
             "session": "S3", "group": "Group C: Teaching Content", "module": "M1", "status": "pending"},
            {"task_id": "T32", "title": "Tag model (tagging system)",
             "session": "S3", "group": "Group C: Teaching Content", "module": "M1", "status": "pending"},
            {"task_id": "T33", "title": "Custom User model",
             "session": "S3", "group": "Group D: Users", "module": "M2", "status": "pending",
             "notes": "CRITICAL: Must be done before T34. AUTH_USER_MODEL must be set before any User FK migrations."},
            {"task_id": "T34", "title": "Practice app (5 models)",
             "session": "S3", "group": "Group E: Practice", "module": "M3", "status": "pending",
             "depends_on": "T33",
             "models_created": "PracticeSession, PracticeAnswer, Streak, DailyQuota, StudentTopicMastery"},
            {"task_id": "T35", "title": "Gamification app (LeaderboardEntry)",
             "session": "S3", "group": "Group F: Gamification", "module": "M3", "status": "pending",
             "depends_on": "T33"},
            {"task_id": "T36", "title": "Assessments app (MockTest + Attempt)",
             "session": "S3", "group": "Group G: Assessments", "module": "M3", "status": "pending",
             "depends_on": "T33"},
            {"task_id": "T37", "title": "Payments app (Order + Subscription)",
             "session": "S3", "group": "Group H: Payments", "module": "M3", "status": "pending",
             "depends_on": "T33"},
            {"task_id": "T38", "title": "Notifications app",
             "session": "S3", "group": "Group I: Notifications", "module": "M3", "status": "pending",
             "depends_on": "T33"},
            {"task_id": "T39", "title": "Register ALL models in Admin",
             "session": "S3", "group": "Group J: Admin + Verify", "module": "M1", "status": "pending",
             "depends_on": "T30,T31,T32,T33,T34,T35,T36,T37,T38"},
            {"task_id": "T40", "title": "Final table verification + architecture tree",
             "session": "S3", "group": "Group J: Admin + Verify", "module": "M1", "status": "pending",
             "depends_on": "T39"},
        ]

        subtasks_data = [
            # T28 subtasks
            {"subtask_id": "T28B", "task_id": "T28",
             "title": "Upgrade PrelimsPYQ to full 8-layer schema (+25 fields)",
             "status": "pending"},
            {"subtask_id": "T28C", "task_id": "T28",
             "title": "Cascading autocomplete dropdowns in Admin (django-smart-selects)",
             "status": "pending", "depends_on": "T28B"},

            # T29 subtasks
            {"subtask_id": "T29B", "task_id": "T29",
             "title": "Create BuildTask + SubTask tracker in Admin",
             "status": "in_progress"},
            {"subtask_id": "T29C", "task_id": "T29",
             "title": "Test import 10 Prelims + 10 Mains PYQs",
             "status": "pending", "depends_on": "T28B,T28C"},
        ]

        # Seed tasks
        task_created = 0
        task_existing = 0
        for data in tasks_data:
            defaults = {k: v for k, v in data.items() if k != 'task_id'}
            _, created = BuildTask.objects.get_or_create(
                task_id=data['task_id'],
                defaults=defaults,
            )
            if created:
                task_created += 1
            else:
                task_existing += 1

        # Seed subtasks
        sub_created = 0
        sub_existing = 0
        for data in subtasks_data:
            task_obj = BuildTask.objects.get(task_id=data['task_id'])
            defaults = {k: v for k, v in data.items()
                        if k not in ('subtask_id', 'task_id')}
            defaults['task'] = task_obj
            _, created = BuildSubTask.objects.get_or_create(
                subtask_id=data['subtask_id'],
                defaults=defaults,
            )
            if created:
                sub_created += 1
            else:
                sub_existing += 1

        # Count by session/status
        s2_total = BuildTask.objects.filter(session='S2').count()
        s2_done = BuildTask.objects.filter(session='S2', status='done').count()
        s3_total = BuildTask.objects.filter(session='S3').count()
        s3_done = BuildTask.objects.filter(session='S3', status='done').count()
        s3_pending = BuildTask.objects.filter(session='S3', status='pending').count()
        total_subs = BuildSubTask.objects.count()

        print()
        print("=" * 40)
        print("  TASK TRACKER SEEDED")
        print("=" * 40)
        print(f"Session 2: {s2_total} tasks (all done)")
        print(f"Session 3: {s3_total} tasks ({s3_done} done, {s3_pending} pending)")
        print(f"Subtasks: {total_subs} total")

        for sub in BuildSubTask.objects.all():
            print(f"  {sub.subtask_id}: {sub.title} ({sub.status})")

        print()
        if task_existing or sub_existing:
            print(f"(Skipped {task_existing} existing tasks, "
                  f"{sub_existing} existing subtasks)")
        print()
