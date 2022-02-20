"""
Google Drive API example
"""

from google_drive_api import GoogleDriveApi

CREDS = 'dan_creds.json'
TOKEN = 'dan_token.json'

gdrive = GoogleDriveApi(CREDS, TOKEN)

folder = '1WkNF9XVipF5dnzR3NAhvih-216yo0PxB'  # Thermometers
file = r"C:\Users\dgpor\Dropbox\Python\BrexitVotes.png"
docid = '1-OOHQBItCv8GyY0Z5NXrPGPtMa6Th9Pcoq_WZfeBvF0'  # PythonAPI_GenFromTemplate_11Feb

doc = gdrive.get_file(docid)

doc.append_image(file, folder)

#doc.download_pdf('test.pdf')

print(doc)

print(doc.get_metadata())
