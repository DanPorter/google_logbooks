# google_logbooks
Use Google Drive API to create experiment logbooks

By Dan Porter, Diamond Light Source Ltd. 2022

### Usage
A *credentials.json* file is required and must be entered in the scripts for permission to communicate with GoogleDrive. [See below](#api_exp). 
####Command line usage
Run a python script from an experiment_parameters.json file
```bash
$ python i16_google_logbook_maker.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json
```

Download the logbook to the scripts folder:
```bash
$ python i16_google_logbook_downloader.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json
```

####Python Script usage

```python
import i16_google_logbook_scripts
from google_drive_api import GoogleDriveApi

gdrive = GoogleDriveApi('credentials.json')

doc = gdrive.get_file('file_id')
[doc, ] = gdrive.find_file('filename')
link = gdrive.get_link('file_id')
gdrive.change_permission('file_id', can_edit=False)
gdrive.upload('/path/to/file')
doc = gdrive.copy_file('id_to_copy', 'new_name')
gdrive.merge_template('file_id', {'{{replace_me}}': 'with me'})
gdrive.append_text('file_id', 'text to append')
gdrive.append_image('file_id', 'loc/of/image.png')
gdrive.download_pdf('file_id', 'file.pdf')

print(doc)  # shows filename, id, link
doc.merge({'{{replace_me}}': 'with me'})
i16_google_logbook_scripts.append_text('text to append')
i16_google_logbook_scripts.append_image('loc/of/image.png')
doc.download_pdf('file.pdf')
```

### Requires
- python3 with Google API
```bash
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Google Drive API Explanation {#api_exp}
https://console.cloud.google.com/apis/credentials?project=beamline-logbooks&supportedpurview=project

####First time Setup:
1. Create a API project on https://console.cloud.google.com
    - APIs + services > create project
2. Enable APIs & services > Enable Google Drive API, Google Docs API
3. Dashboard > Configure Consent screen > External
    - Add scopes: all Google Drive, all Google Docs
    - Add user: add your gmail account (you are not automatically a user!)
4. Create credentials - Dashboard > Credentials > + Create Credentials > OAuth 2.0 Client ID > Desktop App
    - Download json, rename client-id

This client ID file holds the credentials required to use the API, and must be accessed by the python program.

####Python quickstart example:

https://developers.google.com/drive/api/v3/quickstart/python

