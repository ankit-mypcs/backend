from import_export import resources, fields
from .models import PrelimsPYQ


class PrelimsPYQResource(resources.ModelResource):
    """
    Maps Excel columns to PrelimsPYQ model fields.

    Excel columns:
      Q.No., Question, Option (a), Option (b), Option (c), Option (d),
      Answer, Exam Name, Exam Stage, Year, Parse_Error, Review_Status
    """

    question_id = fields.Field(attribute='question_id', column_name='Q.No.')
    stem = fields.Field(attribute='stem', column_name='Question')
    option_a = fields.Field(attribute='option_a', column_name='Option (a)')
    option_b = fields.Field(attribute='option_b', column_name='Option (b)')
    option_c = fields.Field(attribute='option_c', column_name='Option (c)')
    option_d = fields.Field(attribute='option_d', column_name='Option (d)')
    correct_answer = fields.Field(attribute='correct_answer', column_name='Answer')
    exam_source = fields.Field(attribute='exam_source', column_name='Exam Name')
    year = fields.Field(attribute='year', column_name='Year')
    review_status = fields.Field(attribute='review_status', column_name='Review_Status')

    class Meta:
        model = PrelimsPYQ
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['question_id']

        # Only these fields are imported — rest stay default/null
        fields = (
            'question_id', 'stem',
            'option_a', 'option_b', 'option_c', 'option_d',
            'correct_answer', 'exam_source', 'year', 'review_status',
        )

        # Fields to exclude from import
        exclude = ('id', 'uid', 'created_at', 'updated_at')

    def before_import_row(self, row, **kwargs):
        """Clean and transform each row before import."""

        # 1. Generate question_id if it's just a number
        qno = row.get('Q.No.', '')
        if qno and str(qno).isdigit():
            row['Q.No.'] = f"Q-{str(qno).zfill(4)}"

        # 2. Clean answer format: (a) → A, (b) → B, etc.
        answer = row.get('Answer', '')
        if answer:
            answer = str(answer).strip()
            answer_map = {
                '(a)': 'A', '(b)': 'B', '(c)': 'C', '(d)': 'D', '(*)': '*',
            }
            row['Answer'] = answer_map.get(answer.lower(), answer.upper())

        # 3. Clean empty options — set to empty string not None
        for opt in ['Option (a)', 'Option (b)', 'Option (c)', 'Option (d)']:
            if not row.get(opt):
                row[opt] = ''

        # 4. Default review_status
        if not row.get('Review_Status'):
            row['Review_Status'] = 'ok'

        # 5. Default year
        year = row.get('Year', 0)
        try:
            row['Year'] = int(year) if year else 0
        except (ValueError, TypeError):
            row['Year'] = 0

    def skip_row(self, instance, original, row, import_validation_errors=None):
        """Skip blank questions."""
        review = row.get('Review_Status', '')
        if review == 'blank_question':
            return True
        if not row.get('Question', '').strip():
            return True
        return super().skip_row(
            instance, original, row,
            import_validation_errors=import_validation_errors,
        )
