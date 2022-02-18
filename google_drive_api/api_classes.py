"""
Google Drive API
Ease of use classes

By Dan Porter
I16 Beamline Scientist
Diamond Light Source Ltd
2022
"""

import google_drive_api.api_functions as api


class GoogleDriveApi:
    """
    Google Drive API class
    usage:
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
    """
    creds = None
    drive_service = None
    docs_service = None

    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.creds = api.signin(credentials_file, token_file)
        self.drive_serivce, self.docs_service = api.build_services(self.creds)

    def get_file(self, file_id):
        return GoogleDriveFile(file_id, self)

    def find_files(self, filename):
        """
        Find files in Google Drive
        :param filename: str name of file
        :return: [list of GoogleDriveFiles]
        """
        files = api.find_filename(filename, self.drive_service)
        return [self.get_file(file) for file in files]

    def is_file(self, filename):
        """
        Return if file exists already
        :param filename: str name of file
        :return: True/False
        """
        files = api.find_filename(filename, self.drive_service)
        if files:
            return True
        return False

    def get_link(self, file_id):
        """
        Get sharable link for file
        :param file_id: str, FileID
        :return: str file webViewLink
        """
        return api.get_drive_file_link(file_id, self.drive_service)

    def change_permission(self, file_id, can_edit=False):
        """
        Change permission to anyone can view or edit
        :param file_id: str, FileID
        :param can_edit: bool, if True, anyone can edit the file
        """
        api.change_permission(file_id, can_edit, self.drive_service)

    def upload_file(self, filename):
        """
        Upload a local file to Google Drive. If the file exists already, return the previous file link
        :param filename: local filename to upload
        """
        api.upload_file(filename, self.drive_service)

    def download_pdf(self, file_id, local_filename):
        """
        Download GoogldDoc to pdf on local filesystem
        :param file_id: str, FileID
        :param local_filename: str pdf filename
        """
        api.download_pdf(file_id, local_filename, self.drive_service)

    def copy_file(self, id_to_copy, new_file_name):
        """
        Copy a file in Google Drive to a new file, return the new ID
        :param id_to_copy: str, FileID
        :param new_file_name: str, new file name
        :return GoogleDriveFile of copied file
        """
        copiedfile_id = api.copy_file(id_to_copy, new_file_name, self.drive_service)
        return self.get_file(copiedfile_id)

    def merge_template(self, id_to_merge, merge_fields):
        """
        Merge fields in file - replace {{fields}} with strings
        :param id_to_merge: FileID of Doc to merge
        :param merge_fields: dict of fields to replace {'{{replace me}}': 'with me'}
        """
        api.merge_template(id_to_merge, merge_fields, self.docs_service)

    def append_text(self, doc_id, text_to_append=''):
        """
        Append text to end of a GoogleDoc
        :param doc_id: str GoogleDoc id
        :param text_to_append: str text to add to end of file
        """
        api.append_text(doc_id, text_to_append, self.docs_service)

    def append_image(self, doc_id, image_loc=''):
        """
        Append image to end of Goodle Doc
        :param doc_id: str GoogleDoc id
        :param image_loc: location of file, either local filename or http link
        """
        api.append_image(doc_id, image_loc, self.docs_service)


class GoogleDriveFile:
    """
    Container for Google Drive File

    api = GoogleDriveApi('creds.json')
    file = GoogleDriveFile('asboide', api)

    :param file: str or dict with field 'id'
    :param gdriveapi: GoogleDriveApi
    """
    name = ''
    link = None

    def __init__(self, file, gdriveapi):
        self.drive_service = gdriveapi.drive_service
        self.docs_service = gdriveapi.docs_service

        try:
            self.id = file['id']
        except TypeError:
            # file_dict is str
            self.id = file
        if 'name' in file and 'webViewLink' in file:
            self.name = file['name']
            self.link = file['webViewLink']
        else:
            self._update_file_dict()

    def __repr__(self):
        return "GoogleDriveFile('%s')" % self.id

    def __str__(self):
        out = '%s\n' % self.__repr__()
        out += '    File ID: %s\n' % self.id
        out += '  File name: %s\n' % self.name
        out += '  File link: %s\n' % self.link
        return out

    def _update_file_dict(self):
        file = api.get_drive_file_dict(self.id, self.drive_service)
        self.name = file['name']
        self.link = file['webViewLink']

    def change_permission(self, can_edit=False):
        """
        Change permission to anyone can view or edit
        :param can_edit: bool, if True, anyone can edit the file
        """
        api.change_permission(self.id, can_edit, self.drive_service)

    def download_pdf(self, local_filename):
        """
        Download file to pdf on local filesystem
        :param local_filename: str pdf filename
        """
        api.download_pdf(self.id, local_filename, self.drive_service)

    def merge(self, merge_fields):
        """
        Merge fields in file - replace {{fields}} with strings
        :param merge_fields: dict of fields to replace {'{{replace me}}': 'with me'}
        """
        api.merge_template(self.id, merge_fields, self.docs_service)

    def append_text(self, text_to_append):
        """
        Append text to the end of the file
        :param text_to_append: str text to add to end of file
        """
        api.append_text(self.id, text_to_append, self.docs_service)

    def append_image(self, image_loc):
        """
        Append a image to the end of the file
        :param image_loc: location of file, either local filename or http link
        :return:
        """
        api.append_image(self.id, image_loc, self.docs_service)
