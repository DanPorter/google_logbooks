"""
Google Drive API example
"""

from google_drive_api import GoogleDriveApi

CREDS = 'i16_user_google_creds.json'

gdrive = GoogleDriveApi(CREDS)

doc = gdrive.get_file('1VumxVxyzXFuLOMsIIPvUYUEhgIOQo_aiKFhVSYucO0Y')

doc.download_pdf('test.pdf')

print(doc)
