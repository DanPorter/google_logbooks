"""
Google Drive API
Generic ease of use functions

By Dan Porter
I16 Beamline Scientist
Diamond Light Source Ltd
2022
"""

import io
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def signin(credentials_file='credentials.json', token_file='token.json'):
    """
    Sign in to Google Drive API
      Make sure you've set up a project on:
        https://console.cloud.google.com/apis/credentials?
      and downloaded the credentials.json file
    :param credentials_file: filename of credentials.json
    :param token_file: filename of token.json (doesn't need to exist, but will be created)
    :return: credentials
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds


def build_services(creds=None):
    """
    Build Google Drive API services
    :param creds: GoogleDocsAPI credentials
    :return: drive_service, docs_service
    """
    if creds is None:
        creds = signin()
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service


def get_drive_file_dict(file_id, drive_service=None, creds=None):
    """
    Get sharable link for file
    :param file_id: str, FileID
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: dict Drive file details
    """
    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)
    file = drive_service.files().get(fileId=file_id, fields='id, name, webContentLink, webViewLink').execute()
    return file


def get_drive_file_metadata(file_id, fields='*', drive_service=None, creds=None):
    """
    Get sharable link for file
    :param file_id: str, FileID
    :param fields: str, list of metadata fields, e.g. 'id, name, webContentLink, webViewLink'
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: dict Drive file details
    """
    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)
    file = drive_service.files().get(fileId=file_id, fields=fields).execute()
    return file


def get_drive_file_link(file_id, drive_service=None, creds=None):
    """
    Get sharable link for file
    :param file_id: str, FileID
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: str webViewlink
    """
    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)
    file = drive_service.files().get(fileId=file_id, fields='webViewLink').execute()
    return file.get('webViewLink')


def find_filename(filename, drive_service=None, creds=None):
    """
    Returns list of files with this filename in Drive
     output file dicts has fields: 'id', 'name', 'webContentLink'
    :param filename: str name of file to search for
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: list of file dicts
    """

    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)

    files = []
    page_token = None
    while True:
        response = drive_service.files().list(q="name = '%s'" % filename,
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name, webContentLink, webViewLink)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            # print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            # print('webViewLink: %s' % file.get('webContentLink'))
            files += [file]
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files


def change_permission(file_id, can_edit=False, drive_service=None, creds=None):
    """
    Change permission to anyone can view or edit
    :param file_id: str, FileID
    :param can_edit: bool, if True, anyone can edit the file
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: None
    """

    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)

    # Change permissions
    role = 'writer' if can_edit else 'reader'
    user_permission = {
        'type': 'anyone',  # 'user', 'group', 'domain', 'anyone'
        'role': role,  # 'owner', 'organizer', 'fileOrganizer', 'writer' ,'commenter', 'reader'
    }
    drive_service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ).execute()
    print('Permissions changed to %s for everyone' % role)


def upload_file(filename, folder_id=None, drive_service=None, creds=None):
    """
    Upload a local file to Google Drive. If the file exists already, return the previous file link
    :param filename: local filename to upload
    :param folder_id: None or id of folder
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: webContentLink
    """

    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)

    name = os.path.basename(filename)
    already_uploaded = find_filename(name, drive_service)
    if already_uploaded:
        print('%s already uploaded!' % filename)
        file = already_uploaded[-1]
    else:
        file_metadata = {
            'name': name,
        }
        if folder_id:
            file_metadata['parents'] = folder_id

        print(file_metadata)
        media = MediaFileUpload(filename,
                                mimetype='image/jpeg',
                                resumable=True)
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id, name, webContentLink, webViewLink').execute()
        print('File uploaded: %s' % filename)

    change_permission(file.get('id'), drive_service)

    print('File name: %s' % file.get('name'))
    print('File ID: %s' % file.get('id'))
    print('File webContentlink: %s' % file.get('webContentLink'))
    return file.get('webContentLink')


def download_pdf(file_id, local_filename, drive_service=None, creds=None):
    """
    Download GoogldDoc to pdf on local filesystem
    :param file_id: str, FileID
    :param local_filename: str pdf filename
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: None
    """
    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)

    request = drive_service.files().export_media(fileId=file_id, mimeType='application/pdf')
    fh = io.FileIO(local_filename, 'wb')  # this can be used to write to disk
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    print('Downloaded: %s' % local_filename)


def copy_file(id_to_copy, new_file_name, drive_service=None, creds=None):
    """
    Copy a file in Google Drive to a new file, return the new ID
    :param id_to_copy: str, FileID
    :param new_file_name: str, new file name
    :param drive_service: GoogleDriveAPI service
    :param creds: GoogleDocsAPI credentials
    :return: copied file ID
    """

    if drive_service is None:
        if creds is None:
            creds = signin()
        drive_service = build('drive', 'v3', credentials=creds)
    body = {'name': new_file_name}
    print(id_to_copy)
    print(body)
    copiedfile = drive_service.files().copy(fileId=id_to_copy, body=body).execute()
    return copiedfile['id']


def merge_template(id_to_merge, merge_fields, docs_service=None, creds=None):
    """
    Merge fields in file - replace {{fields}} with strings
    :param id_to_merge: FileID of Doc to merge
    :param merge_fields: dict of fields to replace {'{{replace me}}': 'with me'}
    :param docs_service: GoogleDocsAPI service
    :param creds: GoogleDocsAPI credentials
    :return: None
    """

    # Create Google Drive/Docs services, requiring google account credentials
    if docs_service is None:
        if creds is None:
            creds = signin()
        docs_service = build('docs', 'v1', credentials=creds)

    # Merge new logbook with replacement fields
    requests = [
        {
            'replaceAllText': {
                'containsText': {
                    'text': match,
                    'matchCase': 'true'
                },
                'replaceText': replacewith,
            }
        } for match, replacewith in merge_fields.items()
    ]
    docs_service.documents().batchUpdate(
        documentId=id_to_merge, body={'requests': requests}).execute()
    print('Merge comleted')


def append_text(doc_id, text_to_append='', docs_service=None, creds=None):
    """
    Append text to end of a GoogleDoc
    :param doc_id: str GoogleDoc id
    :param text_to_append: str text to add to end of file
    :param docs_service: GoogleDocsAPI service
    :param creds: GoogleDocsAPI credentials
    :return: None
    """

    # Create Google Drive/Docs services, requiring google account credentials
    if docs_service is None:
        if creds is None:
            creds = signin()
        docs_service = build('docs', 'v1', credentials=creds)

    # Find the end of the file
    document = docs_service.documents().get(documentId=doc_id).execute()
    body = document['body']
    content = body['content']
    temp = content[len(content) - 1]
    endIndex = temp['endIndex']
    print('end Index = %s' % endIndex)

    # Edit the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': endIndex - 1,
                },
                'text': text_to_append
            }
        },
    ]
    docs_service.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}).execute()
    print("Append completed")


def append_image(doc_id, image_loc='', folder_id=None, docs_service=None, creds=None):
    """
    Append image to end of Goodle Doc
    :param doc_id: str GoogleDoc id
    :param image_loc: location of file, either local filename or http link
    :param folder_id: None or Drive folder to add image to
    :param docs_service: GoogleDocsAPI service
    :param creds: GoogleDocsAPI credentials
    :return: None
    """

    # Create Google Drive/Docs services, requiring google account credentials
    if docs_service is None:
        if creds is None:
            creds = signin()
        docs_service = build('docs', 'v1', credentials=creds)

    # Find the end of the file
    document = docs_service.documents().get(documentId=doc_id).execute()
    body = document['body']
    content = body['content']
    temp = content[len(content) - 1]
    end_index = temp['endIndex']
    print('end Index = %s' % end_index)

    if not image_loc.startswith('http'):
        image_loc = upload_file(image_loc, folder_id, creds=creds)

    print('\nappend image loc: %s\n' % image_loc)
    # Edit the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index - 1,
                },
                'text': '\n'
            },
        },
        {
            'insertInlineImage': {
                'location': {
                    'index': end_index,
                },
                'uri': image_loc
            }
        },
    ]
    docs_service.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}).execute()
    print("Image appended!")
