"""This file will establish the mapping of columns in tables to other tables
and their foreign key constraints

If you have junction tables that are populated based on foreign keys this is
where you will create your mappings

This mapping created the junctions throughout your backend system effectively
so you have nothing other than configure and GO => => =>
"""


junction_tables = [
    'leads_countries',
    'leads_sectors',
    'leads_tests',
]


mapping = {
    'leads': {
        'junction_tables': {
            'leads_countries': {
                'mapped_table': 'countries',
                'mapped_field': 'id',
                'columns': {
                    'lead_fid': {
                        'leads': 'fid',
                    },
                    'country_id': {
                        'countries': 'id',
                    }
                },
            },
            'leads_sectors': {
                'mapped_table': 'sectors',
                'mapped_field': 'id',
                'columns': {
                    'lead_fid': {
                        'leads': 'fid',
                    },
                    'sector_id': {
                        'sectors': 'id',
                    }
                },
            },
            'leads_tests': {
                'mapped_table': 'tests',
                'mapped_field': 'id',
                'columns': {
                    'lead_fid': {
                        'leads': 'fid',
                    },
                    'test_id': {
                        'tests': 'id',
                    }
                },
            },
        },
        'required': [
            'sector',
            'country_name',
        ],
        'not_required': [
            'test_name'
        ],
        'selectors': {
            'sector': 'leads_sectors',
            'country_name': 'leads_countries',
            'test_name': 'leads_tests',
        }
    }
}


plugins = {
    'leads': [
        {
            'google_api': {
                'query_params': ['country_name', ],
                'mapped_fields': ['locations', ],
            },
        },
    ],
}

hidden_plugin_fields = {
    'leads': ['locations', ]
}

upload_tables = [
        'leads',
]