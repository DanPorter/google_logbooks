"""
Google Drive API
Various shortcuts for basic editing of Google Docs

requires:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Usage:
    from google_drive_api import GoogleDriveApi
    gdrive = GoogleDriveApi('credentials.json')

    doc = gdrive.get_file('file_id')
    [docs] = gdrive.find_file('filename')
    'link' = gdrive.get_link('file_id')
    gdrive.change_permission('file_id', can_edit=False)
    gdrive.upload('/path/to/file')
    doc = gdrive.copy_file('id_to_copy', 'new_name')
    gdrive.merge_template('file_id', {'{{replace_me}}': 'with me'})
    gdrive.append_text('file_id', 'text to append')
    gdrive.append_image('file_id', 'loc/of/image.png')

By Dan Porter
I16 Beamline Scientist
Diamond Light Source Ltd
2022
"""

__version__ = "1.0.0"
__date__ = '18/02/2022'

from google_drive_api.api_classes import GoogleDriveApi
