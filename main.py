"""
I16 Google Logbooks software

 - create new logbooks from a template, replacing experiment details
 - Get sharable link from new logbook and put in a list of logbooks
"""

from i16_google_logbook_scripts import write_exppars, create_new_logbook

exppars = {
    'id': 'mm12345-1',
    'datadir': '/dls/i16/data/2022/mm12345-1',
    'scriptdir': '/dls_sw/i16/scripts/2022/mm12345-1',
    'text_file': '/dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.txt',
    'notebook_file': '/dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.ipynb',
    'example_script': '/dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.py',
    'experiment_parameters': 'mm12345-1.json',
    'logbook_name': 'mm12345-1 TestLogbook',
    'logbook_id': '',
    'logbook_link': '',
    'diffcalc_name': 'xtl_mm12345-1',
    'user_emails': {
        'name': 'email@address.com',
    },
    'replace_fields': {
        '{{visit_id}}': 'mm12345-1',
        '{{users}}': ' Mike A, Sarah J, Mikail V',
        '{{localcontact}}': ' Dan Porter',
        '{{samplename}}': ' Ca2RuO4',
        '{{latticeparameter}}': ' 2.85 2.85 10.8 90 90 120',
        '{{beamlinesetup}}': ' 8 keV, cryostat',
        '{{expdescription}}': ' coherent diffraction',
        '{{datadir}}': ' /dls/i16/data/2022/mm12345-1',
        '{{scriptdir}}': ' /dls_sw/i16/scripts/2022/mm12345-1',
        '{{firstdate}}': ' Wednesday 1 Feb',
        '{{daterange}}': ' 1-7/Feb/2022',
        '{{logbook_link}}': '',
    }
}
write_exppars(exppars)

create_new_logbook(exppars['experiment_parameters'])

