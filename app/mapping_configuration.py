"""This file will establish the mapping of columns in tables to other tables
and their foreign key constraints

If you have junction tables that are populated based on foreign keys this is
where you will create your mappings

The ingestion method disables all constraints on pre-ingestion for the upload
because it will greatly increase performance -- while allowing for inserting
through foreign key constraints as well.

This mapping created the junctions throughout your backend system effectively
so you have nothing other than configure and GO => => =>
"""

mapping = {
    'accounts': {
        'columns': {
            'id': {
                'answers': 'account_id',
                'questions': 'account_id'
            }
        }
    }
}