"""T47: Import 5 Stone Age PrelimsPYQ questions + QuestionAppearance records."""
import os, io, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'mypcs_project.settings'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import django; django.setup()
from content.models import (
    PrelimsPYQ, QuestionAppearance, Subject, Unit, Chapter,
    Topic, SubTopic, MicroTopic, ExamSource, Exam, ExamSession, Paper,
)

# Lookups
chapter = Chapter.objects.get(name='Stone Age')
unit = chapter.unit
subject = unit.subject
paper = Paper.objects.get(short_name='PRE1')
exam_pre = Exam.objects.get(short_name='UPP')

questions = [
    {
        'question_id': 'HIST-SA-006',
        'stem': 'Robert Bruce Foote, who discovered first Palaeolithic tool in India, was a/an -',
        'option_a': 'Geologist',
        'option_b': 'Archaeologist',
        'option_c': 'Paleobotanist',
        'option_d': 'Historian',
        'correct_answer': 'A',
        'explanation': 'According to Encyclopaedia Britannica, Robert Bruce Foote was a British geologist and archaeologist. He is considered as the father of Indian pre-history. He was associated with the Geological Survey of India and documented the antiquities of the Stone Age. Hence, both options (a) and (b) can be considered as correct.',
        'difficulty': 'Medium',
        'topic_lookup': 'Prehistoric Pioneers',
        'common_mistake': 'Students pick Archaeologist (b) - Foote was BOTH geologist AND archaeologist, but his primary title was Geologist with the Geological Survey of India.',
        'exam_tip': 'Controversial question - official answer is (a) but both a & b defensible. Go with official designation in exam.',
        'tags': 'Robert Bruce Foote,Palaeolithic,Geological Survey of India',
        'appearances': [
            {'exam_name': 'U.P. Lower Subordinate (Prelims)', 'year': 2015, 'is_primary': True},
        ],
    },
    {
        'question_id': 'HIST-SA-007',
        'stem': 'The three-age system, divided into stone, bronze and iron from the collection of Copenhagen museum was coined by -',
        'option_a': 'Thomsen',
        'option_b': 'Lubbock',
        'option_c': 'Taylor',
        'option_d': 'Childe',
        'correct_answer': 'A',
        'explanation': 'The three age system - Stone, Bronze and Iron - from the collection of Copenhagen museum was coined by Christian Jurgensen Thomsen.',
        'difficulty': 'Easy',
        'topic_lookup': 'Prehistoric Pioneers',
        'common_mistake': 'Students confuse Thomsen (three-age system) with Lubbock (subdivided Stone Age into Palaeolithic and Neolithic).',
        'exam_tip': 'Thomsen = Three-age system. Lubbock = Subdivided Stone Age. Both exam favorites.',
        'tags': 'Thomsen,Three-age system,Copenhagen museum',
        'appearances': [
            {'exam_name': 'U.P.P.C.S. (Prelims)', 'year': 2010, 'is_primary': True},
        ],
    },
    {
        'question_id': 'HIST-SA-008',
        'stem': 'According to the excavated evidence, the domestication of animals began in -',
        'option_a': 'Lower Palaeolithic period',
        'option_b': 'Middle Palaeolithic period',
        'option_c': 'Upper Palaeolithic period',
        'option_d': 'Mesolithic period',
        'correct_answer': 'D',
        'explanation': 'According to the excavated evidence, the domestication of animals began in the Mesolithic period. The earliest pieces of evidence of domestication of animals in India have been found at Adamgarh (Narmadapuram, M.P.) and Bagor (Bhilwara, Rajasthan).',
        'difficulty': 'Medium',
        'topic_lookup': 'Mesolithic Age',
        'common_mistake': 'Students pick Neolithic - but domestication BEGAN in Mesolithic (Adamgarh, Bagor). Neolithic is when it became widespread.',
        'exam_tip': 'Mesolithic = domestication BEGINS. Neolithic = agriculture + permanent settlement.',
        'tags': 'Mesolithic,domestication,Adamgarh,Bagor',
        'appearances': [
            {'exam_name': 'U.P.C.S. (Mains)', 'year': 2006, 'is_primary': True},
        ],
    },
    {
        'question_id': 'HIST-SA-009',
        'stem': 'Three human skeletons in a single grave were recovered at -',
        'option_a': 'Sarai Nahar Rai',
        'option_b': 'Damdama',
        'option_c': 'Mahadaha',
        'option_d': 'Langhnaj',
        'correct_answer': 'B',
        'explanation': 'Damdama is a Mesolithic site in Pratapgarh district of Uttar Pradesh. In Damdama, 41 human graves were found. Out of these graves, 5 are double burials. One triple burial grave is also found here. A grave with four human skeletons has been found at Sarai Nahar Rai.',
        'difficulty': 'Hard',
        'topic_lookup': 'Mesolithic Age',
        'common_mistake': 'Students pick Sarai Nahar Rai - that had FOUR skeletons, not three. Damdama had the triple burial.',
        'exam_tip': 'UP site! Damdama (Pratapgarh) = triple burial. Sarai Nahar Rai = quadruple. UPPCS loves UP sites.',
        'tags': 'Damdama,Pratapgarh,Mesolithic,burial,Sarai Nahar Rai,UP archaeology',
        'appearances': [
            {'exam_name': 'U.P.P.C.S. (Prelims)', 'year': 2016, 'is_primary': True},
        ],
    },
    {
        'question_id': 'HIST-SA-010',
        'stem': 'The earliest evidence of agriculture in Indian sub-continent comes from -',
        'option_a': 'Koldihwa',
        'option_b': 'Lahuradeva',
        'option_c': 'Mehrgarh',
        'option_d': 'Tokwa',
        'correct_answer': 'B',
        'explanation': 'According to the latest research, the earliest evidence of agriculture in Indian sub-continent has been reported from the Lahuradeva site in Sant Kabir Nagar district, Uttar Pradesh. The evidence dates back to around 9000-7000 B.C. Before this, earlier evidence of wheat was found at Mehrgarh (Balochistan, Pakistan) around 7000 B.C.',
        'difficulty': 'Hard',
        'topic_lookup': 'Neolithic Age',
        'common_mistake': 'Students pick Mehrgarh - OLD answer. Latest research shows Lahuradeva (UP) is earlier at 9000-7000 BC vs Mehrgarh 7000 BC.',
        'exam_tip': 'TRICK - answer changed with new research! Lahuradeva (Sant Kabir Nagar, UP) is now correct. REPEAT question - asked 2004 AND 2008!',
        'tags': 'Lahuradeva,Mehrgarh,agriculture,Neolithic,Sant Kabir Nagar,UP,repeat question',
        'appearances': [
            {'exam_name': 'U.P. Lower Subordinate (Prelims)', 'year': 2004, 'is_primary': True},
            {'exam_name': 'U.P. Lower Subordinate (Prelims)', 'year': 2008, 'is_primary': False},
        ],
    },
]

