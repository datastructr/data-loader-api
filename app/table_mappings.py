"""This file will establish the mapping of columns in tables to other tables
and their foreign key constraints

If you have junction tables that are populated based on foreign keys this is
where you will create your mappings

This mapping created the junctions throughout your backend system effectively
so you have nothing other than configure and GO => => =>
"""

'''
junction_tables
:type: list
:elements: type: String the junction table names in your schema
'''
junction_tables = [
    'leads_countries',
    'leads_sectors',
    'leads_tests',
]


'''
Mapping structure...

    'table_name': {
        'junction_tables': {
            'junction_table_name': {
                'mapped_table': 'table_name',
                'columns': {
                    'column_name': {
                        'reference_table': 'reference_column_name',
                    },
                    'column_name': {
                        'reference_table': 'reference_column_name',
                    }
                },
            },
        },
        'required': [
            'column_name',
            ...
        ],
        'not_required': [
            'column_name',
            ...
        ],
        'selectors': {
            'column_name': 'select_table',
            ...
        }
    ...
    }

    'table_name'            => the KEY REQUIRED for the uploader to work
        'ingest_table_name' => the name of the table that will fire the
            junction aggregation

    'junction_tables'       => the KEY REQUIRED for the uploader to work
        'junction_table_name'
                            => the name of the table in the database that is
                               your junction table

    'mapped_table'          => the KEY REQUIRED for the uploader to work
        'table_name'        => the name of the table you have the many to many
            relationship with (selectors column's table)

    'columns'               => the KEY REQUIRED for the uploader to work
        'column_name'       => the name of the column mapped in your
            junction table
        'reference_table'   => the name of the table the column_name is
            referencing
        'reference_column_name'
                            => the name of the column in the reference_table
                               mapping to the column_name

    'required'              => the KEY REQUIRED for the uploader to work
        'column_name'       => this is the column name of the required
            junctions to fire when uploading data to them

    'not_required'          => the KEY REQUIRED for the uploader to work
        'column_name'       => this is the column name of the optional
            junctions calls when uploading data

    'selectors'             => the KEY REQUIRED for the uploader to work
        'column_name'       => the name of the column in the 'select_table'
            that must be unique to get a primary key back with
        'select_table'      => the name of the table you are firing a junction
            aggregation with


    ===========================================================================
    NOTE: Think of the 'columns' like describing the junction table's schema ==
    ===========================================================================
'''
mapping = {
    'leads': {
        'junction_tables': {
            'leads_countries': {
                'mapped_table': 'countries',
                'columns': {
                    'lead_fid': {
                        'leads': 'id',
                    },
                    'country_id': {
                        'countries': 'id',
                    }
                },
            },
            'leads_sectors': {
                'mapped_table': 'sectors',
                'columns': {
                    'lead_fid': {
                        'leads': 'id',
                    },
                    'sector_id': {
                        'sector_id': 'id',
                    }
                },
            },
            'leads_tests': {
                'mapped_table': 'tests',
                'columns': {
                    'lead_fid': {
                        'leads': 'id',
                    },
                    'sector_id': {
                        'sector_id': 'id',
                    }
                },
            },
        },
        'required': [
            'sector_name',
            'country_name',
        ],
        'not_required': [
            'optional_field'
        ],
        'selectors': {
            'sector_name': 'lead_sectors',
            'country_name': 'lead_countries',
            'test_name': 'lead_tests',
        }
    }
}