imported = 0
appearances_created = 0
errors = []

for q in questions:
    try:
        topic = Topic.objects.get(chapter=chapter, name=q['topic_lookup'])
        primary_year = q['appearances'][0]['year']
        exam_session = ExamSession.objects.get(exam=exam_pre, year=primary_year)

        defaults = {
            'stem': q['stem'],
            'option_a': q['option_a'],
            'option_b': q['option_b'],
            'option_c': q['option_c'],
            'option_d': q['option_d'],
            'correct_answer': q['correct_answer'],
            'explanation': q['explanation'],
            'common_mistake': q.get('common_mistake', ''),
            'exam_tip': q.get('exam_tip', ''),
            'exam_session': exam_session,
            'paper': paper,
            'subject': subject,
            'unit': unit,
            'chapter': chapter,
            'topic': topic,
            'difficulty': q['difficulty'],
            'exam_source': 'UPPCS',
            'year': primary_year,
            'tags': q.get('tags', ''),
            'repeat_count': len(q['appearances']),
            'batch_id': 'TEST-002',
            'review_status': 'draft',
            'is_free': True,
            'is_active': True,
        }

        obj, created = PrelimsPYQ.objects.update_or_create(
            question_id=q['question_id'],
            defaults=defaults,
        )
        action = 'CREATED' if created else 'UPDATED'
        print(f"{q['question_id']} {action} | {q['stem'][:50]}...")
        imported += 1

        for app in q['appearances']:
            exam_src_obj = ExamSource.objects.get(name=app['exam_name'])
            qa, qa_created = QuestionAppearance.objects.get_or_create(
                question=obj,
                year=app['year'],
                exam_source=exam_src_obj.exam_family,
                defaults={
                    'exam_name': app['exam_name'],
                    'is_primary': app['is_primary'],
                }
            )
            if qa_created:
                appearances_created += 1
                primary_tag = '(PRIMARY)' if app['is_primary'] else '(REPEAT)'
                print(f"  -> {app['exam_name']} {app['year']} {primary_tag}")

    except Exception as e:
        print(f"{q['question_id']} ERROR: {e}")
        errors.append((q['question_id'], str(e)))

# === RESULTS ===
print()
print("=" * 40)
print("  IMPORT RESULT")
print("=" * 40)
print(f"Questions: {imported}/5")
print(f"Appearances: {appearances_created}")
print(f"Errors: {len(errors)}")
for qid, err in errors:
    print(f"  {qid}: {err}")

# === VERIFY ===
print()
print("=== VERIFICATION ===")
qs = PrelimsPYQ.objects.filter(batch_id='TEST-002')
print(f"Batch TEST-002: {qs.count()} questions")
print()
for q in qs:
    apps = q.appearances.all()
    app_str = ', '.join([f"{a.exam_name} {a.year}" for a in apps])
    topic_str = q.topic if q.topic else '?'
    print(f"  {q.question_id} | Ans:{q.correct_answer} | {q.difficulty}")
    print(f"    Topic: {topic_str}")
    print(f"    Appearances({apps.count()}): {app_str}")
    print()

# === BRIDGE TABLE TEST ===
print("=== BRIDGE TABLE TEST (Q5 repeat) ===")
q5 = PrelimsPYQ.objects.filter(question_id='HIST-SA-010').first()
if q5:
    print(f"  repeat_count: {q5.repeat_count}")
    for a in q5.appearances.all():
        print(f"  -> {a.exam_name} {a.year} | primary: {a.is_primary}")

# === HIERARCHY TEST ===
print()
print("=== FULL HIERARCHY TEST ===")
ch = Chapter.objects.get(name='Stone Age')
for t in Topic.objects.filter(chapter=ch):
    print(f"  {ch.name} -> {t.name}")
    for st in SubTopic.objects.filter(topic=t):
        print(f"    -> {st.name}")
        for mt in MicroTopic.objects.filter(sub_topic=st):
            print(f"      -> {mt.name}")
